"""Facebook handler using yt-dlp."""

import re
import shutil
from pathlib import Path
from typing import Optional, List, Dict, Any
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

# Thread-safe counter for progress
_progress_lock = threading.Lock()

from ..detector import detect_facebook_type
from ..core.database import Database
from ..core.downloader import sanitize_filename, get_source_folder
from ..core.progress import (
    console,
    show_found_items,
    confirm_download,
    select_items,
    print_info,
    print_success,
    print_error,
    print_warning,
    DownloadProgress,
)


def handle_facebook(url: str, output_dir: Path, db: Database, auto_confirm: bool = False, cookies_from_browser: Optional[str] = None) -> None:
    """Handle Facebook URLs (videos, pages, reels)."""
    if yt_dlp is None:
        print_error("yt-dlp is not installed. Please run: pip install yt-dlp")
        return

    facebook_type = detect_facebook_type(url)
    print_info(f"Facebook type: {facebook_type}")

    if cookies_from_browser:
        print_info(f"Using cookies from: {cookies_from_browser}")

    if facebook_type == "video" or facebook_type == "reel":
        download_video(url, output_dir, db, cookies_from_browser=cookies_from_browser)
    elif facebook_type == "page":
        download_page_videos(url, output_dir, db, auto_confirm=auto_confirm, cookies_from_browser=cookies_from_browser)


def download_video(url: str, output_dir: Path, db: Database, cookies_from_browser: Optional[str] = None) -> None:
    """Download a single Facebook video."""
    print_info("Fetching video info...")

    try:
        # Get video info first
        info_opts = {'quiet': True}
        if cookies_from_browser:
            info_opts['cookiesfrombrowser'] = (cookies_from_browser,)
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get('title', 'Unknown')
        uploader = info.get('uploader', info.get('channel', 'Facebook'))
        duration = info.get('duration', 0)

        # Show info
        console.print(f"\n[bold]{title}[/bold]")
        console.print(f"From: {uploader}")
        if duration:
            console.print(f"Duration: {duration // 60}:{duration % 60:02d}")

        # Create output folder
        source_folder = get_source_folder(output_dir, sanitize_filename(uploader), category="videos")
        safe_title = sanitize_filename(title)

        # Track in database
        dl_id = db.add_download(
            url=url,
            content_type="facebook",
            source_name=uploader,
            title=title,
            metadata={"video_id": info.get('id')}
        )

        # Download
        print_info("Downloading...")
        db.update_status(dl_id, "downloading")

        # Check if ffmpeg is available
        has_ffmpeg = shutil.which('ffmpeg') is not None

        if has_ffmpeg:
            # Best quality with merging
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
                'outtmpl': str(source_folder / f'{safe_title}.%(ext)s'),
                'writethumbnail': True,
                'writeinfojson': True,
                'merge_output_format': 'mp4',
                'progress_hooks': [_make_progress_hook()],
            }
        else:
            # Fallback: single format that doesn't need merging
            print_warning("ffmpeg not found - downloading single format (install ffmpeg for best quality)")
            ydl_opts = {
                'format': 'best[height<=1080]/best',
                'outtmpl': str(source_folder / f'{safe_title}.%(ext)s'),
                'writethumbnail': True,
                'writeinfojson': True,
                'progress_hooks': [_make_progress_hook()],
            }

        if cookies_from_browser:
            ydl_opts['cookiesfrombrowser'] = (cookies_from_browser,)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the actual downloaded file
        for ext in ['mp4', 'webm', 'mkv']:
            potential_file = source_folder / f'{safe_title}.{ext}'
            if potential_file.exists():
                db.update_status(dl_id, "complete", str(potential_file))
                break
        else:
            db.update_status(dl_id, "complete", str(source_folder / f'{safe_title}.mp4'))
        print_success(f"Downloaded: {title}")

    except Exception as e:
        print_error(f"Failed to download: {e}")
        if 'dl_id' in locals():
            db.update_status(dl_id, "error", error_message=str(e))


def _video_exists(source_folder: Path, safe_title: str) -> bool:
    """Check if video already exists in any supported format."""
    for ext in ['mp4', 'webm', 'mkv', 'm4a']:
        if (source_folder / f'{safe_title}.{ext}').exists():
            return True
    return False


def _download_single_video(
    item: Dict[str, Any],
    index: int,
    total: int,
    source_folder: Path,
    page_name: str,
    db: Database,
    progress_counter: Dict[str, int],
    cookies_from_browser: Optional[str] = None
) -> Dict[str, Any]:
    """Download a single video from a Facebook page. Thread-safe."""
    video_url = item['url']
    title = item['title']
    safe_title = sanitize_filename(f"{index:03d}_{title}")

    result = {"index": index, "title": title, "status": "unknown"}

    # Skip if already exists
    if _video_exists(source_folder, safe_title):
        with _progress_lock:
            progress_counter['skipped'] += 1
        result["status"] = "skipped"
        return result

    # Track in database
    dl_id = db.add_download(
        url=video_url,
        content_type="facebook",
        source_name=page_name,
        title=title
    )

    try:
        db.update_status(dl_id, "downloading")

        has_ffmpeg = shutil.which('ffmpeg') is not None
        if has_ffmpeg:
            ydl_opts = {
                'format': 'bestvideo[height<=1080]+bestaudio/best[height<=1080]/best',
                'outtmpl': str(source_folder / f'{safe_title}.%(ext)s'),
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
            }
        else:
            ydl_opts = {
                'format': 'best[height<=1080]/best',
                'outtmpl': str(source_folder / f'{safe_title}.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }

        if cookies_from_browser:
            ydl_opts['cookiesfrombrowser'] = (cookies_from_browser,)

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Find actual file and update database
        for ext in ['mp4', 'webm', 'mkv']:
            if (source_folder / f'{safe_title}.{ext}').exists():
                db.update_status(dl_id, "complete", str(source_folder / f'{safe_title}.{ext}'))
                break

        with _progress_lock:
            progress_counter['completed'] += 1
        result["status"] = "completed"

    except Exception as e:
        db.update_status(dl_id, "error", error_message=str(e))
        with _progress_lock:
            progress_counter['failed'] += 1
        result["status"] = "failed"
        result["error"] = str(e)

    return result


def download_page_videos(url: str, output_dir: Path, db: Database, auto_confirm: bool = False, max_workers: int = 3, cookies_from_browser: Optional[str] = None) -> None:
    """Download all videos from a Facebook page with concurrent downloads."""
    print_info("Fetching page videos...")

    try:
        # Extract page name from URL for display
        page_match = re.search(r'facebook\.com/([^/]+)', url)
        page_name = page_match.group(1) if page_match else "Facebook Page"

        # Get page videos - yt-dlp treats this as a playlist
        info_opts = {'quiet': True, 'extract_flat': True}
        if cookies_from_browser:
            info_opts['cookiesfrombrowser'] = (cookies_from_browser,)
        with yt_dlp.YoutubeDL(info_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        # Handle case where it's a single video (not a page)
        if info.get('_type') != 'playlist':
            print_info("Single video detected, downloading...")
            download_video(url, output_dir, db, cookies_from_browser=cookies_from_browser)
            return

        page_title = info.get('title', page_name)
        entries = info.get('entries', [])

        if not entries:
            print_warning("No videos found on page.")
            return

        # Build items list
        items = []
        for e in entries:
            if e:
                video_url = e.get('url', e.get('webpage_url', ''))
                if not video_url.startswith('http'):
                    video_url = f"https://www.facebook.com{video_url}" if video_url.startswith('/') else f"https://www.facebook.com/watch?v={e.get('id', '')}"
                items.append({
                    "title": e.get('title', 'Untitled'),
                    "url": video_url
                })

        # Show found items
        show_found_items("Facebook Page", page_title, items, "videos")

        # Confirm (skip if auto_confirm)
        if auto_confirm:
            choice = "all"
        else:
            choice = confirm_download(len(items), "videos")
            if choice == "none":
                print_info("Download cancelled.")
                return

            if choice == "select":
                indices = select_items(items)
                items = [items[i] for i in indices]

        # Create output folder
        source_folder = get_source_folder(output_dir, sanitize_filename(page_title), category="videos")

        # Check how many already exist
        existing_count = sum(1 for i, item in enumerate(items, 1)
                           if _video_exists(source_folder, sanitize_filename(f"{i:03d}_{item['title']}")))

        if existing_count > 0:
            print_info(f"Found {existing_count} already downloaded, will skip those")

        remaining = len(items) - existing_count
        if remaining == 0:
            print_success(f"All {len(items)} videos already downloaded!")
            return

        print_info(f"Downloading {remaining} videos ({max_workers} concurrent)...")

        # Progress tracking
        progress_counter = {'completed': 0, 'skipped': 0, 'failed': 0}

        # Download with thread pool for concurrent downloads
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all download tasks
            futures = {
                executor.submit(
                    _download_single_video,
                    item, i, len(items), source_folder, page_title, db, progress_counter, cookies_from_browser
                ): i for i, item in enumerate(items, 1)
            }

            # Process results as they complete
            for future in as_completed(futures):
                result = future.result()
                with _progress_lock:
                    done = progress_counter['completed'] + progress_counter['skipped'] + progress_counter['failed']

                if result["status"] == "completed":
                    console.print(f"[green]✓[/green] [{done}/{len(items)}] {result['title']}")
                elif result["status"] == "skipped":
                    console.print(f"[yellow]⊘[/yellow] [{done}/{len(items)}] {result['title']} (exists)")
                elif result["status"] == "failed":
                    console.print(f"[red]✗[/red] [{done}/{len(items)}] {result['title']}: {result.get('error', 'Unknown error')}")

        # Summary
        console.print("")
        print_success(f"Page complete: {progress_counter['completed']} downloaded, "
                     f"{progress_counter['skipped']} skipped, {progress_counter['failed']} failed")

    except Exception as e:
        print_error(f"Failed to process page: {e}")


def _make_progress_hook():
    """Create a progress hook for yt-dlp."""
    progress_bar = None

    def hook(d):
        nonlocal progress_bar
        if d['status'] == 'downloading':
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)

            if progress_bar is None and total:
                progress_bar = DownloadProgress()
                progress_bar.__enter__()
                progress_bar.start_task("Downloading", total)

            if progress_bar and total:
                progress_bar.update(downloaded, total)

        elif d['status'] == 'finished':
            if progress_bar:
                progress_bar.finish()
                progress_bar.__exit__(None, None, None)
                progress_bar = None

    return hook
