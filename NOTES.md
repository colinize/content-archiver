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

---

## Features Implemented

### YouTube Handler (`handlers/youtube.py`)
- Single video download with metadata
- Playlist support with selective download
- Channel video listing (up to 100 videos)
- Progress bars via yt-dlp hooks
- Saves thumbnails and info.json
- **ffmpeg fallback**: Works without ffmpeg installed (uses single format)

### Podcast Handler (`handlers/podcast.py`)
- RSS feed parsing with feedparser
- Platform URL detection (Spotify, Apple, etc.)
- Webpage audio scanning with BeautifulSoup
- **Indirect link resolution** - follows redirects to find actual audio files
- ID3 metadata tagging with mutagen
- Progress tracking per episode

### Forum Handler (`handlers/forum.py`)
- Multi-platform support: Reddit, Discourse, phpBB, vBulletin, generic
- Automatic pagination following
- Post extraction: author, date, content, images
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
- [ ] `--batch` flag fully tested with URL file input
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
├── NOTES.md                # This file
└── .gitignore
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

---

*Last updated: January 13, 2025*
