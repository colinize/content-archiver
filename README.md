# Content Archiver

A simple CLI tool to archive content from the internet. Just run `archiver "URL"` - it auto-detects YouTube, podcasts, forums, articles, or full websites and does the right thing.

## Installation

```bash
# Clone the repo
git clone https://github.com/colinize/content-archiver.git
cd content-archiver

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install
pip install -e .
```

### System Requirements

- **Python 3.9+**
- **ffmpeg** (for YouTube video merging): `brew install ffmpeg`

## Usage

```bash
# ONE COMMAND FOR EVERYTHING
archiver "URL"

# Examples:
archiver "https://youtube.com/watch?v=dQw4w9WgXcQ"     # Downloads video
archiver "https://youtube.com/playlist?list=..."       # Prompts: "45 videos, download?"
archiver "https://www.pinrepair.com/topcast/past.php"  # Finds audio files, prompts
archiver "https://reddit.com/r/.../comments/..."       # Extracts forum thread
archiver "https://example.com/blog/post"               # Extracts article
archiver "https://blog.example.com"                    # Crawls entire site (needs Firecrawl)

# Batch: archive multiple URLs from a file
archiver --batch urls.txt

# Resume interrupted downloads
archiver --resume

# Show archive status/history
archiver --status
```

## Supported Content Types

| Type | Detection | What It Does |
|------|-----------|--------------|
| **YouTube** | youtube.com, youtu.be | Downloads videos/playlists/channels with yt-dlp |
| **Podcast** | RSS feeds, Spotify/Apple links, audio webpages | Downloads MP3s, adds ID3 metadata |
| **Forum** | Reddit, Discourse, phpBB, vBulletin | Extracts posts with pagination, saves as MD/HTML |
| **Article** | Any webpage | Extracts main content, saves as MD/HTML |
| **Site** | Any domain (with `--site` or Firecrawl) | Crawls and archives all pages |

## Features

- **Auto-detection**: Automatically identifies content type from URL
- **Interactive prompts**: Shows what it found, asks before downloading
- **Selective download**: Choose specific items from playlists/feeds
- **Progress tracking**: Rich progress bars for downloads
- **Resume support**: SQLite database tracks downloads for resume
- **Smart extraction**: Follows indirect audio links, handles pagination
- **Multiple formats**: Saves as Markdown, HTML, and JSON

## Output Structure

```
~/Desktop/content archiver/
├── videos/                       # YouTube content
│   └── MKBHD/
│       ├── video-title.mp4
│       └── video-title.info.json
├── podcasts/                     # Audio content
│   └── TOPcast/
│       ├── index.json
│       └── episode-title.mp3
├── forums/                       # Reddit & forum threads
│   └── r_pinball_thread-title/
│       ├── thread.md
│       ├── thread.html
│       └── images/
├── articles/                     # Blog posts & articles
│   └── pinballnews.com/
│       ├── article-title.md
│       └── images/
└── websites/                     # Full site archives
    └── example.com/
        ├── index.json
        └── page-1.md
```

## Site Crawling with Firecrawl

For full website archiving, you need a Firecrawl API key:

```bash
# Get a free key at https://firecrawl.dev
export FIRECRAWL_API_KEY='your-api-key'

# Then crawl any site
archiver "https://blog.example.com"
```

## Dependencies

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - YouTube downloading
- [feedparser](https://github.com/kurtmckee/feedparser) - RSS parsing
- [beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/) - HTML parsing
- [rich](https://github.com/Textualize/rich) - Terminal UI
- [readability-lxml](https://github.com/buriy/python-readability) - Article extraction
- [mutagen](https://github.com/quodlibet/mutagen) - Audio metadata

## License

MIT
