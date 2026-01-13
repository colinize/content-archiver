"""Podcast handler for RSS feeds and audio webpage scanning."""

import re
import json
from pathlib import Path
from typing import Optional, List, Dict
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
import feedparser
from bs4 import BeautifulSoup

from ..detector import detect_podcast_type
from ..core.database import Database
from ..core.downloader import (
    sanitize_filename,
    get_source_folder,
    download_file,
    get_file_extension,
)
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


# Audio file extensions to look for
AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.wav', '.ogg', '.aac', '.wma', '.flac']
AUDIO_PATTERNS = [
    r'\.mp3',
    r'\.m4a',
    r'\.wav',
    r'\.ogg',
    r'\.aac',
]

# MIME types that indicate audio content
AUDIO_MIME_TYPES = [
    'audio/mpeg',
    'audio/mp3',
    'audio/mp4',
    'audio/x-m4a',
    'audio/wav',
    'audio/ogg',
    'audio/aac',
    'audio/x-wav',
    'application/octet-stream',  # Sometimes used for binary audio
]


def resolve_indirect_audio_links(potential_links: list, max_check: int = 50) -> set:
    """
    Follow potential audio links to find actual audio file URLs.

    Uses HEAD requests to check Content-Type without downloading the file.
    """
    resolved = set()

    # Limit how many we check to avoid hammering servers
    links_to_check = potential_links[:max_check]

    for link_url, link_text in links_to_check:
        try:
            # Use HEAD request to check content type without downloading
            head_response = requests.head(
                link_url,
                timeout=10,
                allow_redirects=True,
                headers={'User-Agent': 'ContentArchiver/1.0'}
            )

            content_type = head_response.headers.get('Content-Type', '').lower()
            final_url = head_response.url  # After redirects

            # Check if it's audio
            is_audio = (
                any(mime in content_type for mime in AUDIO_MIME_TYPES) or
                any(ext in final_url.lower() for ext in AUDIO_EXTENSIONS)
            )

            if is_audio:
                # Store the final URL (after redirects) along with the link text as title
                resolved.add((final_url, link_text))

        except requests.RequestException:
            # Skip links that fail
            continue

    # Return just the URLs (we'll handle titles separately)
    return {url for url, _ in resolved}


def handle_podcast(url: str, output_dir: Path, db: Database) -> None:
    """Handle podcast URLs (RSS feeds, platforms, webpages)."""
    podcast_type = detect_podcast_type(url)
    print_info(f"Podcast type: {podcast_type}")

    if podcast_type == "rss":
        handle_rss_feed(url, output_dir, db)
    elif podcast_type == "platform":
        handle_platform_url(url, output_dir, db)
    else:  # webpage
        handle_audio_webpage(url, output_dir, db)


def handle_rss_feed(url: str, output_dir: Path, db: Database) -> None:
    """Handle a podcast RSS feed."""
    print_info("Fetching RSS feed...")

    try:
        feed = feedparser.parse(url)

        if feed.bozo and not feed.entries:
            print_error(f"Failed to parse RSS feed: {feed.bozo_exception}")
            return

        podcast_title = feed.feed.get('title', 'Unknown Podcast')
        episodes = []

        for entry in feed.entries:
            # Find audio enclosure
            audio_url = None
            for enclosure in getattr(entry, 'enclosures', []):
                enc_type = enclosure.get('type', '')
                if enc_type.startswith('audio/') or any(ext in enclosure.get('href', '').lower() for ext in AUDIO_EXTENSIONS):
                    audio_url = enclosure.get('href')
                    break

            # Try links if no enclosure
            if not audio_url:
                for link in getattr(entry, 'links', []):
                    href = link.get('href', '')
                    if any(ext in href.lower() for ext in AUDIO_EXTENSIONS):
                        audio_url = href
                        break

            if audio_url:
                # Parse date
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    try:
                        published = datetime(*entry.published_parsed[:6]).strftime('%Y-%m-%d')
                    except:
                        pass

                episodes.append({
                    'title': entry.get('title', 'Unknown Episode'),
                    'url': audio_url,
                    'published': published,
                    'description': entry.get('summary', ''),
                })

        if not episodes:
            print_warning("No audio episodes found in feed.")
            return

        # Show found episodes
        show_found_items("Podcast", podcast_title, episodes, "episodes")

        # Confirm download
        choice = confirm_download(len(episodes), "episodes")
        if choice == "none":
            print_info("Download cancelled.")
            return

        if choice == "select":
            indices = select_items(episodes)
            episodes = [episodes[i] for i in indices]

        # Download episodes
        download_episodes(episodes, podcast_title, output_dir, db)

    except Exception as e:
        print_error(f"Failed to process RSS feed: {e}")


def handle_platform_url(url: str, output_dir: Path, db: Database) -> None:
    """Handle podcast platform URLs (Spotify, Apple, etc.)."""
    # For now, try to find an RSS feed or audio links on the page
    print_warning("Platform URL detected. Attempting to find audio files...")
    handle_audio_webpage(url, output_dir, db)


def handle_audio_webpage(url: str, output_dir: Path, db: Database) -> None:
    """Scan a webpage for audio file links, including indirect links."""
    print_info("Scanning page for audio files...")

    try:
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'ContentArchiver/1.0'
        })
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'lxml')

        # Extract page title for source name
        page_title = soup.title.string if soup.title else urlparse(url).netloc
        page_title = page_title.strip() if page_title else 'Unknown'

        # Find all audio file links
        audio_links = set()
        potential_audio_links = []  # Links that might lead to audio

        # Check all anchor tags
        for a in soup.find_all('a', href=True):
            href = a['href']
            full_url = urljoin(url, href)

            # Direct audio link
            if any(ext in href.lower() for ext in AUDIO_EXTENSIONS):
                audio_links.add(full_url)
            # Potential indirect link (showget.php, download.php, etc.)
            elif any(pattern in href.lower() for pattern in ['download', 'get', 'play', 'listen', 'episode', 'media']):
                # Get link text for title
                link_text = a.get_text(strip=True) or href.split('/')[-1]
                potential_audio_links.append((full_url, link_text))

        # Check source tags in audio elements
        for audio in soup.find_all('audio'):
            src = audio.get('src')
            if src:
                audio_links.add(urljoin(url, src))
            for source in audio.find_all('source'):
                src = source.get('src')
                if src:
                    audio_links.add(urljoin(url, src))

        # Also search the raw HTML for audio URLs (some sites use JavaScript)
        html_text = response.text
        for pattern in AUDIO_PATTERNS:
            matches = re.findall(r'https?://[^\s"\'<>]+' + pattern + r'[^\s"\'<>]*', html_text, re.IGNORECASE)
            audio_links.update(matches)

        # If we found potential indirect links but few direct ones, follow them
        if potential_audio_links and len(audio_links) < 5:
            print_info(f"Found {len(potential_audio_links)} potential audio links, checking them...")
            audio_links.update(resolve_indirect_audio_links(potential_audio_links))

        if not audio_links:
            print_warning("No audio files found on page.")
            return

        # Build episodes list
        episodes = []
        for audio_url in sorted(audio_links):
            # Try to extract title from URL
            filename = urlparse(audio_url).path.split('/')[-1]
            title = re.sub(r'\.[^.]+$', '', filename)  # Remove extension
            title = title.replace('_', ' ').replace('-', ' ').strip()

            episodes.append({
                'title': title or audio_url.split('/')[-1],
                'url': audio_url,
                'published': None,
            })

        # Show found episodes
        show_found_items("Audio Files", page_title, episodes, "audio files")

        # Confirm download
        choice = confirm_download(len(episodes), "audio files")
        if choice == "none":
            print_info("Download cancelled.")
            return

        if choice == "select":
            indices = select_items(episodes)
            episodes = [episodes[i] for i in indices]

        # Download episodes
        download_episodes(episodes, page_title, output_dir, db)

    except Exception as e:
        print_error(f"Failed to scan webpage: {e}")


def download_episodes(
    episodes: List[Dict],
    source_name: str,
    output_dir: Path,
    db: Database
) -> None:
    """Download a list of podcast episodes."""
    source_folder = get_source_folder(output_dir, sanitize_filename(source_name), category="podcasts")

    print_info(f"Downloading {len(episodes)} episodes to {source_folder}")

    # Save metadata
    metadata_path = source_folder / "index.json"
    metadata = {
        "source": source_name,
        "episodes": episodes,
        "downloaded_at": datetime.now().isoformat(),
    }
    metadata_path.write_text(json.dumps(metadata, indent=2))

    for i, episode in enumerate(episodes, 1):
        title = episode['title']
        audio_url = episode['url']
        published = episode.get('published', '')

        console.print(f"\n[{i}/{len(episodes)}] {title}")

        # Create filename
        if published:
            filename = f"{published}_{sanitize_filename(title)}"
        else:
            filename = f"{i:03d}_{sanitize_filename(title)}"

        # Guess extension
        ext = get_file_extension(audio_url)
        output_path = source_folder / f"{filename}{ext}"

        # Track in database
        dl_id = db.add_download(
            url=audio_url,
            content_type="podcast",
            source_name=source_name,
            title=title,
            metadata={"published": published}
        )

        try:
            db.update_status(dl_id, "downloading")

            # Download with progress
            with DownloadProgress() as progress:
                task = progress.start_task(title[:40], None)

                def update_progress(downloaded: int, total: int):
                    progress.update(downloaded, total)

                success = download_file(
                    audio_url,
                    output_path,
                    progress_callback=update_progress
                )

            if success:
                db.update_status(dl_id, "complete", str(output_path))
                print_success(f"Downloaded: {title}")

                # Try to add ID3 metadata
                try:
                    add_audio_metadata(output_path, title, source_name, published)
                except:
                    pass  # Metadata is optional
            else:
                db.update_status(dl_id, "error", error_message="Download failed")
                print_error(f"Failed to download: {title}")

        except Exception as e:
            db.update_status(dl_id, "error", error_message=str(e))
            print_error(f"Error: {e}")

    print_success(f"Podcast download complete: {source_name}")


def add_audio_metadata(
    path: Path,
    title: str,
    album: str,
    date: Optional[str] = None
) -> None:
    """Add ID3 metadata to an audio file."""
    try:
        from mutagen.mp3 import MP3
        from mutagen.id3 import ID3, TIT2, TALB, TDRC

        audio = MP3(str(path), ID3=ID3)
        audio.tags.add(TIT2(encoding=3, text=title))
        audio.tags.add(TALB(encoding=3, text=album))
        if date:
            audio.tags.add(TDRC(encoding=3, text=date[:4]))  # Year only
        audio.save()
    except:
        pass  # Non-MP3 or mutagen not available
