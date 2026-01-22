#!/usr/bin/env python3
"""Mark sources as archived to external storage.

Updates manifest.json to reflect which sources have been moved to external storage.
Can verify files exist on mounted drive before marking.
"""

import argparse
import json
from pathlib import Path


def load_manifest(archive_root: Path) -> dict:
    """Load the master manifest."""
    manifest_path = archive_root / ".archiver" / "manifest.json"
    if not manifest_path.exists():
        raise FileNotFoundError(
            f"Manifest not found at {manifest_path}. Run generate_manifest.py first."
        )
    with open(manifest_path) as f:
        return json.load(f)


def save_manifest(archive_root: Path, manifest: dict) -> None:
    """Save the master manifest."""
    manifest_path = archive_root / ".archiver" / "manifest.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)


def update_folder_index(folder_path: Path, storage_status: str) -> None:
    """Update the _index.json in a folder with new storage status."""
    index_path = folder_path / "_index.json"
    if index_path.exists():
        with open(index_path) as f:
            index_data = json.load(f)
        index_data["storage_status"] = storage_status
        with open(index_path, 'w') as f:
            json.dump(index_data, f, indent=2)


def count_files_in_folder(folder_path: Path) -> int:
    """Count media files in a folder (excludes _index.json)."""
    if not folder_path.exists():
        return 0
    count = 0
    for item in folder_path.iterdir():
        if item.is_file() and item.name != "_index.json":
            count += 1
    return count


def verify_external_files(
    archive_root: Path,
    external_root: Path,
    manifest: dict
) -> list[dict]:
    """Verify which sources have files on external drive."""
    verified = []

    for source in manifest["sources"]:
        external_folder = external_root / source["folder_path"]
        file_count = count_files_in_folder(external_folder)

        if file_count > 0:
            verified.append({
                "source": source,
                "external_folder": external_folder,
                "file_count": file_count,
                "expected_count": source["item_count"],
                "complete": file_count >= source["item_count"],
            })

    return verified


def mark_source_external(
    archive_root: Path,
    manifest: dict,
    source_id: str,
    external_location: str
) -> bool:
    """Mark a specific source as external in the manifest."""
    for source in manifest["sources"]:
        if source["id"] == source_id:
            source["storage_status"] = "external"
            source["external_location"] = external_location

            # Update local folder index
            local_folder = archive_root / source["folder_path"]
            update_folder_index(local_folder, "external")

            return True
    return False


def interactive_mode(archive_root: Path, external_root: Path) -> None:
    """Interactive mode to select and mark sources."""
    manifest = load_manifest(archive_root)

    print(f"\nScanning external drive: {external_root}")
    print("-" * 60)

    verified = verify_external_files(archive_root, external_root, manifest)

    if not verified:
        print("No sources found on external drive.")
        return

    print(f"\nFound {len(verified)} sources with files on external drive:\n")

    for i, v in enumerate(verified, 1):
        status = "COMPLETE" if v["complete"] else "PARTIAL"
        current = v["source"]["storage_status"]
        marker = " [already marked]" if current == "external" else ""
        print(
            f"  {i}. {v['source']['source_name']}"
            f" ({v['file_count']}/{v['expected_count']} files - {status}){marker}"
        )

    print("\nOptions:")
    print("  a - Mark ALL found sources as external")
    print("  c - Mark only COMPLETE sources as external")
    print("  1,2,3 - Mark specific sources by number")
    print("  q - Quit without changes")

    choice = input("\nYour choice: ").strip().lower()

    if choice == 'q':
        print("No changes made.")
        return

    sources_to_mark = []

    if choice == 'a':
        sources_to_mark = verified
    elif choice == 'c':
        sources_to_mark = [v for v in verified if v["complete"]]
    else:
        try:
            indices = [int(x.strip()) - 1 for x in choice.split(',')]
            sources_to_mark = [verified[i] for i in indices if 0 <= i < len(verified)]
        except (ValueError, IndexError):
            print("Invalid selection.")
            return

    if not sources_to_mark:
        print("No sources selected.")
        return

    # Update manifest
    for v in sources_to_mark:
        mark_source_external(
            archive_root,
            manifest,
            v["source"]["id"],
            str(v["external_folder"])
        )

    # Update external_root in manifest
    manifest["external_root"] = str(external_root)

    save_manifest(archive_root, manifest)

    print(f"\nMarked {len(sources_to_mark)} sources as external:")
    for v in sources_to_mark:
        print(f"  - {v['source']['source_name']}")


def batch_mode(
    archive_root: Path,
    source_id: str,
    external_location: str
) -> None:
    """Batch mode to mark a specific source."""
    manifest = load_manifest(archive_root)

    if mark_source_external(archive_root, manifest, source_id, external_location):
        save_manifest(archive_root, manifest)
        print(f"Marked {source_id} as external at {external_location}")
    else:
        print(f"Source not found: {source_id}")


def verify_mode(archive_root: Path, external_root: Path) -> None:
    """Verify mode - check files without making changes."""
    manifest = load_manifest(archive_root)

    print(f"\nVerifying external storage at: {external_root}")
    print("-" * 60)

    verified = verify_external_files(archive_root, external_root, manifest)

    if not verified:
        print("No sources found on external drive.")
        return

    complete = [v for v in verified if v["complete"]]
    partial = [v for v in verified if not v["complete"]]

    print(f"\nComplete sources ({len(complete)}):")
    for v in complete:
        print(f"  - {v['source']['source_name']} ({v['file_count']} files)")

    if partial:
        print(f"\nPartial sources ({len(partial)}):")
        for v in partial:
            print(
                f"  - {v['source']['source_name']} "
                f"({v['file_count']}/{v['expected_count']} files)"
            )

    print(f"\nSummary:")
    print(f"  Total sources on external: {len(verified)}")
    print(f"  Complete: {len(complete)}")
    print(f"  Partial: {len(partial)}")


def main():
    parser = argparse.ArgumentParser(
        description="Mark sources as archived to external storage"
    )
    parser.add_argument(
        "--archive-root",
        type=Path,
        default=Path.home() / "projects" / "content-archiver",
        help="Root directory for the archive"
    )
    parser.add_argument(
        "--external-root",
        type=Path,
        help="Path to external drive root"
    )
    parser.add_argument(
        "--source",
        help="Source ID to mark (for batch mode)"
    )
    parser.add_argument(
        "--location",
        help="External location path (for batch mode)"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify mode - check files without making changes"
    )

    args = parser.parse_args()

    if args.source and args.location:
        # Batch mode
        batch_mode(args.archive_root, args.source, args.location)
    elif args.external_root:
        if not args.external_root.exists():
            print(f"Error: External root does not exist: {args.external_root}")
            return 1

        if args.verify:
            verify_mode(args.archive_root, args.external_root)
        else:
            interactive_mode(args.archive_root, args.external_root)
    else:
        parser.print_help()
        print("\nExamples:")
        print("  Interactive: python mark_external.py --external-root /Volumes/MyDrive")
        print("  Verify:      python mark_external.py --external-root /Volumes/MyDrive --verify")
        print("  Batch:       python mark_external.py --source podcast-kaneda --location /Volumes/MyDrive/podcasts/Kaneda")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
