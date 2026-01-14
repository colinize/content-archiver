"""YouTube handler using yt-dlp."""

import json
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

from ..detector import detect_youtube_type
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


def handle_youtube(url: str, output_dir: Path, db: Database, auto_confirm: bool = False) -> None:
    """Handle YouTube URLs (videos, playlists, channels)."""
    if yt_dlp is None:
        print_error("yt-dlp is not installed. Please run: pip install yt-dlp")
        return

    youtube_type = detect_youtube_type(url)
    print_info(f"YouTube type: {youtube_type}")

    if youtube_type == "video":
        download_video(url, output_dir, db)
    elif youtube_type == "playlist":
        download_playlist(url, output_dir, db, auto_confirm=auto_confirm)
    elif youtube_type == "channel":
        download_channel(url, output_dir, db, auto_confirm=auto_confirm)


def download_video(url: str, output_dir: Path, db: Database) -> None:
    """Download a single YouTube video."""
    print_info("Fetching video info...")

    try:
        # Get video info first
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get('title', 'Unknown')
        channel = info.get('uploader', info.get('channel', 'Unknown'))
        duration = info.get('duration', 0)

        # Show info
        console.print(f"\n[bold]{title}[/bold]")
        console.print(f"Channel: {channel}")
        console.print(f"Duration: {duration // 60}:{duration % 60:02d}")

        # Create output folder
        source_folder = get_source_folder(output_dir, channel, category="videos")
        safe_title = sanitize_filename(title)

        # Track in database
        dl_id = db.add_download(
            url=url,
            content_type="youtube",
            source_name=channel,
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
            output_ext = 'mp4'
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
            output_ext = 'webm'  # Usually webm without merging

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Find the actual downloaded file
        for ext in ['mp4', 'webm', 'mkv']:
            potential_file = source_folder / f'{safe_title}.{ext}'
            if potential_file.exists():
                db.update_status(dl_id, "complete", str(potential_file))
                break
        else:
            db.update_status(dl_id, "complete", str(source_folder / f'{safe_title}.{output_ext}'))
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
    playlist_title: str,
    db: Database,
    progress_counter: Dict[str, int]
) -> Dict[str, Any]:
    """Download a single video from a playlist. Thread-safe."""
    video_url = f"https://youtube.com/watch?v={item['url']}" if not item['url'].startswith('http') else item['url']
    title = item['title']
    safe_title = sanitize_filename(f"{index:03d}_{title}")

    result = {"index": index, "title": title, "status": "unknown"}

    # Skip if already exists
    if _video_exists(source_folder, safe_title):
        with _progress_lock:
            progress_counter['skipped'] += 1
            current = progress_counter['completed'] + progress_counter['skipped'] + progress_counter['failed']
        result["status"] = "skipped"
        return result

    # Track in database
    dl_id = db.add_download(
        url=video_url,
        content_type="youtube",
        source_name=playlist_title,
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


def download_playlist(url: str, output_dir: Path, db: Database, auto_confirm: bool = False, max_workers: int = 3) -> None:
    """Download a YouTube playlist with concurrent downloads."""
    print_info("Fetching playlist info...")

    try:
        # Convert video+list URL to playlist-only URL for proper extraction
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(url)
        query = parse_qs(parsed.query)
        if 'list' in query:
            playlist_id = query['list'][0]
            playlist_url = f"https://www.youtube.com/playlist?list={playlist_id}"
        else:
            playlist_url = url

        # Get playlist info
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True}) as ydl:
            info = ydl.extract_info(playlist_url, download=False)

        playlist_title = info.get('title', 'Unknown Playlist')
        entries = info.get('entries', [])

        if not entries:
            print_warning("No videos found in playlist.")
            return

        # Build items list
        items = [
            {"title": e.get('title', 'Unknown'), "url": e.get('url', e.get('id'))}
            for e in entries if e
        ]

        # Show found items
        show_found_items("YouTube Playlist", playlist_title, items, "videos")

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
        source_folder = get_source_folder(output_dir, sanitize_filename(playlist_title), category="videos")

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
                    item, i, len(items), source_folder, playlist_title, db, progress_counter
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
        print_success(f"Playlist complete: {progress_counter['completed']} downloaded, "
                     f"{progress_counter['skipped']} skipped, {progress_counter['failed']} failed")

    except Exception as e:
        print_error(f"Failed to process playlist: {e}")


def _download_channel_video(
    item: Dict[str, Any],
    index: int,
    total: int,
    source_folder: Path,
    channel_name: str,
    db: Database,
    progress_counter: Dict[str, int]
) -> Dict[str, Any]:
    """Download a single video from a channel. Thread-safe."""
    video_url = f"https://youtube.com/watch?v={item['url']}" if not item['url'].startswith('http') else item['url']
    title = item['title']
    safe_title = sanitize_filename(title)

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
        content_type="youtube",
        source_name=channel_name,
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


def download_channel(url: str, output_dir: Path, db: Database, auto_confirm: bool = False, max_workers: int = 3) -> None:
    """Download videos from a YouTube channel with concurrent downloads."""
    print_info("Fetching channel info...")

    try:
        # Get channel videos
        with yt_dlp.YoutubeDL({'quiet': True, 'extract_flat': True, 'playlistend': 100}) as ydl:
            info = ydl.extract_info(url, download=False)

        channel_name = info.get('uploader', info.get('channel', info.get('title', 'Unknown')))
        entries = info.get('entries', [])

        if not entries:
            print_warning("No videos found on channel.")
            return

        # Build items list
        items = [
            {"title": e.get('title', 'Unknown'), "url": e.get('url', e.get('id'))}
            for e in entries if e
        ]

        # Show found items
        show_found_items("YouTube Channel", channel_name, items, "videos")

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
        source_folder = get_source_folder(output_dir, sanitize_filename(channel_name), category="videos")

        # Check how many already exist
        existing_count = sum(1 for item in items
                           if _video_exists(source_folder, sanitize_filename(item['title'])))

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
                    _download_channel_video,
                    item, i, len(items), source_folder, channel_name, db, progress_counter
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
        print_success(f"Channel complete: {progress_counter['completed']} downloaded, "
                     f"{progress_counter['skipped']} skipped, {progress_counter['failed']} failed")

    except Exception as e:
        print_error(f"Failed to process channel: {e}")


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
