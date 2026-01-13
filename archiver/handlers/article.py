"""Article handler for content extraction."""

import re
import json
from pathlib import Path
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

try:
    from readability import Document
    READABILITY_AVAILABLE = True
except ImportError:
    READABILITY_AVAILABLE = False

try:
    from markdownify import markdownify as md
    MARKDOWNIFY_AVAILABLE = True
except ImportError:
    MARKDOWNIFY_AVAILABLE = False

from ..core.database import Database
from ..core.downloader import sanitize_filename, get_source_folder
from ..core.progress import (
    print_info,
    print_success,
    print_error,
    print_warning,
)


# Audio patterns to detect podcast pages
AUDIO_EXTENSIONS = ['.mp3', '.m4a', '.wav', '.ogg', '.aac']


def handle_article(url: str, output_dir: Path, db: Database) -> None:
    """Handle article/blog post URLs."""
    print_info("Fetching page content...")

    try:
        response = requests.get(url, timeout=30, headers={
            'User-Agent': 'ContentArchiver/1.0'
        })
        response.raise_for_status()

        # Check if page contains audio files - if so, redirect to podcast handler
        html_text = response.text.lower()
        has_audio = any(ext in html_text for ext in AUDIO_EXTENSIONS)

        if has_audio:
            print_info("Audio files detected - handling as podcast page...")
            from .podcast import handle_audio_webpage
            handle_audio_webpage(url, output_dir, db)
            return

        # Extract article content
        extract_article(response.text, url, output_dir, db)

    except Exception as e:
        print_error(f"Failed to fetch page: {e}")


def extract_article(html: str, url: str, output_dir: Path, db: Database) -> None:
    """Extract and save article content."""
    soup = BeautifulSoup(html, 'lxml')

    # Get page title
    title = extract_title(soup)
    print_info(f"Article: {title}")

    # Extract main content
    if READABILITY_AVAILABLE:
        doc = Document(html)
        content_html = doc.summary()
        # Get better title from readability if available
        if doc.title():
            title = doc.title()
    else:
        print_warning("readability-lxml not installed. Using basic extraction.")
        content_html = extract_content_basic(soup)

    # Clean up the content
    content_soup = BeautifulSoup(content_html, 'lxml')

    # Extract metadata
    metadata = extract_metadata(soup, url)

    # Convert to markdown if available
    if MARKDOWNIFY_AVAILABLE:
        content_md = md(content_html, heading_style="ATX", strip=['script', 'style'])
        content_md = clean_markdown(content_md)
    else:
        content_md = content_soup.get_text(separator='\n\n', strip=True)

    # Get text content
    content_text = content_soup.get_text(separator='\n\n', strip=True)

    # Extract images
    images = extract_images(content_soup, url)

    # Save the article
    save_article(
        title=title,
        url=url,
        content_html=content_html,
        content_md=content_md,
        content_text=content_text,
        metadata=metadata,
        images=images,
        output_dir=output_dir,
        db=db
    )


def extract_title(soup: BeautifulSoup) -> str:
    """Extract article title from page."""
    # Try common title selectors in order of preference
    selectors = [
        'h1.entry-title', 'h1.post-title', 'h1.article-title',
        'article h1', '.post h1', 'h1', 'title'
    ]

    for selector in selectors:
        element = soup.select_one(selector)
        if element:
            title = element.get_text(strip=True)
            # Clean up title (remove site name suffix)
            title = re.sub(r'\s*[-|–—]\s*[^-|–—]+$', '', title)
            if title and len(title) > 3:
                return title[:200]

    return 'Unknown Article'


def extract_content_basic(soup: BeautifulSoup) -> str:
    """Basic content extraction when readability is not available."""
    # Remove unwanted elements
    for tag in soup.find_all(['script', 'style', 'nav', 'header', 'footer', 'aside', 'form']):
        tag.decompose()

    # Try to find main content area
    content_selectors = [
        'article', '.post-content', '.entry-content', '.article-content',
        '.content', 'main', '#content', '.post-body'
    ]

    for selector in content_selectors:
        content = soup.select_one(selector)
        if content:
            return str(content)

    # Fallback to body
    body = soup.find('body')
    if body:
        return str(body)

    return str(soup)


def extract_metadata(soup: BeautifulSoup, url: str) -> dict:
    """Extract article metadata."""
    metadata = {
        'url': url,
        'domain': urlparse(url).netloc,
        'extracted_at': datetime.now().isoformat(),
    }

    # Try to find author
    author_selectors = [
        'meta[name="author"]', '.author', '.byline', '[rel="author"]',
        '.post-author', '.entry-author'
    ]
    for selector in author_selectors:
        el = soup.select_one(selector)
        if el:
            author = el.get('content') or el.get_text(strip=True)
            if author:
                metadata['author'] = author[:100]
                break

    # Try to find publish date
    date_selectors = [
        'meta[property="article:published_time"]',
        'time[datetime]', '.date', '.post-date', '.published'
    ]
    for selector in date_selectors:
        el = soup.select_one(selector)
        if el:
            date = el.get('content') or el.get('datetime') or el.get_text(strip=True)
            if date:
                metadata['published'] = date[:50]
                break

    # Try to find description
    desc_el = soup.select_one('meta[name="description"]')
    if desc_el:
        metadata['description'] = desc_el.get('content', '')[:500]

    # Get Open Graph data
    og_title = soup.select_one('meta[property="og:title"]')
    if og_title:
        metadata['og_title'] = og_title.get('content', '')

    og_image = soup.select_one('meta[property="og:image"]')
    if og_image:
        metadata['og_image'] = og_image.get('content', '')

    return metadata


def extract_images(soup: BeautifulSoup, base_url: str) -> list:
    """Extract images from content."""
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            # Skip tiny images (likely icons)
            width = img.get('width', '999')
            height = img.get('height', '999')
            try:
                if int(width) < 50 or int(height) < 50:
                    continue
            except ValueError:
                pass

            full_url = urljoin(base_url, src)
            alt = img.get('alt', '')
            images.append({'url': full_url, 'alt': alt})

    return images


def clean_markdown(text: str) -> str:
    """Clean up markdown output."""
    # Remove excessive blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove trailing whitespace from lines
    text = '\n'.join(line.rstrip() for line in text.split('\n'))
    return text.strip()


def save_article(
    title: str,
    url: str,
    content_html: str,
    content_md: str,
    content_text: str,
    metadata: dict,
    images: list,
    output_dir: Path,
    db: Database
) -> None:
    """Save article to files."""
    # Create source folder based on domain
    domain = urlparse(url).netloc.replace('www.', '')
    safe_title = sanitize_filename(title)
    source_folder = get_source_folder(output_dir, domain)

    print_info(f"Saving article to {source_folder}")

    # Track in database
    dl_id = db.add_download(
        url=url,
        content_type="article",
        source_name=domain,
        title=title,
        metadata=metadata
    )

    try:
        db.update_status(dl_id, "downloading")

        # Save as Markdown
        md_path = source_folder / f"{safe_title}.md"
        md_content = f"""# {title}

Source: {url}
"""
        if metadata.get('author'):
            md_content += f"Author: {metadata['author']}\n"
        if metadata.get('published'):
            md_content += f"Published: {metadata['published']}\n"

        md_content += f"""
---

{content_md}
"""
        md_path.write_text(md_content, encoding='utf-8')

        # Save as styled HTML
        html_path = source_folder / f"{safe_title}.html"
        styled_html = generate_styled_html(title, url, content_html, metadata)
        html_path.write_text(styled_html, encoding='utf-8')

        # Save metadata as JSON
        json_path = source_folder / f"{safe_title}.json"
        article_data = {
            'title': title,
            'url': url,
            'metadata': metadata,
            'images': images,
            'content_text': content_text[:10000],  # Truncate for JSON
        }
        json_path.write_text(json.dumps(article_data, indent=2, ensure_ascii=False))

        # Download images
        image_count = download_article_images(images, source_folder, safe_title)

        db.update_status(dl_id, "complete", str(md_path))
        print_success(f"Saved article: {title}")
        print_info(f"  - Files: {safe_title}.md, .html, .json")
        if image_count:
            print_info(f"  - {image_count} images downloaded")

    except Exception as e:
        db.update_status(dl_id, "error", error_message=str(e))
        print_error(f"Error saving article: {e}")


def generate_styled_html(title: str, url: str, content: str, metadata: dict) -> str:
    """Generate a styled HTML file for the article."""
    author = metadata.get('author', '')
    published = metadata.get('published', '')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            font-family: Georgia, 'Times New Roman', serif;
            max-width: 700px;
            margin: 0 auto;
            padding: 40px 20px;
            line-height: 1.8;
            color: #333;
            background: #fafafa;
        }}
        h1 {{
            font-size: 2em;
            line-height: 1.2;
            margin-bottom: 0.5em;
        }}
        .meta {{
            color: #666;
            font-size: 0.9em;
            margin-bottom: 2em;
            padding-bottom: 1em;
            border-bottom: 1px solid #ddd;
        }}
        .meta a {{
            color: #1a73e8;
        }}
        article {{
            font-size: 1.1em;
        }}
        article img {{
            max-width: 100%;
            height: auto;
            margin: 1em 0;
        }}
        article a {{
            color: #1a73e8;
        }}
        blockquote {{
            border-left: 3px solid #ddd;
            margin: 1em 0;
            padding-left: 1em;
            color: #666;
        }}
        pre, code {{
            background: #f0f0f0;
            padding: 0.2em 0.4em;
            border-radius: 3px;
            font-family: 'Menlo', monospace;
            font-size: 0.9em;
        }}
        pre {{
            padding: 1em;
            overflow-x: auto;
        }}
    </style>
</head>
<body>
    <h1>{title}</h1>
    <div class="meta">
        <p>Source: <a href="{url}">{url}</a></p>
        {f'<p>Author: {author}</p>' if author else ''}
        {f'<p>Published: {published}</p>' if published else ''}
    </div>
    <article>
        {content}
    </article>
</body>
</html>
"""


def download_article_images(images: list, folder: Path, article_name: str) -> int:
    """Download images from article."""
    if not images:
        return 0

    images_folder = folder / "images"
    downloaded = 0

    for i, img in enumerate(images[:20], 1):  # Limit to 20 images
        try:
            response = requests.get(img['url'], timeout=30, headers={
                'User-Agent': 'ContentArchiver/1.0'
            })
            response.raise_for_status()

            # Create images folder on first image
            if not images_folder.exists():
                images_folder.mkdir(parents=True)

            # Generate filename
            ext = Path(urlparse(img['url']).path).suffix or '.jpg'
            if ext.lower() not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
                ext = '.jpg'
            filepath = images_folder / f"{article_name}_{i}{ext}"

            filepath.write_bytes(response.content)
            downloaded += 1

        except Exception:
            continue

    return downloaded
