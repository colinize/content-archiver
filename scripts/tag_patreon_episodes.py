#!/usr/bin/env python3
"""
Add ID3 metadata to Patreon podcast episodes using RSS feed data.

Usage:
    python tag_patreon_episodes.py <rss_url> <folder_path> [--rename]

Example:
    python tag_patreon_episodes.py "https://www.patreon.com/rss/kanedapinball?auth=XXX" ~/projects/content-archiver/podcasts/Kaneda/
"""

import sys
import re
import argparse
from pathlib import Path
from datetime import datetime

import feedparser
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TALB, TPE1, TDRC, TCON, COMM
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()


def sanitize_filename(name: str) -> str:
    """Sanitize a string to be safe for filenames."""
    # Remove or replace problematic characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name)
    return name.strip()[:200]  # Limit length


def extract_patreon_id(url: str) -> str:
    """Extract Patreon's numeric ID from an audio URL."""
    # URLs look like: https://c10.patreonusercontent.com/4/patreon-media/.../123456789.mp3
    match = re.search(r'/(\d{6,})\.mp3', url)
    if match:
        return match.group(1)
    # Try just the filename
    match = re.search(r'(\d{6,})', url.split('/')[-1])
    if match:
        return match.group(1)
    return None


def parse_rss_feed(rss_url: str) -> dict:
    """Parse RSS feed and return episode metadata keyed by Patreon ID."""
    console.print(f"[cyan]Fetching RSS feed...[/cyan]")

    feed = feedparser.parse(rss_url)

    if feed.bozo and not feed.entries:
        console.print(f"[red]Failed to parse RSS feed: {feed.bozo_exception}[/red]")
        return {}, None

    podcast_title = feed.feed.get('title', 'Unknown Podcast')
    podcast_author = feed.feed.get('author', feed.feed.get('itunes_author', ''))

    console.print(f"[green]Found podcast: {podcast_title}[/green]")
    console.print(f"[dim]Author: {podcast_author}[/dim]")

    episodes = {}

    for entry in feed.entries:
        # Find audio enclosure
        audio_url = None
        for enclosure in getattr(entry, 'enclosures', []):
            enc_type = enclosure.get('type', '')
            if enc_type.startswith('audio/') or '.mp3' in enclosure.get('href', '').lower():
                audio_url = enclosure.get('href')
                break

        if not audio_url:
            continue

        patreon_id = extract_patreon_id(audio_url)
        if not patreon_id:
            continue

        # Parse date
        published = None
        if hasattr(entry, 'published_parsed') and entry.published_parsed:
            try:
                published = datetime(*entry.published_parsed[:6])
            except:
                pass

        episodes[patreon_id] = {
            'title': entry.get('title', 'Unknown Episode'),
            'published': published,
            'description': entry.get('summary', ''),
            'url': audio_url,
            'podcast_title': podcast_title,
            'podcast_author': podcast_author,
        }

    console.print(f"[green]Found {len(episodes)} episodes with audio[/green]")
    return episodes, podcast_title


def add_id3_tags(file_path: Path, metadata: dict) -> bool:
    """Add ID3 tags to an MP3 file."""
    try:
        audio = MP3(str(file_path))

        # Create ID3 tags if they don't exist
        if audio.tags is None:
            audio.add_tags()

        # Title
        audio.tags.add(TIT2(encoding=3, text=metadata['title']))

        # Album (podcast name)
        audio.tags.add(TALB(encoding=3, text=metadata['podcast_title']))

        # Artist
        if metadata.get('podcast_author'):
            audio.tags.add(TPE1(encoding=3, text=metadata['podcast_author']))

        # Year/Date
        if metadata.get('published'):
            audio.tags.add(TDRC(encoding=3, text=metadata['published'].strftime('%Y-%m-%d')))

        # Genre
        audio.tags.add(TCON(encoding=3, text='Podcast'))

        # Comment (description snippet)
        if metadata.get('description'):
            desc = metadata['description'][:500]  # Truncate long descriptions
            audio.tags.add(COMM(encoding=3, lang='eng', desc='', text=desc))

        audio.save()
        return True

    except Exception as e:
        console.print(f"[red]Failed to tag {file_path.name}: {e}[/red]")
        return False


def main():
    parser = argparse.ArgumentParser(description='Add ID3 metadata to Patreon podcast episodes')
    parser.add_argument('rss_url', help='Patreon RSS feed URL')
    parser.add_argument('folder', help='Folder containing downloaded MP3 files')
    parser.add_argument('--rename', action='store_true', help='Rename files to include episode title')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')

    args = parser.parse_args()

    folder = Path(args.folder).expanduser()
    if not folder.exists():
        console.print(f"[red]Folder not found: {folder}[/red]")
        sys.exit(1)

    # Parse RSS feed
    episodes, podcast_title = parse_rss_feed(args.rss_url)
    if not episodes:
        console.print("[red]No episodes found in RSS feed[/red]")
        sys.exit(1)

    # Find MP3 files in folder
    mp3_files = list(folder.glob('*.mp3'))
    console.print(f"[cyan]Found {len(mp3_files)} MP3 files in folder[/cyan]")

    # Match files to episodes
    matched = 0
    unmatched = []
    tagged = 0
    renamed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("Processing files...", total=len(mp3_files))

        for mp3_file in mp3_files:
            progress.update(task, advance=1)

            # Extract ID from filename
            file_id = re.search(r'(\d{6,})', mp3_file.stem)
            if not file_id:
                unmatched.append(mp3_file.name)
                continue

            file_id = file_id.group(1)

            if file_id not in episodes:
                unmatched.append(mp3_file.name)
                continue

            matched += 1
            metadata = episodes[file_id]

            if args.dry_run:
                console.print(f"[dim]Would tag: {mp3_file.name} → {metadata['title'][:60]}...[/dim]")
                if args.rename:
                    new_name = build_filename(metadata, mp3_file.suffix)
                    console.print(f"[dim]Would rename to: {new_name}[/dim]")
                continue

            # Add ID3 tags
            if add_id3_tags(mp3_file, metadata):
                tagged += 1

            # Rename file if requested
            if args.rename:
                new_name = build_filename(metadata, mp3_file.suffix)
                new_path = mp3_file.parent / new_name

                if new_path != mp3_file and not new_path.exists():
                    mp3_file.rename(new_path)
                    renamed += 1

    # Summary
    console.print()
    console.print(f"[green]✓ Matched: {matched}/{len(mp3_files)} files[/green]")
    if not args.dry_run:
        console.print(f"[green]✓ Tagged: {tagged} files[/green]")
        if args.rename:
            console.print(f"[green]✓ Renamed: {renamed} files[/green]")

    if unmatched:
        console.print(f"[yellow]⚠ Unmatched: {len(unmatched)} files[/yellow]")
        if len(unmatched) <= 10:
            for name in unmatched:
                console.print(f"[dim]  - {name}[/dim]")


def build_filename(metadata: dict, ext: str) -> str:
    """Build a filename from episode metadata."""
    date_str = metadata['published'].strftime('%Y-%m-%d') if metadata.get('published') else ''
    title = sanitize_filename(metadata['title'])

    if date_str:
        return f"{date_str}_{title}{ext}"
    return f"{title}{ext}"


if __name__ == '__main__':
    main()
