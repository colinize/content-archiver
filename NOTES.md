# Content Archiver - Project Notes

This file tracks conversations, decisions, bugs, plans, and ideas for the project.

---

## Project History

### Initial Concept (Jan 2025)
User wanted a tool to systematically archive content from the internet:
- Podcasts, forum threads, Reddit threads, YouTube videos
- Save to `~/Desktop/content archiver` with logical folder structure
- CLI interface with interactive prompts

### Key Design Decisions

1. **Single command interface**: `archiver "URL"` - auto-detects content type
2. **Interactive prompts over config files**: Shows what's found, asks before downloading
3. **Flat folder structure**: `{source-name}/files` instead of nested hierarchies
4. **SQLite for tracking**: Enables resume and status checking

### Tech Stack Chosen
- **Python 3.9+** with Click CLI
- **yt-dlp** for YouTube (industry standard)
- **feedparser** for RSS parsing
- **BeautifulSoup + lxml** for HTML parsing
- **rich** for terminal UI (progress bars, prompts)
- **readability-lxml** for article extraction
- **mutagen** for audio ID3 metadata
- **Firecrawl API** for full site crawling

---

## Bugs Encountered & Fixes

### 1. Podcast page detected as ARTICLE
**Problem**: `pinrepair.com/topcast/past.php` was classified as ARTICLE instead of PODCAST
**Solution**: Added audio file detection in `article.py` - if HTML contains `.mp3`, `.m4a`, etc., redirect to podcast handler

### 2. Only 2 direct MP3 links found on podcast page
**Problem**: Many episodes use indirect links like `showget.php?id=65` that redirect to MP3s
**Solution**: Implemented `resolve_indirect_audio_links()` in `podcast.py`:
- Detects potential audio links (URLs containing "download", "get", "play", etc.)
- Uses HEAD requests to check Content-Type without downloading
- Follows redirects to find actual audio URLs
- Now finds 50+ episodes instead of just 2

### 3. pip install fails on macOS
**Problem**: `pip install` refused due to PEP 668 (externally managed environment)
**Solution**: Use virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### 4. YouTube download fails without ffmpeg
**Problem**: yt-dlp requires ffmpeg to merge separate video+audio streams, fails with error
**Solution**: Added ffmpeg detection in `youtube.py`:
- Checks if ffmpeg is available via `shutil.which('ffmpeg')`
- If available: uses best video+audio format with merging
- If not available: falls back to single format (no merging needed), shows warning
- Works for single videos, playlists, and channels

### 5. Reddit thread extraction returns no posts
**Problem**: Generic forum scraper couldn't extract Reddit threads - returned "No posts could be extracted"
**Cause**: Reddit's modern site uses JavaScript to render content, BeautifulSoup only sees empty HTML
**Solution**: Implemented Reddit-specific handler using JSON API in `forum.py`:
- Appends `.json` to thread URL to get structured data
- Recursive comment extraction with depth tracking
- Extracts images from galleries and preview URLs
- Reddit-specific markdown/HTML formatting with nested reply indentation
- Successfully extracted 59 posts with images from test thread

---

## Features Implemented

### YouTube Handler (`handlers/youtube.py`)
- Single video download with metadata
- Playlist support with selective download
- Channel video listing (up to 100 videos)
- Progress bars via yt-dlp hooks
- Saves thumbnails and info.json
- **ffmpeg fallback**: Works without ffmpeg installed (uses single format)

### Facebook Handler (`handlers/facebook.py`)
- Page videos download (all videos from a Facebook page)
- Single video and reel download
- Concurrent downloads (3 workers by default)
- Skip-if-exists for resume capability
- Browser cookie support for private content
- Progress tracking with completion summary

### Podcast Handler (`handlers/podcast.py`)
- RSS feed parsing with feedparser
- Platform URL detection (Spotify, Apple, etc.)
- Webpage audio scanning with BeautifulSoup
- **Indirect link resolution** - follows redirects to find actual audio files
- ID3 metadata tagging with mutagen
- Progress tracking per episode

### Forum Handler (`handlers/forum.py`)
- Multi-platform support: Reddit, Discourse, phpBB, vBulletin, generic
- **Reddit JSON API** - bypasses JavaScript rendering, extracts via API
- Recursive comment extraction with reply depth tracking
- Automatic pagination following for non-Reddit forums
- Post extraction: author, date, content, score, images
- Output: thread.md, thread.html, thread.json
- Image downloading to `images/` subfolder

### Article Handler (`handlers/article.py`)
- readability-lxml for main content extraction
- markdownify for HTML→Markdown conversion
- Metadata extraction: author, date, description, Open Graph
- Image downloading
- Styled HTML output

### Site Handler (`handlers/site.py`)
- Firecrawl API integration for URL discovery
- Batch scraping with progress
- Falls back to single-page mode without API key
- Saves as Markdown + HTML per page

---

## Ideas & Future Enhancements

### Discussed but not yet implemented:
- [x] `--batch` flag fully tested with URL file input ✅ (Session 3)
- [x] `--yes` / `-y` flag for auto-confirm in batch mode ✅ (Session 3)
- [ ] `--resume` flag for interrupted downloads
- [ ] `--status` flag to show download history

### Potential improvements:
- [ ] Rate limiting for polite crawling
- [ ] Proxy support for geo-restricted content
- [ ] Archive.org integration for wayback saves
- [ ] PDF export option
- [ ] EPUB export for articles/forums
- [ ] Transcript extraction for YouTube videos
- [ ] Podcast chapter markers support
- [ ] RSS feed generation from archived content
- [ ] Deduplication across archives
- [ ] Search across archived content

### Content types to consider:
- [x] Facebook videos/pages ✅ (Session 6)
- [ ] Twitter/X threads
- [ ] Instagram posts/reels
- [ ] TikTok videos
- [ ] Substack newsletters
- [ ] Medium articles (with paywall handling)
- [ ] GitHub repos/gists
- [ ] Hacker News threads
- [ ] Stack Overflow Q&As

---

## Configuration Notes

### Environment Variables
```bash
# Required for full site crawling
export FIRECRAWL_API_KEY='your-api-key'
```

### System Requirements
```bash
# macOS
brew install ffmpeg  # Required for YouTube video merging
```

### Virtual Environment Setup
```bash
cd ~/Desktop/content\ archiver
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

---

## File Structure

### Project Files
```
content archiver/
├── archiver/
│   ├── __init__.py
│   ├── cli.py              # Main entry point
│   ├── detector.py         # URL type detection
│   ├── core/
│   │   ├── config.py       # Configuration management
│   │   ├── database.py     # SQLite tracking
│   │   ├── downloader.py   # Shared download utilities
│   │   └── progress.py     # Rich UI components
│   ├── handlers/
│   │   ├── youtube.py      # yt-dlp wrapper
│   │   ├── podcast.py      # RSS + audio scanning
│   │   ├── forum.py        # Thread extraction
│   │   ├── article.py      # Content extraction
│   │   └── site.py         # Firecrawl integration
│   └── utils/
│       └── __init__.py
├── pyproject.toml
├── README.md
├── INSTRUCTIONS.md         # User guide
├── NOTES.md                # This file
└── .gitignore
```

### Archive Output Structure
```
~/Desktop/content archiver/
├── videos/                 # YouTube videos, playlists, channels
│   └── {channel-name}/
├── podcasts/               # Podcast episodes
│   └── {podcast-name}/
├── forums/                 # Reddit threads, forum discussions
│   └── {thread-title}/
├── articles/               # Blog posts, news articles
│   └── {site-domain}/
├── websites/               # Full site crawls
│   └── {domain}/
└── .archiver/
    └── archive.db          # SQLite tracking database
```

---

## Session Log

### Session 1 - Initial Development
- Created project structure
- Implemented all core handlers
- Fixed podcast detection bug
- Added indirect audio link resolution
- Pushed to GitHub: https://github.com/colinize/content-archiver

### Session 2 - Testing & Fixes (Jan 13, 2025)
- Tested podcast handler with pinrepair.com - successfully found 50 episodes
- Tested YouTube handler - discovered ffmpeg requirement
- Added ffmpeg fallback to youtube.py for environments without ffmpeg
- Added CLAUDE.md instruction to auto-update NOTES.md each session
- Successfully downloaded 1.6GB YouTube video without ffmpeg
- Tested Reddit thread - discovered JavaScript rendering issue
- Implemented Reddit JSON API handler for thread extraction
- Successfully archived Reddit thread with 59 posts and 2 images
- Tested article handler with pinballnews.com - successfully extracted article with 4 images
- Added INSTRUCTIONS.md with comprehensive user guide
- Reorganized folder structure: Archive → videos/podcasts/forums/articles/websites → source → files

### Session 3 - Batch Processing & Bug Fixes (Jan 13-14, 2025)

#### Bug Fixes
1. **auto_confirm not propagating through handlers**
   - Problem: Batch mode caused EOF errors when podcast/audio prompts appeared
   - Fixed: `handle_platform_url()` in podcast.py now accepts and passes `auto_confirm`
   - Fixed: `handle_article()` now accepts `auto_confirm` and passes to `handle_audio_webpage()`
   - Fixed: CLI passes `auto_confirm` to article handler and fallback case

2. **Installed ffmpeg via Homebrew**
   - Required for SoundCloud MP3 conversion from m4a
   - `brew install ffmpeg`

#### New Features
1. **Site handler exclude_paths parameter**
   - Added `exclude_paths` parameter to `handle_site()`
   - Filters out URLs matching patterns (e.g., `/topcast/`)
   - Used for pinrepair.com to skip already-downloaded podcast section

#### Content Archived This Session

**Podcasts (1,408 episodes total):**
| Source | Episodes |
|--------|----------|
| Special When Lit | 98 |
| The Pinball Show (Pinball Network) | 200 |
| Head2Head Pinball | 101 |
| Wedgehead Pinball Podcast | 110 |
| Silverball Chronicles | 50 |
| SoundCloud kanedapinball | 799 |
| Pinball News audio files (retry batch) | ~50 |

**Articles:**
| Source | Count |
|--------|-------|
| Pinball News (batch of 1,643 URLs) | 538 articles |
| Polygon - Big Bang Bar history | 1 |
| Wayback Machine - Steve Ritchie IRC Interview | 1 |

**Websites:**
| Source | Pages |
|--------|-------|
| pinrepair.com (excluding /topcast/) | 100 |
| pinwiki.com | 100 |

#### Batch Processing
- Tested batch mode with 1,643 Pinball News URLs
- Fixed comment line handling (skip lines starting with #)
- Auto-confirm enabled for all batch operations
- Created retry mechanism for failed URLs

### Session 4 - YouTube Playlist Fix (Jan 14, 2025)

#### Bug Fixes
1. **YouTube playlist URLs with `?list=` not detected as playlists**
   - Problem: URLs like `youtube.com/watch?v=XXX&list=YYY` were detected as "video" instead of "playlist"
   - Root cause: `detect_youtube_type()` only checked for "playlist" string, not `list=` query param
   - Fix: Added `'list=' in url_lower` check to `detector.py:109`

2. **Playlist extraction returning 0 entries for video+list URLs**
   - Problem: yt-dlp's `extract_flat=True` returns empty entries for video URLs with list param
   - Fix: `download_playlist()` now extracts playlist ID and constructs proper playlist URL (`youtube.com/playlist?list=ID`)

3. **yt-dlp requires JavaScript runtime (deno) for YouTube**
   - Problem: YouTube now requires JS challenges to be solved, yt-dlp needs deno
   - Warning shown: "No supported JavaScript runtime could be found"
   - Fix: Installed deno via `brew install deno`
   - Also installed `yt-dlp[default]` from GitHub master for `yt-dlp-ejs` support

#### New Features
1. **Concurrent playlist/channel downloads**
   - Added ThreadPoolExecutor for parallel video downloads (default: 3 workers)
   - Significantly faster for large playlists

2. **Skip-if-exists for resume capability**
   - Checks if video already exists before downloading
   - Shows count of existing videos at start
   - Displays skip/complete/fail status per video
   - Enables easy resume after interruption

3. **Better progress reporting**
   - Shows `✓` for completed, `⊘` for skipped, `✗` for failed
   - Summary at end: "X downloaded, Y skipped, Z failed"

#### Content Archived This Session
**YouTube Playlists:**
| Source | Videos | Size |
|--------|--------|------|
| Pinball Expo 2025 (Pinball News) | 46 | 22GB |
| Pinball Expo 2018 (Pinball News) | 23 (1 unavailable) | 12GB |
| Pinball Expo 2022 (Pinball News) | 33 (1 unavailable) | 36GB |

### Session 5 - Kaneda's Pinball Podcast Archive (Jan 15, 2025)

#### New Feature: Browser Cookie Support
**Problem**: 34 of 79 videos failed with "Sign in to confirm you're not a bot" error
**Solution**: Added `--cookies-from-browser` / `-c` option to use browser cookies for authentication

Usage:
```bash
archiver -c chrome "https://youtube.com/playlist?list=..."
archiver -c firefox "https://youtube.com/watch?v=..."
```

Changes made:
- `cli.py`: Added `-c`/`--cookies-from-browser` option
- `youtube.py`: Added `cookiesfrombrowser` to all yt-dlp option dicts
- Passes cookies through `handle_youtube()`, `download_video()`, `download_playlist()`, `download_channel()`, and helper functions

#### Content Archived This Session
**YouTube Playlists:**
| Source | Videos | Size |
|--------|--------|------|
| Kaneda's Pinball Podcast (k) | 79 | 38GB |

Playlist URL: `https://www.youtube.com/watch?v=4moPSmKUg-I&list=PLP-lGX1cksAJo2jUwFQOggnkbNHTXAGga`

Content includes Saturday Morning Spectacular weekly streams, game reveal reactions (Alice, Dune, Kong, Harry Potter, D&D, Beetlejuice, JAWS 50th), 2024/2025 Kudos Awards shows, and Sunday Morning Service episodes.

Initial attempt downloaded 45 videos; retry with `-c chrome` successfully downloaded remaining 34 videos.

### Session 6 - Facebook Support (Jan 17, 2025)

#### New Feature: Facebook Video Downloads
Added support for downloading videos from Facebook pages and individual Facebook videos.

**Supported URL formats:**
- Page videos: `facebook.com/PageName/videos/`
- Single video: `facebook.com/watch?v=...`
- Video links: `fb.watch/...`
- Reels: `facebook.com/reel/...`

**Usage:**
```bash
# Download all videos from a Facebook page
archiver "https://www.facebook.com/PageName/videos/"

# With cookies for logged-in content
archiver -c chrome "https://www.facebook.com/PageName/videos/"

# Single video
archiver "https://fb.watch/abc123/"
```

**Files changed:**
- `detector.py`: Added `FACEBOOK` ContentType, URL patterns, `detect_facebook_type()` function
- `handlers/facebook.py`: New handler using yt-dlp (mirrors YouTube handler structure)
- `cli.py`: Added routing for Facebook URLs

**Features:**
- Auto-detects Facebook URLs (pages, videos, reels)
- Page video listing with interactive selection
- Concurrent downloads (3 workers by default)
- Skip-if-exists for resume capability
- Browser cookie support (`-c chrome`) for private/restricted content
- Progress tracking with completion summary

---

*Last updated: January 17, 2025*
