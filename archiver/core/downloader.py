"""Shared download logic."""

import requests
from pathlib import Path
from typing import Optional, Callable
import re
import unicodedata


def sanitize_filename(name: str, max_length: int = 100) -> str:
    """Sanitize a string to be safe for use as a filename."""
    # Normalize unicode characters
    name = unicodedata.normalize("NFKD", name)
    # Remove characters that aren't alphanumeric, spaces, hyphens, or underscores
    name = re.sub(r'[^\w\s\-.]', '', name)
    # Replace spaces with underscores
    name = re.sub(r'\s+', '_', name)
    # Remove leading/trailing underscores
    name = name.strip('_')
    # Truncate if too long
    if len(name) > max_length:
        name = name[:max_length]
    return name or "unnamed"


def download_file(
    url: str,
    output_path: Path,
    progress_callback: Optional[Callable[[int, int], None]] = None,
    chunk_size: int = 8192,
    headers: Optional[dict] = None,
    resume: bool = True
) -> bool:
    """
    Download a file with optional progress callback and resume support.

    Args:
        url: URL to download from
        output_path: Where to save the file
        progress_callback: Function called with (downloaded_bytes, total_bytes)
        chunk_size: Size of chunks to download
        headers: Additional headers to send
        resume: Whether to resume partial downloads

    Returns:
        True if download succeeded, False otherwise
    """
    # Ensure parent directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Check for existing partial download
    downloaded = 0
    if resume and output_path.exists():
        downloaded = output_path.stat().st_size

    # Set up headers
    req_headers = headers.copy() if headers else {}
    req_headers.setdefault("User-Agent", "ContentArchiver/1.0")

    if downloaded > 0:
        req_headers["Range"] = f"bytes={downloaded}-"

    try:
        response = requests.get(url, headers=req_headers, stream=True, timeout=30)

        # Check if server supports range requests
        if downloaded > 0 and response.status_code != 206:
            # Server doesn't support resume, start over
            downloaded = 0
            response = requests.get(url, headers=headers or {}, stream=True, timeout=30)

        response.raise_for_status()

        # Get total size
        total = int(response.headers.get("content-length", 0))
        if downloaded > 0:
            total += downloaded

        # Open file in append or write mode
        mode = "ab" if downloaded > 0 else "wb"
        with open(output_path, mode) as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if progress_callback:
                        progress_callback(downloaded, total)

        return True

    except requests.RequestException as e:
        return False


def get_source_folder(output_dir: Path, source_name: str, category: str = None) -> Path:
    """
    Get or create a folder for the source.

    Structure: output_dir / category / source_name
    Categories: videos, podcasts, forums, articles, websites
    """
    safe_name = sanitize_filename(source_name)

    if category:
        folder = output_dir / category / safe_name
    else:
        folder = output_dir / safe_name

    folder.mkdir(parents=True, exist_ok=True)
    return folder


def get_file_extension(url: str, content_type: Optional[str] = None) -> str:
    """Guess file extension from URL or content type."""
    # Try URL first
    url_lower = url.lower()
    for ext in ['.mp3', '.mp4', '.m4a', '.wav', '.ogg', '.webm', '.mkv', '.avi']:
        if ext in url_lower:
            return ext

    # Try content type
    if content_type:
        type_map = {
            'audio/mpeg': '.mp3',
            'audio/mp4': '.m4a',
            'audio/x-m4a': '.m4a',
            'audio/wav': '.wav',
            'audio/ogg': '.ogg',
            'video/mp4': '.mp4',
            'video/webm': '.webm',
        }
        for mime, ext in type_map.items():
            if mime in content_type:
                return ext

    # Default
    return '.mp3'
