# Content Archiver Development Notes

## 2026-02-23 - Knapp Arcade Date Fix, Pinball News Legacy Recovery, YAML Frontmatter

### What Was Done

1. **Fixed Knapp Arcade publish dates (`scripts/fix_knapp_dates.py`)**
   - 66 posts from Aug 19-20, 2021 had the CMS migration date instead of their real publish date
   - Parsed real dates from `(Month Year)` patterns in article titles
   - Fixed 64 of 66 — dates range from July 2016 to February 2020
   - 2 unfixable (no date clue): "YESTERcades - Somerville, NJ" and "8 on the Break - Dunellen, NJ"
   - Updated `_all_posts.json` and added `**Publish Date:**` to all 999 markdown files

2. **Exported Pinball News WordPress articles to flat folder**
   - Copied 534 `article.md` files from `articles/pinballnews.com/` subdirectories
   - Renamed using `og_title` from `article.json` + publish date: `TITLE (YYYY-MM-DD).md`
   - 6 non-article pages skipped (sitemap, index pages, directory)
   - Output: `pinball news markdown files/` — covers Nov 2015 to Jan 2026

3. **Recovered 196 legacy Pinball News articles via Wayback Machine (`scripts/scrape_old_pinballnews.py`)**
   - 198 old `/news/*.html` URLs were in the DB as "complete" but all pointed to one generic file (content lost during original scrape)
   - First pass fetched 124 via `web.archive.org/web/2015/` snapshots
   - Retry pass with years 2003-2017 recovered remaining 72 (2 non-articles skipped: index.html, .mp3)
   - Saved to `articles/pinballnews.com-legacy/` — covers ~2003-2017
   - Extracted all-caps article titles from body text (192 of 196 found)
   - Stripped Wayback Machine banner/calendar junk from content
   - Added to `pinball news markdown files/` with proper title + date filenames

4. **Added YAML frontmatter to all exported markdown files**
   - Pinball News (728 files): `title`, `date`, `url`, `source: Pinball News`, `era: wordpress|legacy`
   - Knapp Arcade (999 files): `title`, `date`, `url`, `source: Knapp Arcade`
   - Stripped old inline metadata (`# Title`, `Source:`, `Published:`, `**Slug:**`, `**ID:**`, etc.)
   - Clean format ready for import into any CMS or static site generator

### New Files Created
- `scripts/fix_knapp_dates.py` — Knapp Arcade publish date fixer
- `scripts/scrape_old_pinballnews.py` — Wayback Machine scraper for legacy Pinball News
- `articles/pinballnews.com-legacy/` — 196 recovered legacy articles (2003-2017)
- `pinball news markdown files/` — 728 Pinball News articles with YAML frontmatter

### Current Article Counts
- Knapp Arcade: 999 articles (July 2016 – Oct 2023), YAML frontmatter in `articles/knapparcade.org/`
- Pinball News WordPress: 534 articles (Nov 2015 – Jan 2026)
- Pinball News Legacy: 196 articles (~2003 – 2017, from Wayback Machine)
- Total Pinball News (merged folder): 728 files in `pinball news markdown files/`

### Decisions Made
- Knapp Arcade dates without day precision default to 1st of month (e.g., "July 2017" → 2017-07-01)
- Legacy Pinball News articles use copyright year as fallback date when no explicit date found
- YAML frontmatter uses `era: wordpress|legacy` to distinguish Pinball News source eras
- Wayback Machine junk (banner, calendar, metadata) stripped from legacy article content

---

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

### External Drive Testing (same session)

**Drive:** My Passport for Mac at `/Volumes/My Passport for Mac/Pinball Media Archive`

**Issue Found:** External drive had flat structure (all sources directly in root) instead of nested structure (videos/Source/, podcasts/Source/).

**Fix:** Updated `mark_external.py` with `find_matching_folder()` function that checks:
1. Nested path (videos/Source_Name/)
2. Flat path (Source_Name/ directly in root)
3. Fuzzy name matching for slight variations

**Results:**
- 50 sources detected on external drive
- 23 complete sources marked as external
- 27 partial sources (some files present, not all)

**Folder Structure Created on External:**
```
/Volumes/My Passport for Mac/Pinball Media Archive/
├── videos/           (18 source folders)
├── podcasts/         (38 source folders)
├── articles/         (4 source folders)
├── websites/         (2 source folders)
└── forums/           (1 source folder)
```

User will manually reorganize existing flat files into the new structure.

### Next Steps
1. Reorganize files on external drive into new folder structure
2. Re-run `mark_external.py --verify` after reorganization
3. Consider adding original source URLs to manifest for future re-downloading

### Decisions Made
- Database is single source of truth; manifest is regenerable
- Per-folder indices enable offline browsing even if master manifest is lost
- Storage status tracks: `local`, `external`, `partial`
- External drive mirrors same folder structure (no manifest needed there)
