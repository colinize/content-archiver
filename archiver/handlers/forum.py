"""Forum handler for thread extraction with pagination support."""

import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
from urllib.parse import urljoin, urlparse, parse_qs

import requests
from bs4 import BeautifulSoup

from ..core.database import Database
from ..core.downloader import sanitize_filename, get_source_folder
from ..core.progress import (
    console,
    print_info,
    print_success,
    print_error,
    print_warning,
)


# Common forum patterns for post extraction
FORUM_PATTERNS = {
    'reddit': {
        'post_selector': '.thing.comment, .Comment',
        'author_selector': '.author, [data-testid="comment_author_link"]',
        'content_selector': '.md, [data-testid="comment"]',
        'date_selector': 'time',
    },
    'discourse': {
        'post_selector': '.topic-post',
        'author_selector': '.username',
        'content_selector': '.cooked',
        'date_selector': '.post-date',
    },
    'phpbb': {
        'post_selector': '.post',
        'author_selector': '.username, .postauthor',
        'content_selector': '.content, .postbody',
        'date_selector': '.postdate, time',
    },
    'vbulletin': {
        'post_selector': '.postcontainer, .b-post',
        'author_selector': '.username, .b-post__username',
        'content_selector': '.postcontent, .b-post__content',
        'date_selector': '.postdate, .b-post__date',
    },
    'generic': {
        'post_selector': 'article, .post, .comment, .message',
        'author_selector': '.author, .username, .user, .poster',
        'content_selector': '.content, .body, .text, .message-body, p',
        'date_selector': 'time, .date, .timestamp',
    },
}


def handle_forum(url: str, output_dir: Path, db: Database) -> None:
    """Handle forum thread URLs."""
    print_info("Fetching forum thread...")

    try:
        # Detect forum type
        forum_type = detect_forum_type(url)
        print_info(f"Forum type: {forum_type}")

        # Fetch all pages
        all_posts = []
        current_url = url
        page_num = 1
        seen_urls = set()

        while current_url and current_url not in seen_urls:
            seen_urls.add(current_url)
            print_info(f"Fetching page {page_num}...")

            response = requests.get(current_url, timeout=30, headers={
                'User-Agent': 'ContentArchiver/1.0'
            })
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # Extract thread title
            if page_num == 1:
                thread_title = extract_thread_title(soup, url)

            # Extract posts from this page
            posts = extract_posts(soup, forum_type)
            if not posts:
                if page_num == 1:
                    print_warning("No posts found on page. Trying generic extraction...")
                    posts = extract_posts(soup, 'generic')

            all_posts.extend(posts)

            # Find next page
            next_url = find_next_page(soup, current_url)
            if next_url and next_url != current_url:
                current_url = next_url
                page_num += 1
            else:
                break

        if not all_posts:
            print_warning("No posts could be extracted from this thread.")
            return

        print_info(f"Found {len(all_posts)} posts across {page_num} page(s)")

        # Save the thread
        save_thread(all_posts, thread_title, url, output_dir, db)

    except Exception as e:
        print_error(f"Failed to process forum thread: {e}")


def detect_forum_type(url: str) -> str:
    """Detect the forum platform from URL."""
    url_lower = url.lower()

    if 'reddit.com' in url_lower:
        return 'reddit'
    elif any(x in url_lower for x in ['discourse', 'community.', 'forum.', 'discuss.']):
        return 'discourse'
    elif 'phpbb' in url_lower or 'viewtopic.php' in url_lower:
        return 'phpbb'
    elif 'vbulletin' in url_lower or 'showthread.php' in url_lower:
        return 'vbulletin'
    else:
        return 'generic'


def extract_thread_title(soup: BeautifulSoup, url: str) -> str:
    """Extract thread title from page."""
    # Try common title selectors
    selectors = [
        'h1.title', 'h1', '.thread-title', '.topic-title',
        '#thread-title', '.post-title', 'title'
    ]

    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            title = element.get_text(strip=True)
            # Clean up title
            title = re.sub(r'\s*[-|]\s*.*$', '', title)  # Remove site name suffix
            if title and len(title) > 3:
                return title[:200]  # Limit length

    # Fallback to URL-based title
    parsed = urlparse(url)
    path_parts = [p for p in parsed.path.split('/') if p]
    if path_parts:
        return path_parts[-1].replace('-', ' ').replace('_', ' ')[:200]

    return 'Unknown Thread'


def extract_posts(soup: BeautifulSoup, forum_type: str) -> List[Dict]:
    """Extract posts from a forum page."""
    patterns = FORUM_PATTERNS.get(forum_type, FORUM_PATTERNS['generic'])
    posts = []

    # Find all post containers
    post_elements = soup.select(patterns['post_selector'])

    for i, post_el in enumerate(post_elements):
        try:
            # Extract author
            author_el = post_el.select_one(patterns['author_selector'])
            author = author_el.get_text(strip=True) if author_el else 'Unknown'

            # Extract content
            content_el = post_el.select_one(patterns['content_selector'])
            if not content_el:
                # Try getting all text from post
                content_el = post_el

            # Get text content and clean it
            content = content_el.get_text(separator='\n', strip=True)

            # Also get HTML for rich content
            content_html = str(content_el) if content_el else ''

            # Extract date
            date_el = post_el.select_one(patterns['date_selector'])
            date_str = ''
            if date_el:
                date_str = date_el.get('datetime', '') or date_el.get_text(strip=True)

            # Extract any images
            images = []
            for img in post_el.find_all('img'):
                src = img.get('src') or img.get('data-src')
                if src and not any(x in src.lower() for x in ['avatar', 'emoji', 'icon', 'badge']):
                    images.append(src)

            if content and len(content) > 10:  # Skip empty/very short posts
                posts.append({
                    'index': i + 1,
                    'author': author[:100],
                    'date': date_str[:50],
                    'content': content,
                    'content_html': content_html,
                    'images': images,
                })

        except Exception:
            continue

    return posts


def find_next_page(soup: BeautifulSoup, current_url: str) -> Optional[str]:
    """Find the next page URL in pagination."""
    # Common next page patterns
    next_selectors = [
        'a.next', 'a[rel="next"]', '.pagination a.next',
        '.pager a.next', 'a:contains("Next")', 'a:contains("»")',
        '.page-link[aria-label="Next"]', 'a.pageNav-jump--next',
    ]

    for selector in next_selectors:
        try:
            next_link = soup.select_one(selector)
            if next_link and next_link.get('href'):
                return urljoin(current_url, next_link['href'])
        except Exception:
            continue

    # Try finding numbered pagination and get next number
    current_page = soup.select_one('.pagination .active, .page-item.active, .current')
    if current_page:
        next_sibling = current_page.find_next_sibling('a')
        if next_sibling and next_sibling.get('href'):
            return urljoin(current_url, next_sibling['href'])

    return None


def save_thread(
    posts: List[Dict],
    title: str,
    url: str,
    output_dir: Path,
    db: Database
) -> None:
    """Save extracted thread to files."""
    # Create source folder
    safe_title = sanitize_filename(title)
    source_folder = get_source_folder(output_dir, safe_title)

    print_info(f"Saving thread to {source_folder}")

    # Track in database
    dl_id = db.add_download(
        url=url,
        content_type="forum",
        source_name=title,
        title=title,
        metadata={"post_count": len(posts)}
    )

    try:
        db.update_status(dl_id, "downloading")

        # Save as JSON (full data)
        json_path = source_folder / "thread.json"
        thread_data = {
            "title": title,
            "url": url,
            "extracted_at": datetime.now().isoformat(),
            "post_count": len(posts),
            "posts": posts,
        }
        json_path.write_text(json.dumps(thread_data, indent=2, ensure_ascii=False))

        # Save as Markdown (readable)
        md_path = source_folder / "thread.md"
        md_content = generate_markdown(title, url, posts)
        md_path.write_text(md_content, encoding='utf-8')

        # Save as HTML (styled)
        html_path = source_folder / "thread.html"
        html_content = generate_html(title, url, posts)
        html_path.write_text(html_content, encoding='utf-8')

        # Download images
        image_count = download_thread_images(posts, source_folder, url)

        db.update_status(dl_id, "complete", str(md_path))
        print_success(f"Saved thread: {title}")
        print_info(f"  - {len(posts)} posts")
        print_info(f"  - {image_count} images")
        print_info(f"  - Files: thread.md, thread.html, thread.json")

    except Exception as e:
        db.update_status(dl_id, "error", error_message=str(e))
        print_error(f"Error saving thread: {e}")


def generate_markdown(title: str, url: str, posts: List[Dict]) -> str:
    """Generate Markdown version of thread."""
    lines = [
        f"# {title}",
        f"",
        f"Source: {url}",
        f"Posts: {len(posts)}",
        f"",
        "---",
        "",
    ]

    for post in posts:
        lines.append(f"## Post #{post['index']} by {post['author']}")
        if post['date']:
            lines.append(f"*{post['date']}*")
        lines.append("")
        lines.append(post['content'])
        if post['images']:
            lines.append("")
            for img in post['images']:
                lines.append(f"![image]({img})")
        lines.append("")
        lines.append("---")
        lines.append("")

    return '\n'.join(lines)


def generate_html(title: str, url: str, posts: List[Dict]) -> str:
    """Generate styled HTML version of thread."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #333;
        }}
        h1 {{
            border-bottom: 2px solid #333;
            padding-bottom: 10px;
        }}
        .meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }}
        .post {{
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            background: #fafafa;
        }}
        .post-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
            font-size: 0.9em;
        }}
        .author {{
            font-weight: bold;
            color: #1a73e8;
        }}
        .date {{
            color: #666;
        }}
        .content {{
            white-space: pre-wrap;
        }}
        .images img {{
            max-width: 100%;
            margin-top: 10px;
            border-radius: 4px;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="meta">
        <p>Source: <a href="{url}">{url}</a></p>
        <p>Posts: {len(posts)}</p>
    </div>
"""

    for post in posts:
        images_html = ''.join(f'<img src="{img}" alt="image">' for img in post['images'])
        html += f"""
    <div class="post">
        <div class="post-header">
            <span class="author">{post['author']}</span>
            <span class="date">{post['date']}</span>
        </div>
        <div class="content">{post['content']}</div>
        <div class="images">{images_html}</div>
    </div>
"""

    html += """
</body>
</html>
"""
    return html


def download_thread_images(posts: List[Dict], folder: Path, base_url: str) -> int:
    """Download images from thread posts."""
    images_folder = folder / "images"
    downloaded = 0

    for post in posts:
        for img_url in post['images']:
            try:
                full_url = urljoin(base_url, img_url)
                response = requests.get(full_url, timeout=30, headers={
                    'User-Agent': 'ContentArchiver/1.0'
                })
                response.raise_for_status()

                # Create images folder on first image
                if not images_folder.exists():
                    images_folder.mkdir(parents=True)

                # Generate filename
                filename = f"post{post['index']}_{downloaded + 1}"
                ext = Path(urlparse(img_url).path).suffix or '.jpg'
                filepath = images_folder / f"{filename}{ext}"

                filepath.write_bytes(response.content)
                downloaded += 1

            except Exception:
                continue

    return downloaded
