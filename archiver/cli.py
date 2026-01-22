"""Main CLI entry point for the Content Archiver."""

import subprocess
import sys
import click
from pathlib import Path
from typing import Optional

from .detector import detect_content_type, ContentType, get_source_name_from_url
from .core.config import get_output_dir, ensure_dirs
from .core.database import Database
from .core.progress import (
    console,
    print_info,
    print_error,
    print_success,
    print_warning,
    show_status,
)

# Path to media-transcriber
TRANSCRIBER_PATH = Path.home() / "projects" / "media-transcriber"
TRANSCRIBER_SCRIPT = TRANSCRIBER_PATH / "transcriber.py"
TRANSCRIBER_VENV = TRANSCRIBER_PATH / "venv" / "bin" / "python"


@click.command()
@click.argument("url", required=False)
@click.option("--batch", "-b", type=click.Path(exists=True), help="Process URLs from a file")
@click.option("--yes", "-y", is_flag=True, help="Auto-confirm all prompts (download all items)")
@click.option("--resume", "-r", is_flag=True, help="Resume interrupted downloads")
@click.option("--status", "-s", is_flag=True, help="Show archive status")
@click.option("--check", is_flag=True, help="Check if URL is already archived")
@click.option("--output", "-o", type=click.Path(), help="Output directory")
@click.option("--cookies-from-browser", "-c", type=str, help="Browser to extract cookies from (chrome, firefox, safari, edge)")
@click.option("--transcribe", "-t", is_flag=True, help="Transcribe downloaded audio/video files")
@click.option("--transcribe-model", type=str, default="large-v3", help="Whisper model for transcription (default: large-v3)")
@click.version_option(package_name="content-archiver")
def main(
    url: Optional[str],
    batch: Optional[str],
    yes: bool,
    resume: bool,
    status: bool,
    check: bool,
    output: Optional[str],
    cookies_from_browser: Optional[str],
    transcribe: bool,
    transcribe_model: str,
) -> None:
    """
    Archive content from any URL.

    Just paste a URL and the archiver will detect what it is
    (YouTube, podcast, forum, article, or full website) and download it.

    \b
    Examples:
        archiver "https://youtube.com/watch?v=..."
        archiver "https://youtube.com/playlist?list=..."
        archiver "https://facebook.com/PageName/videos/"
        archiver "https://podcast.example.com/feed.xml"
        archiver "https://reddit.com/r/.../comments/..."
        archiver "https://blog.example.com/post-title"

    \b
    Options:
        archiver --batch urls.txt    # Process multiple URLs from file
        archiver --resume            # Resume interrupted downloads
        archiver --status            # Show download history
    """
    ensure_dirs()
    db = Database()

    # Handle --status flag
    if status:
        stats = db.get_stats()
        downloads = db.get_all()
        show_status(stats, downloads)
        return

    # Handle --check flag
    if check:
        if not url:
            print_error("--check requires a URL argument")
            return
        archived_info = db.get_archived_info(url)
        if archived_info:
            print_success(f"ARCHIVED: {url}")
            print_info(f"  Title: {archived_info.title}")
            print_info(f"  Source: {archived_info.source_name}")
            print_info(f"  Type: {archived_info.content_type}")
            print_info(f"  Status: {archived_info.status}")
            print_info(f"  Archived: {archived_info.created_at[:10]}")
            if archived_info.local_path:
                print_info(f"  Path: {archived_info.local_path}")
        else:
            print_warning(f"NOT ARCHIVED: {url}")
        return

    # Handle --resume flag
    if resume:
        pending = db.get_pending()
        if not pending:
            print_info("No pending downloads to resume.")
            return

        print_info(f"Found {len(pending)} pending downloads.")
        for dl in pending:
            print_info(f"Resuming: {dl.title or dl.url}")
            # Re-run the archiver for each pending URL
            archive_url(dl.url, output, db)
        return

    # Handle --batch flag
    if batch:
        batch_path = Path(batch)
        # Skip empty lines and comments (lines starting with #)
        urls = [
            line.strip() for line in batch_path.read_text().splitlines()
            if line.strip() and not line.strip().startswith('#')
        ]
        if not urls:
            print_error("No URLs found in batch file.")
            return

        print_info(f"Processing {len(urls)} URLs from batch file...")
        # Auto-confirm in batch mode
        folders_to_transcribe = []
        for i, batch_url in enumerate(urls, 1):
            print_info(f"\n[{i}/{len(urls)}] {batch_url}")
            result_folder = archive_url(batch_url, output, db, auto_confirm=True, cookies_from_browser=cookies_from_browser)
            if result_folder and transcribe:
                folders_to_transcribe.append(result_folder)

        # Transcribe all downloaded content
        if transcribe and folders_to_transcribe:
            print_info("\n--- Starting transcription ---")
            for folder in set(folders_to_transcribe):  # Dedupe folders
                if folder.exists():
                    run_transcription(folder, transcribe_model)
        return

    # Handle single URL
    if not url:
        console.print(main.get_help(click.Context(main)))
        return

    result_folder = archive_url(url, output, db, auto_confirm=yes, cookies_from_browser=cookies_from_browser)

    # Transcribe if requested
    if transcribe and result_folder and result_folder.exists():
        print_info("\n--- Starting transcription ---")
        run_transcription(result_folder, transcribe_model)


def run_transcription(folder: Path, model: str = "large-v3") -> None:
    """Run transcription on media files in a folder."""
    if not TRANSCRIBER_SCRIPT.exists():
        print_warning(f"Transcriber not found at {TRANSCRIBER_SCRIPT}")
        print_warning("Install media-transcriber to ~/projects/media-transcriber")
        return

    if not TRANSCRIBER_VENV.exists():
        print_warning(f"Transcriber venv not found at {TRANSCRIBER_VENV}")
        return

    # Check for media files
    media_extensions = {'.mp3', '.mp4', '.m4a', '.wav', '.mkv', '.mov', '.avi', '.webm'}
    media_files = [f for f in folder.iterdir() if f.suffix.lower() in media_extensions]

    if not media_files:
        print_info("No media files to transcribe.")
        return

    print_info(f"Transcribing {len(media_files)} media file(s)...")

    try:
        result = subprocess.run(
            [str(TRANSCRIBER_VENV), str(TRANSCRIBER_SCRIPT), str(folder), "--model", model],
            cwd=str(TRANSCRIBER_PATH),
            capture_output=False,
        )
        if result.returncode == 0:
            print_success("Transcription complete!")
        else:
            print_warning("Transcription finished with errors")
    except Exception as e:
        print_error(f"Transcription failed: {e}")


def archive_url(url: str, output: Optional[str], db: Database, auto_confirm: bool = False, cookies_from_browser: Optional[str] = None) -> Optional[Path]:
    """Archive a single URL. Returns the output folder path if successful."""
    # Detect content type
    content_type = detect_content_type(url)
    source_name = get_source_name_from_url(url, content_type)

    print_info(f"Detected: [bold]{content_type.value.upper()}[/bold] - {source_name}")

    # Get output directory
    output_dir = Path(output) if output else get_output_dir()

    # Determine content-specific output folder
    content_folder_map = {
        ContentType.YOUTUBE: "videos",
        ContentType.FACEBOOK: "videos",
        ContentType.PODCAST: "podcasts",
        ContentType.FORUM: "forums",
        ContentType.ARTICLE: "articles",
        ContentType.SITE: "websites",
    }
    content_folder = content_folder_map.get(content_type, "articles")
    download_folder = output_dir / content_folder / source_name

    # Route to appropriate handler
    try:
        if content_type == ContentType.YOUTUBE:
            from .handlers.youtube import handle_youtube
            handle_youtube(url, output_dir, db, auto_confirm=auto_confirm, cookies_from_browser=cookies_from_browser)

        elif content_type == ContentType.FACEBOOK:
            from .handlers.facebook import handle_facebook
            handle_facebook(url, output_dir, db, auto_confirm=auto_confirm, cookies_from_browser=cookies_from_browser)

        elif content_type == ContentType.PODCAST:
            from .handlers.podcast import handle_podcast
            handle_podcast(url, output_dir, db, auto_confirm=auto_confirm)

        elif content_type == ContentType.FORUM:
            from .handlers.forum import handle_forum
            handle_forum(url, output_dir, db)

        elif content_type == ContentType.ARTICLE:
            from .handlers.article import handle_article
            handle_article(url, output_dir, db, auto_confirm=auto_confirm)

        elif content_type == ContentType.SITE:
            from .handlers.site import handle_site
            handle_site(url, output_dir, db)

        else:
            print_warning(f"Unknown content type. Trying as article...")
            from .handlers.article import handle_article
            handle_article(url, output_dir, db, auto_confirm=auto_confirm)

        return download_folder

    except ImportError as e:
        print_error(f"Handler not yet implemented: {e}")
        return None
    except Exception as e:
        print_error(f"Failed to archive: {e}")
        raise


if __name__ == "__main__":
    main()
