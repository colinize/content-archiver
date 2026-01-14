"""Main CLI entry point for the Content Archiver."""

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


@click.command()
@click.argument("url", required=False)
@click.option("--batch", "-b", type=click.Path(exists=True), help="Process URLs from a file")
@click.option("--yes", "-y", is_flag=True, help="Auto-confirm all prompts (download all items)")
@click.option("--resume", "-r", is_flag=True, help="Resume interrupted downloads")
@click.option("--status", "-s", is_flag=True, help="Show archive status")
@click.option("--output", "-o", type=click.Path(), help="Output directory")
@click.version_option(package_name="content-archiver")
def main(
    url: Optional[str],
    batch: Optional[str],
    yes: bool,
    resume: bool,
    status: bool,
    output: Optional[str],
) -> None:
    """
    Archive content from any URL.

    Just paste a URL and the archiver will detect what it is
    (YouTube, podcast, forum, article, or full website) and download it.

    \b
    Examples:
        archiver "https://youtube.com/watch?v=..."
        archiver "https://youtube.com/playlist?list=..."
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
        for i, batch_url in enumerate(urls, 1):
            print_info(f"\n[{i}/{len(urls)}] {batch_url}")
            archive_url(batch_url, output, db, auto_confirm=True)
        return

    # Handle single URL
    if not url:
        console.print(main.get_help(click.Context(main)))
        return

    archive_url(url, output, db, auto_confirm=yes)


def archive_url(url: str, output: Optional[str], db: Database, auto_confirm: bool = False) -> None:
    """Archive a single URL."""
    # Detect content type
    content_type = detect_content_type(url)
    source_name = get_source_name_from_url(url, content_type)

    print_info(f"Detected: [bold]{content_type.value.upper()}[/bold] - {source_name}")

    # Get output directory
    output_dir = Path(output) if output else get_output_dir()

    # Route to appropriate handler
    try:
        if content_type == ContentType.YOUTUBE:
            from .handlers.youtube import handle_youtube
            handle_youtube(url, output_dir, db, auto_confirm=auto_confirm)

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

    except ImportError as e:
        print_error(f"Handler not yet implemented: {e}")
    except Exception as e:
        print_error(f"Failed to archive: {e}")
        raise


if __name__ == "__main__":
    main()
