"""Site handler for full website archiving using Firecrawl."""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urlparse

import requests

from ..core.database import Database
from ..core.downloader import sanitize_filename, get_source_folder
from ..core.progress import (
    console,
    show_found_items,
    confirm_download,
    select_items,
    print_info,
    print_success,
    print_error,
    print_warning,
)

# Firecrawl API base URL
FIRECRAWL_API_URL = "https://api.firecrawl.dev/v1"


def get_api_key() -> Optional[str]:
    """Get Firecrawl API key from environment."""
    return os.environ.get('FIRECRAWL_API_KEY')


def handle_site(url: str, output_dir: Path, db: Database) -> None:
    """Handle full website archiving."""
    api_key = get_api_key()

    if not api_key:
        print_warning("Firecrawl API key not found.")
        print_info("To use site crawling, set your API key:")
        print_info("  export FIRECRAWL_API_KEY='your-api-key'")
        print_info("")
        print_info("Get a free API key at: https://firecrawl.dev")
        print_info("")
        print_info("Falling back to basic site scanning...")
        handle_site_basic(url, output_dir, db)
        return

    print_info("Mapping website URLs with Firecrawl...")

    try:
        # Map the site to discover URLs
        urls = map_site(url, api_key)

        if not urls:
            print_warning("No URLs found on site.")
            return

        # Build items list for display
        items = [{"title": u, "url": u} for u in urls]

        # Show found URLs
        domain = urlparse(url).netloc
        show_found_items("Website", domain, items, "pages")

        # Confirm download
        choice = confirm_download(len(items), "pages")
        if choice == "none":
            print_info("Download cancelled.")
            return

        if choice == "select":
            indices = select_items(items)
            urls = [items[i]['url'] for i in indices]

        # Crawl the selected URLs
        crawl_site(urls, url, output_dir, db, api_key)

    except Exception as e:
        print_error(f"Failed to crawl site: {e}")


def map_site(url: str, api_key: str, limit: int = 500) -> List[str]:
    """Map a website to discover all URLs."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "url": url,
        "limit": limit,
    }

    response = requests.post(
        f"{FIRECRAWL_API_URL}/map",
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Map failed: {response.text}")

    result = response.json()

    if not result.get('success'):
        raise Exception(f"Map failed: {result.get('error', 'Unknown error')}")

    return result.get('links', [])


def crawl_site(
    urls: List[str],
    base_url: str,
    output_dir: Path,
    db: Database,
    api_key: str
) -> None:
    """Crawl and save pages from a website."""
    domain = urlparse(base_url).netloc.replace('www.', '')
    source_folder = get_source_folder(output_dir, sanitize_filename(domain))

    print_info(f"Archiving {len(urls)} pages to {source_folder}")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # Start batch scrape
    data = {
        "urls": urls,
        "formats": ["markdown", "html"],
    }

    response = requests.post(
        f"{FIRECRAWL_API_URL}/batch/scrape",
        headers=headers,
        json=data,
        timeout=60
    )

    if response.status_code != 200:
        raise Exception(f"Batch scrape failed: {response.text}")

    result = response.json()
    job_id = result.get('id')

    if not job_id:
        raise Exception("No job ID returned")

    print_info(f"Batch job started: {job_id}")

    # Poll for completion
    completed_urls = set()
    while True:
        status_response = requests.get(
            f"{FIRECRAWL_API_URL}/batch/scrape/{job_id}",
            headers=headers,
            timeout=30
        )

        if status_response.status_code != 200:
            raise Exception(f"Status check failed: {status_response.text}")

        status = status_response.json()
        current_status = status.get('status', 'unknown')

        completed = status.get('completed', 0)
        total = status.get('total', len(urls))

        console.print(f"\rProgress: {completed}/{total} pages", end="")

        # Process any completed data
        if 'data' in status:
            for page_data in status['data']:
                page_url = page_data.get('metadata', {}).get('url', '')
                if page_url and page_url not in completed_urls:
                    completed_urls.add(page_url)
                    save_page(page_data, source_folder, domain, db)

        if current_status == 'completed':
            console.print()  # New line
            break
        elif current_status == 'failed':
            console.print()
            raise Exception(f"Batch scrape failed: {status.get('error', 'Unknown')}")

        time.sleep(2)

    # Save site index
    index_path = source_folder / "index.json"
    index_data = {
        "domain": domain,
        "base_url": base_url,
        "archived_at": datetime.now().isoformat(),
        "page_count": len(completed_urls),
        "pages": list(completed_urls),
    }
    index_path.write_text(json.dumps(index_data, indent=2))

    print_success(f"Site archive complete: {domain}")
    print_info(f"  - {len(completed_urls)} pages saved")
    print_info(f"  - Location: {source_folder}")


def save_page(page_data: dict, folder: Path, domain: str, db: Database) -> None:
    """Save a single scraped page."""
    metadata = page_data.get('metadata', {})
    url = metadata.get('url', 'unknown')
    title = metadata.get('title', 'Unknown Page')

    # Create safe filename from URL path
    parsed = urlparse(url)
    path = parsed.path.strip('/') or 'index'
    safe_name = sanitize_filename(path.replace('/', '_'))[:100]

    # Track in database
    dl_id = db.add_download(
        url=url,
        content_type="site",
        source_name=domain,
        title=title,
        metadata=metadata
    )

    try:
        db.update_status(dl_id, "downloading")

        # Save markdown
        md_content = page_data.get('markdown', '')
        if md_content:
            md_path = folder / f"{safe_name}.md"
            full_md = f"# {title}\n\nSource: {url}\n\n---\n\n{md_content}"
            md_path.write_text(full_md, encoding='utf-8')

        # Save HTML
        html_content = page_data.get('html', '')
        if html_content:
            html_path = folder / f"{safe_name}.html"
            html_path.write_text(html_content, encoding='utf-8')

        db.update_status(dl_id, "complete", str(folder / f"{safe_name}.md"))

    except Exception as e:
        db.update_status(dl_id, "error", error_message=str(e))


def handle_site_basic(url: str, output_dir: Path, db: Database) -> None:
    """Basic site handling without Firecrawl (single page only)."""
    print_info("Basic mode: Archiving single page only.")
    print_info("For full site crawling, set up Firecrawl API key.")

    from .article import handle_article
    handle_article(url, output_dir, db)
