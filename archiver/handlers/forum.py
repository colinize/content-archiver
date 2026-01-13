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

        # Reddit needs special handling via JSON API
        if forum_type == 'reddit':
            handle_reddit_thread(url, output_dir, db)
            return

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


def handle_reddit_thread(url: str, output_dir: Path, db: Database) -> None:
    """Handle Reddit threads using the JSON API."""
    print_info("Fetching Reddit thread via API...")

    try:
        # Convert URL to JSON endpoint
        # Remove trailing slash and add .json
        json_url = url.rstrip('/') + '.json'

        response = requests.get(json_url, timeout=30, headers={
            'User-Agent': 'ContentArchiver/1.0'
        })
        response.raise_for_status()

        data = response.json()

        # Reddit returns [post_data, comments_data]
        if not isinstance(data, list) or len(data) < 2:
            print_error("Unexpected Reddit API response format")
            return

        # Extract post info
        post_data = data[0]['data']['children'][0]['data']
        title = post_data.get('title', 'Unknown Thread')
        author = post_data.get('author', 'Unknown')
        selftext = post_data.get('selftext', '')
        created_utc = post_data.get('created_utc', 0)
        subreddit = post_data.get('subreddit', 'reddit')
        score = post_data.get('score', 0)
        post_url = post_data.get('url', '')

        # Format date
        post_date = datetime.fromtimestamp(created_utc).strftime('%Y-%m-%d %H:%M') if created_utc else ''

        # Build posts list starting with the OP
        posts = [{
            'index': 0,
            'author': author,
            'date': post_date,
            'content': selftext or f"[Link post: {post_url}]",
            'content_html': selftext,
            'images': extract_reddit_images(post_data),
            'score': score,
            'is_op': True,
        }]

        # Extract comments
        comments_data = data[1]['data']['children']
        comment_index = 1

        def extract_comments(comments, depth=0):
            nonlocal comment_index
            for comment in comments:
                if comment.get('kind') != 't1':  # t1 = comment
                    continue

                c_data = comment.get('data', {})
                c_author = c_data.get('author', '[deleted]')
                c_body = c_data.get('body', '')
                c_created = c_data.get('created_utc', 0)
                c_score = c_data.get('score', 0)

                if c_body and c_author != '[deleted]':
                    c_date = datetime.fromtimestamp(c_created).strftime('%Y-%m-%d %H:%M') if c_created else ''

                    posts.append({
                        'index': comment_index,
                        'author': c_author,
                        'date': c_date,
                        'content': c_body,
                        'content_html': c_body,
                        'images': [],
                        'score': c_score,
                        'depth': depth,
                    })
                    comment_index += 1

                # Recursively get replies
                replies = c_data.get('replies')
                if isinstance(replies, dict):
                    reply_children = replies.get('data', {}).get('children', [])
                    extract_comments(reply_children, depth + 1)

        extract_comments(comments_data)

        print_info(f"Found {len(posts)} posts (1 OP + {len(posts) - 1} comments)")

        # Save the thread
        save_reddit_thread(posts, title, subreddit, url, output_dir, db)

    except Exception as e:
        print_error(f"Failed to fetch Reddit thread: {e}")


def extract_reddit_images(post_data: dict) -> list:
    """Extract image URLs from Reddit post data."""
    images = []

    # Check for direct image URL
    url = post_data.get('url', '')
    if any(ext in url.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']):
        images.append(url)

    # Check for gallery
    if post_data.get('is_gallery'):
        media_metadata = post_data.get('media_metadata', {})
        for item_id, item_data in media_metadata.items():
            if item_data.get('status') == 'valid':
                # Get the highest resolution image
                if 's' in item_data:
                    img_url = item_data['s'].get('u', '').replace('&amp;', '&')
                    if img_url:
                        images.append(img_url)

    # Check for preview images
    preview = post_data.get('preview', {})
    if preview and 'images' in preview:
        for img in preview['images']:
            source = img.get('source', {})
            img_url = source.get('url', '').replace('&amp;', '&')
            if img_url:
                images.append(img_url)

    return images


def save_reddit_thread(
    posts: List[Dict],
    title: str,
    subreddit: str,
    url: str,
    output_dir: Path,
    db: Database
) -> None:
    """Save Reddit thread to files."""
    safe_title = sanitize_filename(f"r_{subreddit}_{title[:50]}")
    source_folder = get_source_folder(output_dir, safe_title, category="forums")

    print_info(f"Saving thread to {source_folder}")

    # Track in database
    dl_id = db.add_download(
        url=url,
        content_type="forum",
        source_name=f"r/{subreddit}",
        title=title,
        metadata={"post_count": len(posts), "subreddit": subreddit}
    )

    try:
        db.update_status(dl_id, "downloading")

        # Save as JSON
        json_path = source_folder / "thread.json"
        thread_data = {
            "title": title,
            "subreddit": subreddit,
            "url": url,
            "extracted_at": datetime.now().isoformat(),
            "post_count": len(posts),
            "posts": posts,
        }
        json_path.write_text(json.dumps(thread_data, indent=2, ensure_ascii=False))

        # Save as Markdown
        md_path = source_folder / "thread.md"
        md_content = generate_reddit_markdown(title, subreddit, url, posts)
        md_path.write_text(md_content, encoding='utf-8')

        # Save as HTML
        html_path = source_folder / "thread.html"
        html_content = generate_reddit_html(title, subreddit, url, posts)
        html_path.write_text(html_content, encoding='utf-8')

        # Download images from OP
        image_count = 0
        if posts and posts[0].get('images'):
            image_count = download_thread_images(posts[:1], source_folder, url)

        db.update_status(dl_id, "complete", str(md_path))
        print_success(f"Saved thread: {title}")
        print_info(f"  - {len(posts)} posts ({len(posts) - 1} comments)")
        if image_count:
            print_info(f"  - {image_count} images")
        print_info(f"  - Files: thread.md, thread.html, thread.json")

    except Exception as e:
        db.update_status(dl_id, "error", error_message=str(e))
        print_error(f"Error saving thread: {e}")


def generate_reddit_markdown(title: str, subreddit: str, url: str, posts: List[Dict]) -> str:
    """Generate Markdown for Reddit thread."""
    lines = [
        f"# {title}",
        f"",
        f"**Subreddit:** r/{subreddit}",
        f"**Source:** {url}",
        f"**Comments:** {len(posts) - 1}",
        f"",
        "---",
        "",
    ]

    for post in posts:
        if post.get('is_op'):
            lines.append(f"## Original Post by u/{post['author']}")
            lines.append(f"*{post['date']}* | Score: {post.get('score', 0)}")
        else:
            indent = "  " * post.get('depth', 0)
            lines.append(f"{indent}### u/{post['author']}")
            lines.append(f"{indent}*{post['date']}* | Score: {post.get('score', 0)}")

        lines.append("")
        # Indent content for nested comments
        content = post['content']
        if post.get('depth', 0) > 0:
            content = '\n'.join('  ' * post['depth'] + line for line in content.split('\n'))
        lines.append(content)

        if post.get('images'):
            lines.append("")
            for img in post['images']:
                lines.append(f"![image]({img})")

        lines.append("")
        lines.append("---")
        lines.append("")

    return '\n'.join(lines)


def generate_reddit_html(title: str, subreddit: str, url: str, posts: List[Dict]) -> str:
    """Generate styled HTML for Reddit thread."""
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title} - r/{subreddit}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
            color: #1a1a1b;
            background: #dae0e6;
        }}
        .thread {{
            background: white;
            border-radius: 4px;
            padding: 20px;
        }}
        h1 {{
            font-size: 1.5em;
            margin-bottom: 0.5em;
        }}
        .meta {{
            color: #7c7c7c;
            font-size: 0.85em;
            margin-bottom: 15px;
        }}
        .meta a {{
            color: #0079d3;
        }}
        .post {{
            border-left: 3px solid #ccc;
            padding: 10px 15px;
            margin: 10px 0;
            background: #f8f9fa;
        }}
        .post.op {{
            border-left-color: #0079d3;
            background: #f0f7ff;
        }}
        .post-header {{
            font-size: 0.85em;
            color: #7c7c7c;
            margin-bottom: 8px;
        }}
        .author {{
            color: #1a1a1b;
            font-weight: 500;
        }}
        .score {{
            color: #ff4500;
        }}
        .content {{
            white-space: pre-wrap;
        }}
        .images img {{
            max-width: 100%;
            margin-top: 10px;
            border-radius: 4px;
        }}
        .depth-1 {{ margin-left: 20px; }}
        .depth-2 {{ margin-left: 40px; }}
        .depth-3 {{ margin-left: 60px; }}
        .depth-4 {{ margin-left: 80px; }}
    </style>
</head>
<body>
    <div class="thread">
        <h1>{title}</h1>
        <div class="meta">
            <strong>r/{subreddit}</strong> |
            <a href="{url}">Original Thread</a> |
            {len(posts) - 1} comments
        </div>
"""

    for post in posts:
        depth_class = f"depth-{min(post.get('depth', 0), 4)}" if not post.get('is_op') else ''
        op_class = 'op' if post.get('is_op') else ''
        images_html = ''.join(f'<img src="{img}" alt="image">' for img in post.get('images', []))

        html += f"""
        <div class="post {op_class} {depth_class}">
            <div class="post-header">
                <span class="author">u/{post['author']}</span> |
                <span class="date">{post['date']}</span> |
                <span class="score">{post.get('score', 0)} points</span>
            </div>
            <div class="content">{post['content']}</div>
            <div class="images">{images_html}</div>
        </div>
"""

    html += """
    </div>
</body>
</html>
"""
    return html


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
    source_folder = get_source_folder(output_dir, safe_title, category="forums")

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
