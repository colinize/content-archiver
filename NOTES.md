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
- [x] Transcript extraction for YouTube videos ✅ (Session 8 - via media-transcriber)
- [x] Podcast chapter markers support ✅ (Session 8 - via media-transcriber --chapters)
- [x] Parallel transcription processing ✅ (Session 9 - via --workers flag)
- [x] Combined document export ✅ (Session 9 - via --export flag)
- [x] Named entity extraction ✅ (Session 9 - via --entities flag)
- [x] Topic/keyword tagging ✅ (Session 9 - via --topics flag)
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

### Session 7 - Pinball Profile Podcast Archive (Jan 17, 2025)

#### Content Archived This Session
**Podcasts:**
| Source | Episodes | Size |
|--------|----------|------|
| Pinball Profile Podcast | 341 | 13GB |

RSS feed URL: `https://www.pinballprofile.com/feed/podcast/`

Episodes range from early episodes (ep 115+) through ep 432 (Kyle Spiteri, Nov 2025). Notable interviews include Eugene Jarvis (ep 400), Todd MacCulloch, Josh Sharpe, and many pinball industry figures and competitive players.

#### Notes
- Initial URL `https://www.pinballprofile.com/podcast-2/` was detected as ARTICLE
- Used RSS feed URL directly for proper podcast handling
- XMLParsedAsHTMLWarning appeared (BeautifulSoup parsing XML as HTML) but didn't affect downloads

### Session 8 - Media Transcriber Overhaul (Jan 17, 2025)

Major improvements to the standalone media-transcriber project at `~/projects/media-transcriber/`.

#### Core Engine Upgrade
- **Switched from OpenAI Whisper to faster-whisper** (CTranslate2-based, 4x faster)
- **Default model upgraded to large-v3** (most accurate, 1.5B parameters)
- **Added pinball-specific vocabulary prompt** for improved accuracy on domain terms
- **VAD filtering** (Silero-VAD) to skip silent sections
- **Device auto-detection**: CUDA → MPS → CPU with appropriate compute types

#### New Features Implemented

| Feature | Flag | Description |
|---------|------|-------------|
| Progress bars | (automatic) | Rich progress with ETA during transcription |
| Speaker diarization | `--diarize` | Identify who's speaking (requires HF_TOKEN) |
| SRT subtitles | `--srt` | Generate .srt subtitle files |
| VTT subtitles | `--vtt` | Generate WebVTT subtitle files |
| Custom vocabulary | `--vocab FILE` | Load domain-specific terms from file |
| Batch folders | (positional) | Process multiple folders in one command |
| Summary generation | `--summarize` | LLM-generated summaries (Ollama/OpenAI) |
| Chapters | `--chapters` | YouTube-compatible chapter markers |

#### Content Archiver Integration
Added `--transcribe` and `--transcribe-model` flags to archiver CLI:
```bash
archiver "https://youtube.com/watch?v=..." --transcribe
archiver --batch urls.txt --transcribe --transcribe-model medium
```

Archiver calls the transcriber via subprocess after downloads complete.

#### LLM Integration (for summaries/chapters)
- **Auto-detection**: Tries Ollama first (free, local), falls back to OpenAI
- **Ollama support**: `brew install ollama && ollama pull llama3.2`
- **OpenAI support**: Set `OPENAI_API_KEY` environment variable
- **Standalone modes**: `--summarize-only` and `--chapters-only` for existing transcripts

#### Usage Examples
```bash
# Basic transcription
python transcriber.py /path/to/podcasts

# Full featured
python transcriber.py /path/to/folder --diarize --srt --summarize --chapters

# Multiple folders
python transcriber.py ~/podcasts/show1 ~/podcasts/show2

# Summarize existing transcripts
python transcriber.py /path/to/folder --summarize-only

# Generate chapters for existing transcripts
python transcriber.py /path/to/folder --chapters-only
```

#### Files Modified
- `~/projects/media-transcriber/transcriber.py` - Complete rewrite
- `~/Desktop/Content Archiver/archiver/cli.py` - Added transcription integration

### Session 9 - Media Transcriber Enhancements (Jan 17, 2025)

Additional features added to the media-transcriber project.

#### New Features Implemented

| Feature | Flag | Description |
|---------|------|-------------|
| Parallel processing | `--workers N` / `-w N` | Transcribe multiple files simultaneously |
| Combined export | `--export` | Merge all transcripts into single document |
| Export-only mode | `--export-only` | Export existing transcripts without transcribing |
| Export format | `--export-format` | Choose markdown or txt format |
| Named entities | `--entities` | Extract people, companies, games, events, etc. |
| Entities-only | `--entities-only` | Extract from existing transcripts |
| Topic extraction | `--topics` | Extract main topics, keywords, themes |
| Topics-only | `--topics-only` | Extract from existing transcripts |

#### Parallel Processing
- Uses `ThreadPoolExecutor` for concurrent file processing
- Thread-safe console output via `Lock()`
- Recommended max: 3 workers (model memory constraints)
- Example: `python transcriber.py /folder --workers 3`

#### Combined Document Export
- Collects all `.transcript.md` files from specified folders
- Markdown format includes table of contents with links
- Plain text format strips markdown formatting
- Useful for importing full podcast series into AI tools
- Example: `python transcriber.py /folder --export-only --export-format txt`

#### Named Entity Extraction
- Uses LLM (Ollama/OpenAI) to extract structured entities
- Categories: people, companies, games, events, places, products
- Output: `.entities.json` files
- Pinball-optimized: recognizes designers, manufacturers, machines
- Example: `python transcriber.py /folder --entities-only`

#### Keyword/Topic Tagging
- Uses LLM to extract main topics and keywords
- Output fields: main_topics, keywords, themes, tone
- Output: `.topics.json` files
- Useful for categorization and searchability
- Example: `python transcriber.py /folder --topics-only`

#### Usage Examples
```bash
# Parallel transcription (2 files at once)
python transcriber.py /path/to/folder --workers 2

# Full analysis pipeline
python transcriber.py /folder --summarize --chapters --entities --topics

# Export existing transcripts to single markdown
python transcriber.py /folder --export-only

# Extract metadata from existing transcripts
python transcriber.py /folder --entities-only --topics-only --summarize-only
```

#### Implementation Notes
- All LLM features use the same provider system (`--summarize-provider`, `--summarize-model`)
- Entity/topic extraction uses JSON output mode for structured responses
- Fallback regex parsing if LLM returns malformed JSON

### Session 10 - Loser Kid Pinball Podcast Archive (Jan 17, 2025)

#### Content Archived This Session
**Podcasts:**
| Source | Episodes | Size |
|--------|----------|------|
| Pinball Profile Podcast (RSS) | 341 | 13GB |
| LoserKid Pinball Podcast (Zencastr) | 197 | 11GB |
| LoserKid Pinball Podcast (SoundCloud) | 166 | 8.2GB |

**Total this session:** 704 episodes, ~32GB

#### Archive Details

**Pinball Profile Podcast:**
- RSS feed: `https://www.pinballprofile.com/feed/podcast/`
- Episodes range from ep 115 through ep 432 (Kyle Spiteri, Nov 2025)
- Notable interviews: Eugene Jarvis (ep 400), Todd MacCulloch, Josh Sharpe

**LoserKid Pinball Podcast (Zencastr):**
- RSS feed: `https://feeds.zencastr.com/f/xtY9MlLy.rss`
- 197 episodes with UUID filenames
- Direct MP3 downloads, faster archive process
- Saved to `podcasts/LoserKid_Pinball_Podcast/`

**LoserKid Pinball Podcast (SoundCloud):**
- URL: `https://soundcloud.com/loserkidpinballpodcast`
- 166 episodes with proper titles
- Used yt-dlp directly (HLS streaming, slower)
- Saved to `podcasts/Loser_Kid_Pinball_Podcast/`

#### Notes
- SoundCloud requires yt-dlp (HLS streaming) while Zencastr has direct MP3s
- Zencastr has 31 more episodes than SoundCloud (likely newer episodes)
- Both archives may have different content - kept separate for completeness
- SoundCloud filenames have proper episode titles; Zencastr uses UUIDs

### Session 11 - Wedgehead Podcast Transcription (Jan 17, 2025)

#### Transcription Progress
Started transcription of Wedgehead Pinball Podcast (110 episodes) using media-transcriber.

| Status | Count |
|--------|-------|
| Total episodes | 110 |
| Transcribed | 7 (Episodes 1-7) |
| Remaining | 103 |
| Avg time/episode | ~35 min (CPU, large-v3 model) |

#### Process Details
- Transcription process started at 4:15 PM (PID 28846)
- Running on CPU with int8 quantization (large-v3 model)
- Using pinball-specific vocabulary prompt
- Process still running when session paused

#### Completed Transcripts
1. Episode 1 - Lightning Flippers (16:51)
2. Episode 2 - The Ritchie Brothers Steve vs. Mark (17:53)
3. Episode 3 - Boutique Manufacturers (18:21)
4. Episode 4 - The Brief History of Wedgehead (18:57)
5. Episode 5 - Video Modes (19:32)
6. Episode 6 - Howdy Pardner (20:16)
7. Episode 7 - Die on this Hill: Gilligan's Island (20:44)

#### Notes
- Episode 8 (Pinball Terminology Explained) in progress when paused
- Estimated ~60 hours remaining for full transcription
- Process will continue running in background

### Session 12 - Patreon RSS Support (Jan 17, 2025)

#### New Feature: Patreon Personal RSS Feeds
Added support for downloading podcasts from Patreon personal RSS feeds.

**Bug Fixed:**
- `/rss/?$` pattern only matched RSS at end of path
- Patreon URLs like `/rss/creatorname` weren't detected as podcasts
- Added `patreon.com/rss/` and `/rss/` patterns to detector

**New Scripts Created:**
- `scripts/tag_simple.py` - Add ID3 metadata from RSS feed to downloaded MP3s
- `scripts/rename_episodes.py` - Rename files using episode titles and dates

**Usage:**
```bash
# Download Patreon podcast
archiver --yes "https://www.patreon.com/rss/creatorname?auth=TOKEN&show=ID"

# Tag files with metadata (requires feed.xml in folder)
python scripts/tag_simple.py "podcasts/FolderName"

# Rename files to "YYYY-MM-DD_Episode Title.mp3"
python scripts/rename_episodes.py "podcasts/FolderName"
```

#### Content Archived This Session
**Podcasts:**
| Source | Episodes | Size |
|--------|----------|------|
| Kaneda Patreon (RSS) | 590 | 23GB |

- Episodes range from Dec 2021 (Ep 634) to Jan 2026 (Ep 1178)
- ID3 tagged: 572 (11 failed due to iCloud sync timeouts)
- All 583 files renamed with date and episode title

### Session 13 - Knapp Arcade Archives (Jan 18, 2025)

#### New Feature: Cookie-Authenticated API Scraper
Created `scripts/scrape_knapp_archives.py` to scrape content behind login walls using browser cookies.

**Features:**
- Auto-extracts cookies from Chrome/Firefox/Safari via `browser_cookie3`
- Manual cookie string option (`--cookie`) for Keychain-free operation
- Handles paginated and single-response APIs
- Saves individual markdown files + combined JSON

**Usage:**
```bash
# Auto-extract cookies from browser
python scripts/scrape_knapp_archives.py

# Manual cookie string
python scripts/scrape_knapp_archives.py --cookie "session=abc123"

# Debug mode to see API response
python scripts/scrape_knapp_archives.py --debug
```

#### Content Archived This Session
**Articles:**
| Source | Posts | Size |
|--------|-------|------|
| Knapp Arcade Archives (API) | 999 | 6.4MB |

- Posts include arcade reports, pinball reviews, event coverage, industry news
- Content spans 2016-2025
- Full post content captured (not truncated "read more" excerpts)
- API endpoint: `https://www.knapparcade.org/api/archives`
- Authentication: Browser cookies (paid membership required)

#### Technical Notes
- Site is a React app hosted on Replit with Stripe payments
- API returns all 1000 posts in single response (no pagination needed)
- Post fields: `id`, `title`, `slug`, `content`, `excerpt`, `publish_date`, `published_at`, `created_at`, `updated_at`, `author_id`, `source_url`
- macOS Keychain access required for Chrome cookie extraction (or use `--cookie` flag)

### Session 14 - Dutch Pinball Open Expo 2024 & 2025 (Jan 18, 2025)

#### Content Archived This Session
**YouTube Playlists:**
| Source | Videos | Size |
|--------|--------|------|
| Dutch Pinball Open Expo 2024 (Pinball News) | 9 | 5.7GB |
| Dutch Pinball Open Expo 2025 (Pinball News) | 9 | 5.1GB |
| Dirty Pool Podcast (Pinball Industry) | 25 | 21GB |
| Wormhole Pinball Presents | 42 | 31GB |

**Podcasts:**
| Source | Episodes | Size |
|--------|----------|------|
| Eclectic Gamers Podcast | 264 | 15GB |
| Slam Tilt Podcast | 100 | ~8GB |

**Individual YouTube Videos:**
| Source | Video | Size |
|--------|-------|------|
| Wormhole Pinball | TWIPY Awards Show 2025 Part I | 593MB |
| Wormhole Pinball | TWIPY Awards Show 2025 Part II | 2.4GB |
| Kaneda Pinball | Episode 1000: George Gomez | 311MB |
| Kaneda Pinball | Kaneda Visits Automated Pinball | 297MB |

**2024 Playlist:** `https://www.youtube.com/watch?v=9dLjuLczXyk&list=PLsqJ4LfOEWVXentrasEM8kZcDeJIaSc9u`
- Dutch Pinball Exclusive, Jersey Jack Pinball (2), Stern Pinball, Pinball Brothers, Barrels of Fun, Hexa Pinball, Dutch Pinball Museum, 23-Minute Tour

**2025 Playlist:** `https://www.youtube.com/watch?v=00QmG2ovQv0&list=PLsqJ4LfOEWVU-5qsKv004M4_2luLiFd1_`
- 28-Minute Tour, Dr. Sander Bakkes, Tony Ramunni, Steve Ritchie (2), Gary Stern & Jack Danger, Antoine Depelchin (Hexa), Pinball Brothers, Team NL JJP

**Dirty Pool Podcast:** `https://www.youtube.com/playlist?list=PLS9lWVjGsygallsiz2_TJ_oxIlhl29fLC`
- Pinball industry interviews (Scott Danesi, FAST Pinball, Spooky Pinball, etc.)
- 4 videos still rate-limited by YouTube (can retry later)

**Wormhole Pinball Presents:** `https://www.youtube.com/playlist?list=PLOPIF-UqiqSaBvV9PgsQ6ilI_TC-fjf3f`
- 51 episodes including interviews, Project Pinball, Arcades Across America series

**Eclectic Gamers Podcast:** `http://feeds.feedburner.com/eclecticgamerspodcast`
- Pinball & video games podcast, episodes 1-263 plus bonus interviews
- 1 file failed (Mike Homepin interview - malformed URL in feed)

**Slam Tilt Podcast:** `https://www.slamtiltpodcast.com/feed/podcast`
- 100 episodes (Episodes 164-262)
- All downloads successful

**Individual Videos:**
- TWIPY Awards Show 2025 (Parts I & II) - Annual pinball awards ceremony
- Kaneda Episode 1000 - George Gomez interview (legendary pinball designer)
- Kaneda Visits Automated Pinball - Tour of pinball manufacturing facility

#### Notes
- YouTube playlists required Chrome cookies (`-c chrome`) due to bot detection
- 89 playlist videos + 4 individual videos downloaded
- 4 Dirty Pool videos still rate-limited by YouTube (can retry later)
- Eclectic Gamers: 264 of 265 episodes (1 failed - malformed URL)
- Slam Tilt: 100 of 100 episodes (all successful)

---

*Last updated: January 19, 2025*
