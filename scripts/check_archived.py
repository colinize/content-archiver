#!/usr/bin/env python3
"""Check if URLs or sources are already archived.

Query the manifest and database to check if content has been archived.
Useful for automation - pipe in URLs and get back only new ones.
"""

import argparse
import json
import sqlite3
import sys
from pathlib import Path


def load_manifest(archive_root: Path) -> dict | None:
    """Load the master manifest if it exists."""
    manifest_path = archive_root / ".archiver" / "manifest.json"
    if manifest_path.exists():
        with open(manifest_path) as f:
            return json.load(f)
    return None


def check_url_in_db(db_path: Path, url: str) -> dict | None:
    """Check if a URL exists in the database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    row = conn.execute("""
        SELECT id, url, content_type, source_name, title, status, local_path, created_at
        FROM downloads
        WHERE url = ?
    """, (url,)).fetchone()

    conn.close()

    if row:
        return dict(row)
    return None


def check_source_in_manifest(manifest: dict, source_name: str) -> dict | None:
    """Check if a source exists in the manifest (fuzzy match)."""
    source_lower = source_name.lower()

    for source in manifest.get("sources", []):
        if source_lower in source["source_name"].lower():
            return source
        if source_lower in source["id"].lower():
            return source

    return None


def format_archive_info(db_record: dict | None, manifest_source: dict | None) -> str:
    """Format archive information for display."""
    lines = []

    if db_record:
        lines.append(f"  Status: {db_record['status']}")
        lines.append(f"  Title: {db_record['title']}")
        lines.append(f"  Source: {db_record['source_name']}")
        lines.append(f"  Type: {db_record['content_type']}")
        lines.append(f"  Archived: {db_record['created_at'][:10]}")
        if db_record['local_path']:
            lines.append(f"  Path: {db_record['local_path']}")

    if manifest_source:
        storage = manifest_source.get('storage_status', 'local')
        lines.append(f"  Storage: {storage}")
        if storage == 'external' and manifest_source.get('external_location'):
            lines.append(f"  External: {manifest_source['external_location']}")

    return "\n".join(lines)


def check_single_url(
    url: str,
    archive_root: Path,
    db_path: Path,
    quiet: bool = False
) -> bool:
    """Check a single URL. Returns True if archived."""
    manifest = load_manifest(archive_root)
    db_record = check_url_in_db(db_path, url)

    if db_record:
        if quiet:
            return True

        # Find manifest source for storage info
        manifest_source = None
        if manifest:
            for source in manifest.get("sources", []):
                if source["source_name"] == db_record["source_name"]:
                    manifest_source = source
                    break

        print(f"ARCHIVED: {url}")
        print(format_archive_info(db_record, manifest_source))
        return True
    else:
        if not quiet:
            print(f"NOT ARCHIVED: {url}")
        return False


def check_source(
    source_name: str,
    archive_root: Path,
    db_path: Path
) -> bool:
    """Check if a source exists."""
    manifest = load_manifest(archive_root)

    if not manifest:
        print("Manifest not found. Run generate_manifest.py first.")
        return False

    source = check_source_in_manifest(manifest, source_name)

    if source:
        print(f"FOUND: {source['source_name']}")
        print(f"  ID: {source['id']}")
        print(f"  Type: {source['content_type']}")
        print(f"  Items: {source['item_count']}")
        print(f"  Folder: {source['folder_path']}")
        print(f"  Storage: {source.get('storage_status', 'local')}")
        if source.get('external_location'):
            print(f"  External: {source['external_location']}")
        return True
    else:
        print(f"NOT FOUND: {source_name}")
        return False


def batch_check_urls(
    urls: list[str],
    archive_root: Path,
    db_path: Path,
    output_new: bool = False
) -> None:
    """Check multiple URLs. Optionally output only new ones."""
    archived = 0
    new_urls = []

    for url in urls:
        url = url.strip()
        if not url:
            continue

        db_record = check_url_in_db(db_path, url)
        if db_record:
            archived += 1
        else:
            new_urls.append(url)

    if output_new:
        # Output only new URLs (for piping to archiver)
        for url in new_urls:
            print(url)
    else:
        # Summary output
        print(f"Total URLs: {len(urls)}")
        print(f"Already archived: {archived}")
        print(f"New: {len(new_urls)}")

        if new_urls:
            print("\nNew URLs:")
            for url in new_urls:
                print(f"  {url}")


def list_sources(archive_root: Path, content_type: str | None = None) -> None:
    """List all sources in the manifest."""
    manifest = load_manifest(archive_root)

    if not manifest:
        print("Manifest not found. Run generate_manifest.py first.")
        return

    sources = manifest.get("sources", [])

    if content_type:
        sources = [s for s in sources if s["content_type"] == content_type]

    print(f"Sources ({len(sources)}):\n")

    # Group by content type
    by_type = {}
    for source in sources:
        ct = source["content_type"]
        if ct not in by_type:
            by_type[ct] = []
        by_type[ct].append(source)

    for ct in sorted(by_type.keys()):
        print(f"{ct.upper()} ({len(by_type[ct])} sources):")
        for source in sorted(by_type[ct], key=lambda x: -x["item_count"]):
            storage = source.get("storage_status", "local")
            storage_marker = " [external]" if storage == "external" else ""
            print(f"  {source['source_name']} ({source['item_count']} items){storage_marker}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description="Check if URLs or sources are already archived"
    )
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=Path.home() / "projects" / "content-archiver",
        help="Root directory for the archive"
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="Path to database file"
    )
    parser.add_argument(
        "url",
        nargs="?",
        help="URL to check"
    )
    parser.add_argument(
        "--source",
        help="Check if a source exists by name"
    )
    parser.add_argument(
        "--file",
        type=Path,
        help="File containing URLs to check (one per line)"
    )
    parser.add_argument(
        "--new-only",
        action="store_true",
        help="Output only new (non-archived) URLs"
    )
    parser.add_argument(
        "--quiet", "-q",
        action="store_true",
        help="Quiet mode - exit code only"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all sources in manifest"
    )
    parser.add_argument(
        "--type",
        choices=["podcast", "youtube", "article", "site", "forum"],
        help="Filter --list by content type"
    )

    args = parser.parse_args()

    db_path = args.db or (args.archive_root / ".archiver" / "archive.db")

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return 1

    # List mode
    if args.list:
        list_sources(args.archive_root, args.type)
        return 0

    # Source check mode
    if args.source:
        found = check_source(args.source, args.archive_root, db_path)
        return 0 if found else 1

    # Batch file mode
    if args.file:
        if not args.file.exists():
            print(f"Error: File not found: {args.file}")
            return 1
        with open(args.file) as f:
            urls = [line.strip() for line in f if line.strip()]
        batch_check_urls(urls, args.archive_root, db_path, args.new_only)
        return 0

    # Stdin batch mode
    if not sys.stdin.isatty() and not args.url:
        urls = [line.strip() for line in sys.stdin if line.strip()]
        batch_check_urls(urls, args.archive_root, db_path, args.new_only)
        return 0

    # Single URL mode
    if args.url:
        archived = check_single_url(args.url, args.archive_root, db_path, args.quiet)
        return 0 if archived else 1

    parser.print_help()
    print("\nExamples:")
    print("  Single URL:   python check_archived.py https://example.com/video")
    print("  Source:       python check_archived.py --source 'Kaneda'")
    print("  List:         python check_archived.py --list")
    print("  Batch file:   python check_archived.py --file urls.txt")
    print("  New only:     python check_archived.py --file urls.txt --new-only")
    print("  Pipe:         cat urls.txt | python check_archived.py --new-only")
    return 1


if __name__ == "__main__":
    exit(main())
