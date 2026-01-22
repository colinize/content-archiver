#!/usr/bin/env python3
"""Generate manifest and placeholder folders from the archive database.

Creates:
- .archiver/manifest.json - Master index of all sources
- {category}/{source}/_index.json - Per-folder indices
- Optionally mirrors folder structure to external drive
"""

import argparse
import json
import re
import sqlite3
from datetime import datetime
from pathlib import Path


# Content type to folder mapping
CONTENT_TYPE_FOLDERS = {
    "podcast": "podcasts",
    "youtube": "videos",
    "article": "articles",
    "site": "websites",
    "forum": "forums",
}


def sanitize_folder_name(name: str) -> str:
    """Convert a source name to a valid folder name."""
    # Replace problematic characters with underscores
    sanitized = re.sub(r'[<>:"/\\|?*]', '_', name)
    # Replace spaces and multiple underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    sanitized = re.sub(r'_+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    return sanitized


def get_source_id(content_type: str, source_name: str) -> str:
    """Generate a unique source ID."""
    safe_name = sanitize_folder_name(source_name).lower()
    return f"{content_type}-{safe_name}"


def get_sources_from_db(db_path: Path) -> list[dict]:
    """Query database for all sources with aggregated data."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    # Get source-level summary
    sources = conn.execute("""
        SELECT
            content_type,
            source_name,
            COUNT(*) as item_count,
            MIN(created_at) as first_archived,
            MAX(updated_at) as last_updated
        FROM downloads
        GROUP BY content_type, source_name
        ORDER BY content_type, item_count DESC
    """).fetchall()

    result = []
    for row in sources:
        source_data = {
            "content_type": row["content_type"],
            "source_name": row["source_name"],
            "item_count": row["item_count"],
            "first_archived": row["first_archived"][:10] if row["first_archived"] else None,
            "last_updated": row["last_updated"][:10] if row["last_updated"] else None,
        }
        result.append(source_data)

    conn.close()
    return result


def get_items_for_source(db_path: Path, content_type: str, source_name: str) -> list[dict]:
    """Get all items for a specific source."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    items = conn.execute("""
        SELECT url, title, local_path, status, created_at, metadata
        FROM downloads
        WHERE content_type = ? AND source_name = ?
        ORDER BY title
    """, (content_type, source_name)).fetchall()

    result = []
    for row in items:
        # Extract filename from local_path if present
        filename = None
        if row["local_path"]:
            filename = Path(row["local_path"]).name

        item_data = {
            "url": row["url"],
            "title": row["title"],
            "filename": filename,
            "status": row["status"],
            "downloaded_at": row["created_at"][:10] if row["created_at"] else None,
        }
        result.append(item_data)

    conn.close()
    return result


def create_folder_index(
    source_id: str,
    source_name: str,
    content_type: str,
    items: list[dict],
    storage_status: str = "local"
) -> dict:
    """Create a per-folder _index.json structure."""
    return {
        "source_id": source_id,
        "source_name": source_name,
        "content_type": content_type,
        "storage_status": storage_status,
        "item_count": len(items),
        "items": items,
    }


def create_master_manifest(
    sources: list[dict],
    archive_root: Path,
    external_root: Path | None = None
) -> dict:
    """Create the master manifest.json structure."""
    # Calculate summary stats
    by_type = {}
    total_items = 0
    for source in sources:
        ct = source["content_type"]
        by_type[ct] = by_type.get(ct, 0) + source["item_count"]
        total_items += source["item_count"]

    manifest = {
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "archive_root": str(archive_root),
        "external_root": str(external_root) if external_root else None,
        "summary": {
            "total_sources": len(sources),
            "total_items": total_items,
            "by_type": by_type,
        },
        "sources": [],
    }

    for source in sources:
        folder_name = CONTENT_TYPE_FOLDERS.get(source["content_type"], source["content_type"])
        source_folder = sanitize_folder_name(source["source_name"])

        source_entry = {
            "id": get_source_id(source["content_type"], source["source_name"]),
            "content_type": source["content_type"],
            "source_name": source["source_name"],
            "folder_path": f"{folder_name}/{source_folder}",
            "item_count": source["item_count"],
            "storage_status": "local",  # Default, updated by mark_external.py
            "external_location": None,
            "first_archived": source["first_archived"],
            "last_updated": source["last_updated"],
        }
        manifest["sources"].append(source_entry)

    return manifest


def generate_manifest(
    archive_root: Path,
    db_path: Path,
    external_root: Path | None = None,
    content_type_filter: str | None = None,
    dry_run: bool = False
) -> None:
    """Generate manifest and folder structure."""

    print(f"Reading from database: {db_path}")
    sources = get_sources_from_db(db_path)

    if content_type_filter:
        sources = [s for s in sources if s["content_type"] == content_type_filter]

    print(f"Found {len(sources)} sources")

    # Generate master manifest
    manifest = create_master_manifest(sources, archive_root, external_root)

    if dry_run:
        print("\n[DRY RUN] Would create the following structure:\n")

    # Create folders and per-folder indices
    folders_created = 0
    indices_created = 0

    for source in sources:
        folder_name = CONTENT_TYPE_FOLDERS.get(source["content_type"], source["content_type"])
        source_folder = sanitize_folder_name(source["source_name"])
        source_id = get_source_id(source["content_type"], source["source_name"])

        # Local folder path
        local_folder = archive_root / folder_name / source_folder
        index_file = local_folder / "_index.json"

        # Get items for this source
        items = get_items_for_source(db_path, source["content_type"], source["source_name"])

        # Create folder index
        folder_index = create_folder_index(
            source_id, source["source_name"], source["content_type"], items
        )

        if dry_run:
            print(f"  {local_folder}/")
            print(f"    _index.json ({source['item_count']} items)")
        else:
            # Create local folder
            local_folder.mkdir(parents=True, exist_ok=True)
            folders_created += 1

            # Write index file
            with open(index_file, 'w') as f:
                json.dump(folder_index, f, indent=2)
            indices_created += 1

        # Create external folder if specified
        if external_root:
            external_folder = external_root / folder_name / source_folder
            if dry_run:
                print(f"  [EXTERNAL] {external_folder}/")
            else:
                external_folder.mkdir(parents=True, exist_ok=True)

    # Write master manifest
    manifest_path = archive_root / ".archiver" / "manifest.json"

    if dry_run:
        print(f"\n  {manifest_path}")
        print(f"\nSummary:")
        print(f"  Total sources: {manifest['summary']['total_sources']}")
        print(f"  Total items: {manifest['summary']['total_items']}")
        print(f"  By type: {manifest['summary']['by_type']}")
    else:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with open(manifest_path, 'w') as f:
            json.dump(manifest, f, indent=2)

        print(f"\nCreated {folders_created} folders with {indices_created} index files")
        print(f"Master manifest: {manifest_path}")
        print(f"\nSummary:")
        print(f"  Total sources: {manifest['summary']['total_sources']}")
        print(f"  Total items: {manifest['summary']['total_items']}")
        print(f"  By type: {manifest['summary']['by_type']}")

        if external_root:
            print(f"\nExternal folders created at: {external_root}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate manifest and placeholder folders from archive database"
    )
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=Path.home() / "projects" / "content-archiver",
        help="Root directory for the archive (default: ~/projects/content-archiver)"
    )
    parser.add_argument(
        "--db",
        type=Path,
        help="Path to database file (default: {archive-root}/.archiver/archive.db)"
    )
    parser.add_argument(
        "--external-root",
        type=Path,
        help="Path to external drive root for mirroring folder structure"
    )
    parser.add_argument(
        "--type",
        choices=["podcast", "youtube", "article", "site", "forum"],
        help="Filter to specific content type"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be created without making changes"
    )

    args = parser.parse_args()

    db_path = args.db or (args.archive_root / ".archiver" / "archive.db")

    if not db_path.exists():
        print(f"Error: Database not found at {db_path}")
        return 1

    if args.external_root and not args.external_root.exists():
        print(f"Error: External root does not exist: {args.external_root}")
        return 1

    generate_manifest(
        archive_root=args.archive_root,
        db_path=db_path,
        external_root=args.external_root,
        content_type_filter=args.type,
        dry_run=args.dry_run,
    )

    return 0


if __name__ == "__main__":
    exit(main())
