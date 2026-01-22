#!/usr/bin/env python3
"""
Scrape Knapp Arcade archives using browser cookies for authentication.

Usage:
    # Auto-extract cookies from browser (may require Keychain password on macOS)
    python scripts/scrape_knapp_archives.py
    python scripts/scrape_knapp_archives.py --browser firefox

    # Manual cookie string (copy from DevTools > Application > Cookies)
    python scripts/scrape_knapp_archives.py --cookie "session=abc123; token=xyz789"

    # Specify output directory
    python scripts/scrape_knapp_archives.py --output ~/projects/content-archiver/articles/knapparcade.org
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from http.cookiejar import CookieJar
from http.cookies import SimpleCookie

import requests
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn

console = Console()

API_URL = "https://www.knapparcade.org/api/archives"
DEFAULT_OUTPUT = Path.home() / "projects" / "content-archiver" / "articles" / "knapparcade.org"


def parse_cookie_string(cookie_string: str) -> dict:
    """Parse a cookie string into a dict."""
    cookies = {}
    for item in cookie_string.split(';'):
        item = item.strip()
        if '=' in item:
            key, value = item.split('=', 1)
            cookies[key.strip()] = value.strip()
    return cookies


def get_cookies_from_browser(browser: str = "chrome"):
    """Extract cookies from browser."""
    try:
        import browser_cookie3
    except ImportError:
        console.print("[red]browser_cookie3 not installed[/red]")
        console.print("[yellow]Install with: pip install browser_cookie3[/yellow]")
        console.print("[yellow]Or use --cookie option to provide cookies manually[/yellow]")
        sys.exit(1)

    console.print(f"[dim]Extracting cookies from {browser}...[/dim]")

    cookie_funcs = {
        "chrome": browser_cookie3.chrome,
        "firefox": browser_cookie3.firefox,
        "safari": browser_cookie3.safari,
        "edge": browser_cookie3.edge,
        "chromium": browser_cookie3.chromium,
    }

    if browser not in cookie_funcs:
        console.print(f"[red]Unknown browser: {browser}[/red]")
        console.print(f"Supported: {', '.join(cookie_funcs.keys())}")
        sys.exit(1)

    try:
        cj = cookie_funcs[browser](domain_name=".knapparcade.org")
        # Convert to dict for requests
        return {c.name: c.value for c in cj}
    except Exception as e:
        console.print(f"[red]Failed to get cookies from {browser}: {e}[/red]")
        console.print("[yellow]Make sure you're logged into knapparcade.org in your browser[/yellow]")
        console.print("[yellow]Or use --cookie option to provide cookies manually[/yellow]")
        sys.exit(1)


def fetch_archives(cookies, page: int = 1, limit: int = 100):
    """Fetch archives from API."""
    params = {"page": page, "limit": limit}

    try:
        response = requests.get(API_URL, cookies=cookies, params=params, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            console.print("[red]Authentication failed - cookies may be expired[/red]")
            console.print("[yellow]Try logging into knapparcade.org again in your browser[/yellow]")
        else:
            console.print(f"[red]HTTP Error: {e}[/red]")
        sys.exit(1)
    except Exception as e:
        console.print(f"[red]Failed to fetch archives: {e}[/red]")
        sys.exit(1)


def fetch_all_archives(cookies):
    """Fetch all archive posts, handling pagination."""
    all_posts = []
    page = 1
    limit = 100  # Fetch in batches

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Fetching archives...", total=None)

        while True:
            data = fetch_archives(cookies, page=page, limit=limit)

            # Handle different API response formats
            if isinstance(data, list):
                posts = data
                total = None
            elif isinstance(data, dict):
                posts = data.get("posts") or data.get("items") or data.get("data") or data.get("archives") or []
                total = data.get("total") or data.get("totalCount")

                if total and progress.tasks[task].total is None:
                    progress.update(task, total=total)
            else:
                console.print(f"[yellow]Unexpected API response format[/yellow]")
                break

            if not posts:
                break

            all_posts.extend(posts)
            progress.update(task, completed=len(all_posts), description=f"[cyan]Fetched {len(all_posts)} posts...")

            # Check if we've got all posts
            if len(posts) < limit:
                break

            page += 1

    return all_posts


def sanitize_filename(title: str) -> str:
    """Create a safe filename from title."""
    # Remove/replace problematic characters
    safe = re.sub(r'[<>:"/\\|?*]', '', title)
    safe = re.sub(r'\s+', '_', safe)
    safe = safe[:100]  # Limit length
    return safe or "untitled"


def save_post_markdown(post: dict, output_dir: Path) -> Path:
    """Save a single post as markdown."""
    # Extract fields (adjust based on actual API response)
    title = post.get("title") or post.get("name") or "Untitled"
    content = post.get("content") or post.get("body") or post.get("text") or ""
    date = post.get("date") or post.get("createdAt") or post.get("publishedAt") or ""
    author = post.get("author") or post.get("authorName") or ""
    post_id = post.get("id") or post.get("_id") or ""
    tags = post.get("tags") or []

    # Parse date if present
    date_str = ""
    if date:
        try:
            if isinstance(date, str):
                # Try common formats
                for fmt in ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d"]:
                    try:
                        dt = datetime.strptime(date[:26], fmt)
                        date_str = dt.strftime("%Y-%m-%d")
                        break
                    except ValueError:
                        continue
        except Exception:
            date_str = str(date)[:10]

    # Create filename
    if date_str:
        filename = f"{date_str}_{sanitize_filename(title)}.md"
    else:
        filename = f"{sanitize_filename(title)}.md"

    filepath = output_dir / filename

    # Build markdown content
    md_lines = [f"# {title}", ""]

    if date_str:
        md_lines.append(f"**Date:** {date_str}")
    if author:
        md_lines.append(f"**Author:** {author}")
    if tags:
        md_lines.append(f"**Tags:** {', '.join(tags)}")
    if post_id:
        md_lines.append(f"**ID:** {post_id}")

    md_lines.append("")
    md_lines.append("---")
    md_lines.append("")
    md_lines.append(content)

    filepath.write_text("\n".join(md_lines), encoding="utf-8")
    return filepath


def save_all_posts(posts: list, output_dir: Path):
    """Save all posts as individual markdown files and a combined JSON."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save combined JSON
    json_path = output_dir / "_all_posts.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=2, ensure_ascii=False, default=str)
    console.print(f"[green]Saved combined JSON:[/green] {json_path}")

    # Save individual markdown files
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("[cyan]Saving posts...", total=len(posts))

        for post in posts:
            save_post_markdown(post, output_dir)
            progress.advance(task)

    console.print(f"[green]Saved {len(posts)} posts to:[/green] {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Scrape Knapp Arcade archives")
    parser.add_argument(
        "--browser", "-b",
        default="chrome",
        help="Browser to extract cookies from (chrome, firefox, safari, edge)"
    )
    parser.add_argument(
        "--cookie", "-c",
        help="Manual cookie string (copy from DevTools > Network > Request Headers)"
    )
    parser.add_argument(
        "--output", "-o",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"Output directory (default: {DEFAULT_OUTPUT})"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Print API response for debugging"
    )
    args = parser.parse_args()

    console.print("[bold]Knapp Arcade Archives Scraper[/bold]\n")

    # Get cookies - manual or from browser
    if args.cookie:
        console.print("[dim]Using provided cookie string...[/dim]")
        cookies = parse_cookie_string(args.cookie)
    else:
        cookies = get_cookies_from_browser(args.browser)
    console.print("[green]✓[/green] Got cookies\n")

    # Test API access first
    console.print("[dim]Testing API access...[/dim]")
    test_data = fetch_archives(cookies, page=1, limit=1)

    if args.debug:
        console.print("[yellow]API Response:[/yellow]")
        console.print(json.dumps(test_data, indent=2, default=str)[:2000])
        console.print("\n")

    console.print("[green]✓[/green] API access confirmed\n")

    # Fetch all archives
    posts = fetch_all_archives(cookies)

    if not posts:
        console.print("[yellow]No posts found in archives[/yellow]")
        return

    console.print(f"\n[green]✓[/green] Found {len(posts)} posts\n")

    # Save posts
    save_all_posts(posts, args.output)

    console.print("\n[bold green]Done![/bold green]")


if __name__ == "__main__":
    main()
