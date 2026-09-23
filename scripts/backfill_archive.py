#!/usr/bin/env python3
"""Backfill the archive database from files on external drive.

Scans the external drive's folder structure and registers existing files
in the downloads table. This is useful when files exist but the database
is empty or out of sync.

Usage:
    python3 scripts/backfill_archive.py
    python3 scripts/backfill_archive.py --dry-run
    python3 scripts/backfill_archive.py --type podcast
    python3 scripts/backfill_archive.py --external-root /Volumes/MyDrive
"""

from __future__ import annotations

import argparse
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

# Default external drive path
DEFAULT_EXTERNAL_ROOT = Path("/Volumes/My Passport for Mac/Pinball Media Archive")

# Map folder names to content types
FOLDER_TO_CONTENT_TYPE = {
    "podcasts": "podcast",
    "videos": "youtube",
    "articles": "article",
    "websites": "site",
    "forums": "forum",
}

# Media file extensions by content type
MEDIA_EXTENSIONS = {
    "podcast": {".mp3", ".m4a", ".ogg", ".wav", ".flac"},
    "youtube": {".mp4", ".mkv", ".webm", ".mov", ".avi"},
    "article": {".md", ".html"},
    "site": {".md", ".html"},
    "forum": {".md", ".html"},
}


def get_database_path() -> Path:
    """Get the path to the archive database."""
    return Path(__file__).parent.parent / ".archiver" / "archive.db"


def sanitize_source_name(folder_name: str) -> str:
    """Convert folder name back to readable source name."""
    # Replace underscores with spaces (common sanitization)
    name = folder_name.replace("_", " ")
    # Handle common patterns
    name = name.replace(" - ", " – ")  # Restore en-dash
    return name.strip()


def generate_placeholder_url(content_type: str, source_name: str, title: str) -> str:
    """Generate a placeholder URL for files without known URLs.

    Format: local://{content_type}/{source_name}/{title}
    This allows us to track files while acknowledging we don't have the original URL.
    """
    # Sanitize for URL
    safe_source = source_name.replace(" ", "_")
    safe_title = title.replace(" ", "_")
    return f"local://{content_type}/{safe_source}/{safe_title}"


def get_file_metadata(file_path: Path) -> dict:
    """Extract metadata from a file."""
    stat = file_path.stat()
    return {
        "file_path": str(file_path),
        "file_size": stat.st_size,
        "modified_time": datetime.fromtimestamp(stat.st_mtime).isoformat(),
        "created_time": datetime.fromtimestamp(stat.st_ctime).isoformat(),
    }


def scan_external_drive(
    external_root: Path,
    content_type_filter: Optional[str] = None
) -> list[dict]:
    """Scan the external drive and return file info."""
    files = []

    for folder_name, content_type in FOLDER_TO_CONTENT_TYPE.items():
        if content_type_filter and content_type != content_type_filter:
            continue

        folder_path = external_root / folder_name
        if not folder_path.exists():
            print(f"  Skipping {folder_name}/ (not found)")
            continue

        print(f"  Scanning {folder_name}/...")
        valid_extensions = MEDIA_EXTENSIONS.get(content_type, set())

        # Each subfolder is a source
        for source_folder in folder_path.iterdir():
            if not source_folder.is_dir():
                continue
            if source_folder.name.startswith("."):
                continue

            source_name = sanitize_source_name(source_folder.name)

            # Scan for media files
            for file_path in source_folder.rglob("*"):
                if not file_path.is_file():
                    continue
                if file_path.suffix.lower() not in valid_extensions:
                    continue
                if file_path.name.startswith("."):
                    continue
                # Skip index files
                if file_path.name == "_index.json":
                    continue

                # Extract title from filename
                title = file_path.stem

                files.append({
                    "content_type": content_type,
                    "source_name": source_name,
                    "title": title,
                    "file_path": file_path,
                    "folder_name": folder_name,
                })

    return files


def backfill_database(
    files: list[dict],
    db_path: Path,
    dry_run: bool = False
) -> tuple[int, int]:
    """Insert files into the database.

    Returns (inserted_count, skipped_count).
    """
    inserted = 0
    skipped = 0

    if dry_run:
        # Just count what would be inserted
        for f in files:
            print(f"  Would insert: {f['content_type']}/{f['source_name']}/{f['title']}")
            inserted += 1
        return inserted, skipped

    # Connect to database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    now = datetime.now().isoformat()

    for f in files:
        url = generate_placeholder_url(f["content_type"], f["source_name"], f["title"])

        # Check if already exists
        cursor.execute(
            "SELECT id FROM downloads WHERE url = ? AND title = ?",
            (url, f["title"])
        )
        if cursor.fetchone():
            skipped += 1
            continue

        # Get file metadata
        metadata = get_file_metadata(f["file_path"])

        try:
            cursor.execute("""
                INSERT INTO downloads
                (url, content_type, source_name, title, status, local_path,
                 file_size, created_at, updated_at, metadata)
                VALUES (?, ?, ?, ?, 'complete', ?, ?, ?, ?, ?)
            """, (
                url,
                f["content_type"],
                f["source_name"],
                f["title"],
                str(f["file_path"]),
                metadata["file_size"],
                now,
                now,
                json.dumps(metadata),
            ))
            inserted += 1
        except sqlite3.IntegrityError as e:
            print(f"  Skipped (duplicate): {f['title']}")
            skipped += 1

    conn.commit()
    conn.close()

    return inserted, skipped


def main():
    parser = argparse.ArgumentParser(
        description="Backfill archive database from external drive files"
    )
    parser.add_argument(
        "--external-root",
        type=Path,
        default=DEFAULT_EXTERNAL_ROOT,
        help="Path to external drive archive root"
    )
    parser.add_argument(
        "--type",
        choices=["podcast", "youtube", "article", "site", "forum"],
        help="Only process specific content type"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be inserted without making changes"
    )
    args = parser.parse_args()

    external_root = args.external_root
    db_path = get_database_path()

    print(f"External drive: {external_root}")
    print(f"Database: {db_path}")

    if not external_root.exists():
        print(f"\nError: External drive not found at {external_root}")
        print("Please mount the drive and try again.")
        return 1

    if not db_path.exists():
        print(f"\nError: Database not found at {db_path}")
        print("Please run the archiver once to initialize the database.")
        return 1

    if args.dry_run:
        print("\n[DRY RUN] No changes will be made\n")

    # Scan external drive
    print("\nScanning external drive...")
    files = scan_external_drive(external_root, args.type)
    print(f"\nFound {len(files)} media files")

    if not files:
        print("No files to process.")
        return 0

    # Group by content type for summary
    by_type = {}
    for f in files:
        ct = f["content_type"]
        by_type[ct] = by_type.get(ct, 0) + 1

    print("\nBy type:")
    for ct, count in sorted(by_type.items()):
        print(f"  {ct}: {count}")

    # Backfill database
    print("\nBackfilling database...")
    inserted, skipped = backfill_database(files, db_path, args.dry_run)

    print(f"\nResults:")
    print(f"  Inserted: {inserted}")
    print(f"  Skipped (duplicates): {skipped}")

    return 0


if __name__ == "__main__":
    exit(main())
