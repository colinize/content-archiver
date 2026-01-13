# Content Archiver - Instructions

A complete guide to installing and using the Content Archiver CLI tool.

---

## Quick Start

```bash
# 1. Clone and enter the directory
git clone https://github.com/colinize/content-archiver.git
cd content-archiver

# 2. Set up Python environment
python3 -m venv venv
source venv/bin/activate

# 3. Install
pip install -e .

# 4. Archive something!
archiver "https://youtube.com/watch?v=VIDEO_ID"
```

---

## Installation

### Prerequisites

| Requirement | How to Check | How to Install |
|-------------|--------------|----------------|
| Python 3.9+ | `python3 --version` | [python.org](https://python.org) or `brew install python` |
| pip | `pip --version` | Comes with Python |
| ffmpeg (optional) | `ffmpeg -version` | `brew install ffmpeg` |

**Note:** ffmpeg is only required for YouTube downloads that need video+audio merging. The tool works without it but will download lower quality single-stream videos.

### Step-by-Step Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/colinize/content-archiver.git
   cd content-archiver
   ```

2. **Create a virtual environment** (required on macOS due to PEP 668)
   ```bash
   python3 -m venv venv
   ```

3. **Activate the virtual environment**
   ```bash
   # macOS/Linux
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

   You should see `(venv)` in your terminal prompt.

4. **Install the package**
   ```bash
   pip install -e .
   ```

5. **Verify installation**
   ```bash
   archiver --help
   ```

### Updating

```bash
cd content-archiver
git pull
pip install -e .
```

---

## Usage

### Basic Command

```bash
archiver "URL"
```

That's it. The tool auto-detects what type of content the URL points to and handles it appropriately.

### Examples by Content Type

#### YouTube Videos

```bash
# Single video
archiver "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Playlist (will prompt to select videos)
archiver "https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf"

# Channel (fetches up to 100 recent videos)
archiver "https://www.youtube.com/@mkbhd"
```

**Output:** `{channel-name}/video-title.mp4` plus thumbnail and metadata JSON.

#### Podcasts

```bash
# RSS feed
archiver "https://feeds.example.com/podcast.rss"

# Webpage with audio files
archiver "https://www.pinrepair.com/topcast/past.php"

# Platform links (Spotify, Apple) - shows message about limitations
archiver "https://open.spotify.com/show/..."
```

**Output:** `{podcast-name}/episode-title.mp3` with ID3 metadata tags.

#### Reddit Threads

```bash
archiver "https://www.reddit.com/r/pinball/comments/abc123/thread_title/"
```

**Output:**
- `thread.md` - Markdown with nested comments
- `thread.html` - Styled HTML version
- `thread.json` - Raw data
- `images/` - Any images from the thread

#### Articles & Blog Posts

```bash
archiver "https://www.pinballnews.com/site/2025/12/01/some-article/"
archiver "https://medium.com/@user/article-title"
```

**Output:**
- `article-title.md` - Clean markdown
- `article-title.html` - Styled HTML
- `article-title.json` - Metadata
- `images/` - Downloaded images

#### Full Websites (requires Firecrawl API)

```bash
# Set your API key first
export FIRECRAWL_API_KEY='your-api-key'

# Crawl entire site
archiver "https://blog.example.com"
```

Get a free API key at [firecrawl.dev](https://firecrawl.dev).

---

## Interactive Prompts

When archiving collections (playlists, podcasts, etc.), the tool shows what it found and asks what to do:

```
Found 45 episodes in "My Podcast"

  1. Episode 45 - Latest News
  2. Episode 44 - Interview
  3. Episode 43 - Review
  ... and 42 more

Download options:
  [A] Download all 45 episodes
  [S] Select specific episodes
  [N] Cancel

Your choice:
```

If you choose **Select**, you can enter episode numbers:
```
Enter episode numbers (e.g., 1,3,5-10): 1-5,10,15
```

---

## Output Location

All content is saved to:
```
~/Desktop/content archiver/
```

Each source gets its own folder:
```
~/Desktop/content archiver/
├── MKBHD/                          # YouTube channel
├── TOPcast/                        # Podcast
├── r_pinball_thread_title/         # Reddit thread
├── pinballnews.com/                # Article source
└── .archiver/                      # Tool data (database)
    └── archive.db
```

---

## Command-Line Options

```bash
archiver "URL"              # Archive a single URL
archiver --batch urls.txt   # Archive URLs from a file (one per line)
archiver --resume           # Resume interrupted downloads
archiver --status           # Show download history
archiver --help             # Show help
```

---

## Troubleshooting

### "externally-managed-environment" error on pip install

**Problem:** macOS prevents installing packages to the system Python.

**Solution:** Use a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### "ffmpeg not found" warning on YouTube downloads

**Problem:** yt-dlp needs ffmpeg to merge separate video and audio streams.

**Solution:** Install ffmpeg:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

The tool still works without ffmpeg but downloads single-stream videos (lower quality).

### "No posts could be extracted" on Reddit

**Problem:** Old versions tried to scrape HTML, but Reddit uses JavaScript rendering.

**Solution:** Update to the latest version which uses Reddit's JSON API:
```bash
git pull
pip install -e .
```

### Podcast only finds 2 episodes

**Problem:** Some podcast pages use indirect links (e.g., `download.php?id=5`).

**Solution:** The tool automatically resolves these. If still having issues, check if the page requires login or has other access restrictions.

### YouTube download fails

**Possible causes:**
1. Video is private or age-restricted
2. Video is geo-blocked in your region
3. yt-dlp needs updating: `pip install --upgrade yt-dlp`

---

## Configuration

### Environment Variables

| Variable | Purpose | Required |
|----------|---------|----------|
| `FIRECRAWL_API_KEY` | Full website crawling | Only for site crawling |

Set in your shell:
```bash
export FIRECRAWL_API_KEY='fc-your-key-here'
```

Or add to `~/.zshrc` / `~/.bashrc` for persistence.

---

## Tips

1. **Always activate the venv** before using the tool:
   ```bash
   source venv/bin/activate
   ```

2. **Bookmark the folder**: The output folder is `~/Desktop/content archiver/`

3. **Check status**: Use `archiver --status` to see what you've archived

4. **Resume downloads**: If a download is interrupted, run `archiver --resume`

5. **Selective downloads**: When prompted, choose "Select" to pick specific items instead of downloading everything

---

## Getting Help

- **GitHub Issues:** [github.com/colinize/content-archiver/issues](https://github.com/colinize/content-archiver/issues)
- **Project Notes:** See `NOTES.md` for development history and known issues

---

*Last updated: January 2025*
