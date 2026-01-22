# Content Archiver Development Notes

## 2026-01-22 - Index & Placeholder System Implementation

### What Was Done

1. **Database Path Migration**
   - Updated 5,101 records in `.archiver/archive.db` to use new project path
   - Changed from `/Users/calsheimer/Desktop/content archiver/` to `/Users/calsheimer/projects/content-archiver/`

2. **Created scripts/generate_manifest.py**
   - Generates master manifest at `.archiver/manifest.json`
   - Creates per-folder `_index.json` files in each source directory
   - Supports `--dry-run` mode to preview changes
   - Can mirror folder structure to external drive with `--external-root`
   - Filters by content type with `--type`

3. **Created scripts/mark_external.py**
   - Interactive mode scans external drive and finds matching sources
   - Batch mode for scripted updates: `--source <id> --location <path>`
   - Verify mode: `--verify` checks files without making changes
   - Updates both master manifest and per-folder indices

4. **Created scripts/check_archived.py**
   - Single URL check: `python3 check_archived.py <url>`
   - Source lookup: `--source "name"` fuzzy matches source names
   - Batch file: `--file urls.txt` checks multiple URLs
   - Pipe support: `cat urls.txt | python3 check_archived.py --new-only`
   - List all sources: `--list` (optionally filter by `--type`)

5. **Extended archiver/core/database.py**
   - `get_sources()` - Returns all unique sources with aggregate stats
   - `get_source_items()` - Returns all items for a specific source
   - `is_url_archived()` - Quick boolean check
   - `get_archived_info()` - Full record for a URL

6. **Added --check flag to CLI**
   - `archiver --check <url>` shows archive status inline

### Current Stats
- 63 unique sources
- 5,101 total items
- Breakdown: podcast (2909), article (1521), youtube (470), site (200), forum (1)

### Folder Structure Created
```
~/projects/content-archiver/
├── .archiver/
│   ├── archive.db          # Database (source of truth)
│   └── manifest.json       # Master index (63 sources)
├── articles/
│   └── {source}/_index.json
├── forums/
│   └── {source}/_index.json
├── podcasts/
│   └── {source}/_index.json  (38 sources)
├── videos/
│   └── {source}/_index.json  (18 sources)
└── websites/
    └── {source}/_index.json
```

### Next Steps
1. Mount external drive and run `mark_external.py` to track moved files
2. Consider adding original source URLs to manifest for future re-downloading
3. Test external drive workflow end-to-end

### Decisions Made
- Database is single source of truth; manifest is regenerable
- Per-folder indices enable offline browsing even if master manifest is lost
- Storage status tracks: `local`, `external`, `partial`
- External drive mirrors same folder structure (no manifest needed there)
