"""Scrape old Pinball News /news/ articles via the Wayback Machine.

Reads the 198 URLs from the archive DB, fetches each from web.archive.org,
extracts the article text, and saves as individual markdown files.
"""

import json
import os
import re
import sqlite3
import time
import urllib.request
from html.parser import HTMLParser

DB_PATH = "/Users/calsheimer/projects/content-archiver/.archiver/archive.db"
OUT_DIR = "/Users/calsheimer/projects/content-archiver/articles/pinballnews.com-legacy"
WAYBACK_PREFIX = "https://web.archive.org/web/2015/"

# Rate limit: be nice to archive.org
DELAY = 1.5  # seconds between requests


class ArticleExtractor(HTMLParser):
    """Extract text content from Pinball News HTML pages."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.in_body = False
        self.skip_tags = {"script", "style", "nav", "header", "footer"}
        self.skip_depth = 0
        self.title = ""
        self.in_title = False
        self.date_text = ""

    def handle_starttag(self, tag, attrs):
        if tag == "body":
            self.in_body = True
        if tag == "title":
            self.in_title = True
        if tag in self.skip_tags:
            self.skip_depth += 1
        if tag == "br" and self.in_body and self.skip_depth == 0:
            self.text_parts.append("\n")
        if tag == "p" and self.in_body and self.skip_depth == 0:
            self.text_parts.append("\n\n")

    def handle_endtag(self, tag):
        if tag in self.skip_tags:
            self.skip_depth = max(0, self.skip_depth - 1)
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_body and self.skip_depth == 0:
            self.text_parts.append(data)

    def get_text(self):
        raw = "".join(self.text_parts)
        # Clean up excessive whitespace but keep paragraph breaks
        lines = []
        for line in raw.split("\n"):
            line = line.strip()
            if line:
                lines.append(line)
            elif lines and lines[-1] != "":
                lines.append("")
        return "\n".join(lines).strip()


def extract_date(text):
    """Try to find a date in the article text."""
    # Look for "Story dated Month Day, Year" pattern common on Pinball News
    m = re.search(
        r"(?:Story\s+dated|dated)\s+"
        r"((?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\s+\d{1,2},?\s+\d{4})",
        text,
        re.IGNORECASE,
    )
    if m:
        return m.group(1)

    # Look for standalone dates
    m = re.search(
        r"((?:January|February|March|April|May|June|July|August|September|"
        r"October|November|December)\s+\d{1,2},?\s+\d{4})",
        text,
    )
    if m:
        return m.group(1)

    return None


def url_to_slug(url):
    """Convert URL to a filesystem-safe slug."""
    # Extract the meaningful part: /news/foo.html -> foo
    path = url.split("/news/")[-1] if "/news/" in url else url.split("/")[-1]
    path = path.replace("/index.html", "").replace(".html", "").replace("/", "_")
    return path


def fetch_from_wayback(url):
    """Fetch a URL from the Wayback Machine."""
    wayback_url = WAYBACK_PREFIX + url
    req = urllib.request.Request(
        wayback_url,
        headers={"User-Agent": "content-archiver/1.0 (personal archive project)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return None


def main():
    os.makedirs(OUT_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT DISTINCT url FROM downloads WHERE url LIKE '%pinballnews.com/news%' ORDER BY url"
    ).fetchall()
    conn.close()

    urls = [r[0] for r in rows]
    print(f"Found {len(urls)} URLs to scrape")

    success = 0
    failed = []

    for i, url in enumerate(urls):
        slug = url_to_slug(url)
        md_path = os.path.join(OUT_DIR, f"{slug}.md")

        if os.path.exists(md_path):
            print(f"  [{i+1}/{len(urls)}] SKIP (exists): {slug}")
            success += 1
            continue

        print(f"  [{i+1}/{len(urls)}] Fetching: {slug} ...", end=" ", flush=True)

        html = fetch_from_wayback(url)
        if not html:
            print("FAILED (fetch)")
            failed.append((url, "fetch failed"))
            time.sleep(DELAY)
            continue

        parser = ArticleExtractor()
        parser.feed(html)
        text = parser.get_text()
        title = parser.title.strip()

        if len(text) < 50:
            print(f"FAILED (too short: {len(text)} chars)")
            failed.append((url, f"too short: {len(text)} chars"))
            time.sleep(DELAY)
            continue

        # Clean up the title
        title = re.sub(r"\s*[-–|]\s*Pinball News.*$", "", title, flags=re.IGNORECASE)
        if not title:
            title = slug.replace("_", " ").title()

        date = extract_date(text)
        date_line = f"Published: {date}\n" if date else ""

        md_content = f"# {title}\n\nSource: {url}\n{date_line}\n---\n\n{text}\n"

        with open(md_path, "w") as f:
            f.write(md_content)

        print(f"OK ({len(text)} chars, date: {date or 'none'})")
        success += 1
        time.sleep(DELAY)

    print(f"\nDone: {success} saved, {len(failed)} failed")
    if failed:
        print("\nFailed URLs:")
        for url, reason in failed:
            print(f"  {reason}: {url}")


if __name__ == "__main__":
    main()
