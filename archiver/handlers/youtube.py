"""YouTube handler using yt-dlp."""

import json
import shutil
from pathlib import Path
from typing import Optional

try:
    import yt_dlp
except ImportError:
    yt_dlp = None

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


def download_playlist(url: str, output_dir: Path, db: Database, auto_confirm: bool = False) -> None:
    """Download a YouTube playlist."""
    print_info("Fetching playlist info...")

    try:
        # Convert video+list URL to playlist-only URL for proper extraction
        import re
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

        # Download each video
        print_info(f"Downloading {len(items)} videos...")

        for i, item in enumerate(items, 1):
            video_url = f"https://youtube.com/watch?v={item['url']}" if not item['url'].startswith('http') else item['url']
            title = item['title']

            console.print(f"\n[{i}/{len(items)}] {title}")

            dl_id = db.add_download(
                url=video_url,
                content_type="youtube",
                source_name=playlist_title,
                title=title
            )

            try:
                db.update_status(dl_id, "downloading")
                safe_title = sanitize_filename(f"{i:03d}_{title}")

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

                # Find actual file
                for ext in ['mp4', 'webm', 'mkv']:
                    if (source_folder / f'{safe_title}.{ext}').exists():
                        db.update_status(dl_id, "complete", str(source_folder / f'{safe_title}.{ext}'))
                        break
                print_success(f"Downloaded: {title}")

            except Exception as e:
                print_error(f"Failed: {e}")
                db.update_status(dl_id, "error", error_message=str(e))

        print_success(f"Playlist download complete: {playlist_title}")

    except Exception as e:
        print_error(f"Failed to process playlist: {e}")


def download_channel(url: str, output_dir: Path, db: Database, auto_confirm: bool = False) -> None:
    """Download videos from a YouTube channel."""
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

        # Download each video
        print_info(f"Downloading {len(items)} videos...")

        for i, item in enumerate(items, 1):
            video_url = f"https://youtube.com/watch?v={item['url']}" if not item['url'].startswith('http') else item['url']
            title = item['title']

            console.print(f"\n[{i}/{len(items)}] {title}")

            dl_id = db.add_download(
                url=video_url,
                content_type="youtube",
                source_name=channel_name,
                title=title
            )

            try:
                db.update_status(dl_id, "downloading")
                safe_title = sanitize_filename(title)

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

                # Find actual file
                for ext in ['mp4', 'webm', 'mkv']:
                    if (source_folder / f'{safe_title}.{ext}').exists():
                        db.update_status(dl_id, "complete", str(source_folder / f'{safe_title}.{ext}'))
                        break
                print_success(f"Downloaded: {title}")

            except Exception as e:
                print_error(f"Failed: {e}")
                db.update_status(dl_id, "error", error_message=str(e))

        print_success(f"Channel download complete: {channel_name}")

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
