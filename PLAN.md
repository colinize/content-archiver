# Content Archiver Redesign Plan

## Inspiration

[How The New York Times uses a custom AI tool to track the "manosphere"](https://www.niemanlab.org/2026/02/how-the-new-york-times-uses-a-custom-ai-tool-to-track-the-manosphere/) — Nieman Lab, Feb 2026

The NYT's "Manosphere Report" uses LLMs to automatically transcribe and summarize dozens of podcasts, delivering AI-generated reports to journalists. Their broader "Cheatsheet" tool applies the same approach to general investigative research at scale. Key philosophy: AI as a "force multiplier" for existing work, not a content generator.

## Current State

The content-archiver is a **manual, on-demand CLI tool**. You paste a URL, it downloads the content. It has:

- Auto-detection of content types (YouTube, podcast, forum, article, website)
- SQLite database tracking 5,100+ downloads across 63 sources
- Transcription support via external `media-transcriber` tool
- Batch processing from URL files
- Resume capability for interrupted downloads

**What it lacks:**
- No automated monitoring (must manually re-check sources)
- No AI-powered analysis of archived content
- No summarization or theme extraction
- No periodic reporting or notifications
- No concept of "watched" sources vs one-off downloads

---

## Proposed Redesign: Three Phases

### Phase 1: Watch & Monitor System

**Goal:** Transform from one-shot archiver into a source monitoring tool that automatically detects and archives new content.

#### 1.1 Watchlist (`archiver/core/watchlist.py`)

New database table and CLI commands for managing monitored sources:

```sql
CREATE TABLE watchlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL UNIQUE,           -- Source URL (RSS feed, channel, etc.)
    content_type TEXT NOT NULL,         -- youtube, podcast, article, site
    source_name TEXT,                   -- Human-readable name
    check_interval_hours INTEGER DEFAULT 24,
    last_checked_at TEXT,
    last_new_content_at TEXT,
    enabled BOOLEAN DEFAULT 1,
    metadata TEXT,                      -- JSON: custom settings per source
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**CLI commands:**
```bash
archiver watch "https://feeds.example.com/podcast.rss"      # Add source to watchlist
archiver watch --name "My Podcast" "URL"                     # Add with custom name
archiver watch --interval 12 "URL"                           # Check every 12 hours
archiver unwatch "URL"                                       # Remove from watchlist
archiver watchlist                                           # Show all watched sources
archiver watchlist --enabled                                 # Show only active watches
```

#### 1.2 New Content Detection (`archiver/core/monitor.py`)

Logic to check watched sources and identify new items not yet in the database:

- **RSS/Podcast feeds:** Compare feed entries against `downloads` table by URL
- **YouTube channels/playlists:** Use yt-dlp to list videos, compare against archived
- **Websites:** Use Firecrawl or sitemap.xml to detect new pages
- **Articles/blogs:** Check RSS feed or sitemap for new posts

```python
class Monitor:
    def check_source(self, watch: WatchEntry) -> list[NewItem]:
        """Check a watched source for new content. Returns list of new items."""

    def check_all(self) -> dict[str, list[NewItem]]:
        """Check all enabled watched sources. Returns {source_name: [new_items]}."""

    def archive_new(self, items: list[NewItem], auto_confirm=True) -> list[Download]:
        """Download and archive new items."""
```

**CLI commands:**
```bash
archiver check                    # Check all watched sources for new content
archiver check "URL"              # Check a specific watched source
archiver check --download         # Check and auto-download new content
```

#### 1.3 Scheduler Support

Add a `run` command for daemon/cron-style operation:

```bash
archiver run                      # Run continuously, checking sources on their intervals
archiver run --once               # Run one check cycle and exit (for cron)
```

Config file (`~/.archiver/config.yaml` or similar):
```yaml
monitor:
  default_interval_hours: 24
  auto_download: true
  max_concurrent_downloads: 3
```

**Database changes:** Add `last_checked_at` tracking to avoid redundant checks. Store check results for debugging.

---

### Phase 2: AI Analysis Pipeline

**Goal:** Add LLM-powered transcription, summarization, and analysis of archived content — the core of the NYT approach.

#### 2.1 Transcription Integration (`archiver/ai/transcribe.py`)

Improve the existing transcription integration:

- Currently calls external `media-transcriber` tool
- Move to built-in Whisper support or configurable transcription backend
- Auto-transcribe new podcast/video downloads when `--transcribe` is set per-watched-source
- Store transcripts alongside media files and in the database

```sql
ALTER TABLE downloads ADD COLUMN transcript_path TEXT;
ALTER TABLE downloads ADD COLUMN transcript_status TEXT DEFAULT 'none';
-- transcript_status: none, pending, processing, complete, error
```

**Watchlist integration:**
```bash
archiver watch --transcribe "https://feeds.example.com/podcast.rss"
```

This means: watch this feed, auto-download new episodes, and auto-transcribe them.

#### 2.2 LLM Summarization (`archiver/ai/summarize.py`)

Use an LLM API to process transcripts and article text:

```python
class Summarizer:
    def summarize(self, text: str, prompt: str = None) -> Summary:
        """Generate a summary of the given text."""

    def extract_topics(self, text: str) -> list[str]:
        """Extract key topics/themes from text."""

    def extract_entities(self, text: str) -> list[Entity]:
        """Extract named entities (people, organizations, etc.)."""

    def compare_themes(self, summaries: list[Summary]) -> ThemeReport:
        """Compare themes across multiple pieces of content."""
```

**Supported backends** (configurable):
- Anthropic Claude API (default)
- OpenAI API
- Local models via Ollama

**Database additions:**
```sql
CREATE TABLE summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    download_id INTEGER REFERENCES downloads(id),
    summary_type TEXT,              -- 'brief', 'detailed', 'topics', 'entities'
    content TEXT NOT NULL,          -- The summary text or JSON
    model TEXT,                     -- Which model generated this
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
```

**CLI commands:**
```bash
archiver summarize "URL"                  # Summarize a specific archived item
archiver summarize --source "Podcast"     # Summarize all items from a source
archiver summarize --recent 7             # Summarize items from last 7 days
```

**Watchlist integration:**
```bash
archiver watch --transcribe --summarize "URL"
```

#### 2.3 Analysis Configuration

Per-source analysis prompts (like NYT's customized Cheatsheet):

```yaml
# In watchlist metadata or config file
sources:
  - url: "https://feeds.example.com/podcast.rss"
    name: "Example Podcast"
    transcribe: true
    summarize: true
    analysis_prompt: |
      Summarize this podcast episode. Focus on:
      - Key topics discussed
      - Notable claims or opinions
      - Any news or announcements mentioned
      - Sentiment toward [specific topics]
```

---

### Phase 3: Report Generation & Delivery

**Goal:** Automatically generate periodic digest reports from monitored sources and deliver them, mirroring the NYT's emailed "Manosphere Report."

#### 3.1 Report Generator (`archiver/reports/generator.py`)

Combine summaries across sources into structured reports:

```python
class ReportGenerator:
    def generate_digest(self, period: str = "daily") -> Report:
        """Generate a digest of new content from watched sources."""

    def generate_source_report(self, source_name: str) -> Report:
        """Generate a detailed report for a specific source."""

    def generate_theme_report(self, theme: str) -> Report:
        """Generate a cross-source report on a specific theme."""
```

**Report format options:**
- Markdown (for local reading)
- HTML (for email)
- JSON (for programmatic consumption)

#### 3.2 Report Templates (`archiver/reports/templates/`)

Configurable report templates:

```
Daily Digest — Feb 12, 2026
============================

## New Content (last 24 hours)

### Podcasts (3 new episodes)

**Example Podcast** — "Episode Title"
- Published: Feb 11, 2026
- Summary: [AI-generated 2-3 sentence summary]
- Key topics: topic1, topic2, topic3

**Another Podcast** — "Episode Title"
- ...

### Articles (5 new articles)
- ...

### Videos (1 new video)
- ...

## Cross-Source Themes
- [Theme 1]: Discussed in Podcast A, Article B
- [Theme 2]: Mentioned across 3 sources

## Source Status
- 12 sources checked, 3 with new content
- 2 sources had errors (see details)
```

#### 3.3 Delivery (`archiver/reports/deliver.py`)

Configurable delivery channels:

```python
class ReportDelivery:
    def send_email(self, report: Report, recipients: list[str]) -> None:
    def save_local(self, report: Report, path: Path) -> None:
    def post_webhook(self, report: Report, url: str) -> None:
```

**Config:**
```yaml
reports:
  digest_schedule: "daily"          # daily, weekly, or cron expression
  format: "html"
  delivery:
    - type: email
      recipients: ["user@example.com"]
      smtp_host: "smtp.gmail.com"
    - type: local
      path: "~/reports/"
    - type: webhook
      url: "https://hooks.slack.com/..."
```

**CLI commands:**
```bash
archiver report                           # Generate and display today's digest
archiver report --period weekly           # Generate weekly digest
archiver report --send                    # Generate and deliver via configured channels
archiver report --source "Podcast Name"   # Report on specific source
```

---

## Implementation Priority

| Priority | Feature | Effort | Value |
|----------|---------|--------|-------|
| **P0** | Watchlist + CLI commands | Medium | Foundation for everything |
| **P0** | New content detection (monitor) | Medium | Core monitoring capability |
| **P1** | `archiver check` + auto-download | Low | Makes monitoring actionable |
| **P1** | Auto-transcription on watch | Low | Builds on existing transcriber |
| **P2** | LLM summarization | Medium | The "AI force multiplier" |
| **P2** | Database schema for summaries | Low | Storage for AI output |
| **P3** | Report generator | Medium | Combines everything into output |
| **P3** | Report templates | Low | Formatting layer |
| **P3** | Email/webhook delivery | Medium | Completes the pipeline |
| **P4** | Scheduler/daemon mode | Medium | Fully automated operation |
| **P4** | Cross-source theme analysis | High | Advanced AI feature |
| **P4** | Per-source analysis prompts | Low | Customization layer |

---

## Architecture Changes

### New Package Structure

```
archiver/
├── __init__.py
├── cli.py                          # Extended with new commands
├── detector.py                     # Unchanged
├── core/
│   ├── config.py                   # Extended for new settings
│   ├── database.py                 # Extended with new tables
│   ├── downloader.py               # Unchanged
│   ├── progress.py                 # Unchanged
│   ├── monitor.py                  # NEW: Source monitoring logic
│   └── watchlist.py                # NEW: Watchlist management
├── handlers/                       # Unchanged
│   ├── youtube.py
│   ├── podcast.py
│   ├── forum.py
│   ├── article.py
│   └── site.py
├── ai/                             # NEW: AI analysis pipeline
│   ├── __init__.py
│   ├── transcribe.py               # Transcription management
│   ├── summarize.py                # LLM summarization
│   └── prompts.py                  # Default and custom prompts
└── reports/                        # NEW: Report generation
    ├── __init__.py
    ├── generator.py                # Report composition
    ├── deliver.py                  # Delivery channels
    └── templates/                  # Report templates
        ├── daily_digest.md.j2
        └── source_report.md.j2
```

### New Dependencies

```toml
[project.optional-dependencies]
ai = [
    "anthropic>=0.30",              # Claude API
    "openai>=1.0",                  # OpenAI API (alternative)
]
reports = [
    "jinja2>=3.0",                  # Report templating
]
```

### CLI Changes (using Click groups)

Current CLI is a single `@click.command()`. Redesign to use `@click.group()` for subcommands while keeping backward compatibility:

```bash
# Existing behavior (preserved):
archiver "URL"                      # Archive a URL (default command)
archiver --batch urls.txt           # Batch archive
archiver --status                   # Show status

# New subcommands:
archiver watch "URL"                # Add to watchlist
archiver unwatch "URL"              # Remove from watchlist
archiver watchlist                  # List watched sources
archiver check                     # Check for new content
archiver check --download          # Check and download new content
archiver summarize "URL"           # Summarize archived content
archiver report                    # Generate digest report
archiver run                       # Run monitoring daemon
```

---

## Design Decisions

1. **LLM provider should be configurable.** Default to Anthropic Claude, but support OpenAI and local models (Ollama). Store API keys in environment variables (`ANTHROPIC_API_KEY`, `OPENAI_API_KEY`).

2. **Reports are generated from summaries, not raw content.** The pipeline is: Archive → Transcribe → Summarize → Report. Each step is independently useful and can be run standalone.

3. **The watchlist is separate from the downloads table.** A watchlist entry represents a source to monitor. Downloads represent individual items. One watchlist entry can produce many downloads over time.

4. **Backward compatibility is maintained.** `archiver "URL"` continues to work exactly as before. New features are additive, accessed through subcommands or flags.

5. **AI features are optional.** The tool should work without any API keys for basic archiving and monitoring. AI summarization and smart reporting require API configuration.

6. **Per-source customization.** Each watched source can have its own check interval, auto-download preference, transcription setting, and analysis prompt. This mirrors how the NYT customizes analysis per podcast.

---

## Open Questions

1. **Should monitoring state be stored in the same SQLite database or a separate one?** Single database is simpler but could get large. Separate databases keep concerns isolated.

2. **What's the right default summarization prompt?** Need to experiment with prompts that produce useful, concise summaries across different content types (podcast transcript vs article vs forum thread).

3. **How should the scheduler work?** Options: built-in daemon using `schedule` library, systemd service file, or simple cron-friendly `--once` mode. Cron is probably most portable.

4. **Should we support Whisper locally or rely on the external transcriber?** Local Whisper gives more control but requires GPU setup. The existing `media-transcriber` integration works but is fragile.

5. **Email delivery: SMTP directly or use a service?** SMTP is universal but fiddly. Services like SendGrid/Resend are simpler but add a dependency. Could support both.
