"""Auto-detect content type from URLs."""

import re
from urllib.parse import urlparse
from typing import Literal, Optional
from enum import Enum


class ContentType(Enum):
    """Types of content we can archive."""
    YOUTUBE = "youtube"
    FACEBOOK = "facebook"
    TWITCH = "twitch"
    PODCAST = "podcast"
    FORUM = "forum"
    ARTICLE = "article"
    SITE = "site"
    UNKNOWN = "unknown"


# YouTube patterns
YOUTUBE_PATTERNS = [
    r'youtube\.com/watch',
    r'youtube\.com/playlist',
    r'youtube\.com/channel',
    r'youtube\.com/@',
    r'youtube\.com/c/',
    r'youtube\.com/user/',
    r'youtu\.be/',
    r'youtube\.com/shorts/',
]

# Facebook patterns
FACEBOOK_PATTERNS = [
    r'facebook\.com/.+/videos',
    r'facebook\.com/watch',
    r'facebook\.com/reel',
    r'facebook\.com/.+/posts/',
    r'fb\.watch/',
    r'facebook\.com/video\.php',
]

# Twitch patterns
TWITCH_PATTERNS = [
    r'twitch\.tv/videos/',          # VODs: twitch.tv/videos/123456789
    r'twitch\.tv/[^/]+/video/',     # VODs: twitch.tv/channel/video/123456789
    r'twitch\.tv/[^/]+/clip/',      # Clips: twitch.tv/channel/clip/ClipName
    r'clips\.twitch\.tv/',          # Clips: clips.twitch.tv/ClipName
    r'twitch\.tv/[^/]+/clips',      # Channel clips page
    r'twitch\.tv/[^/]+$',           # Channel page (for listing VODs)
]

# Podcast platform patterns
PODCAST_PATTERNS = [
    r'open\.spotify\.com/show',
    r'open\.spotify\.com/episode',
    r'podcasts\.apple\.com',
    r'anchor\.fm',
    r'soundcloud\.com',
    r'podbean\.com',
    r'buzzsprout\.com',
    r'libsyn\.com',
    r'spreaker\.com',
    r'simplecast\.com',
    r'zencastr\.com/f/',
    r'patreon\.com/rss/',  # Patreon podcast RSS feeds
    r'/feed\.xml',
    r'/rss\.xml',
    r'/feed/?$',
    r'/rss/?$',
    r'/rss/',  # RSS anywhere in path (not just at end)
]

# Forum patterns
FORUM_PATTERNS = [
    r'reddit\.com/r/[^/]+/comments/',
    r'old\.reddit\.com/r/[^/]+/comments/',
    r'forum\.',
    r'forums\.',
    r'/forum/',
    r'/forums/',
    r'/thread/',
    r'/threads/',
    r'discourse\.',
    r'/t/[^/]+/\d+',  # Discourse pattern
    r'viewtopic\.php',  # phpBB
    r'showthread\.php',  # vBulletin
]

# Patterns that suggest it's a full site to crawl
SITE_PATTERNS = [
    # Just a domain with no path or root path
    r'^https?://[^/]+/?$',
]


def detect_content_type(url: str) -> ContentType:
    """
    Detect the content type from a URL.

    Returns the most likely content type based on URL patterns.
    """
    url_lower = url.lower()

    # Check YouTube first (most specific)
    for pattern in YOUTUBE_PATTERNS:
        if re.search(pattern, url_lower):
            return ContentType.YOUTUBE

    # Check Facebook
    for pattern in FACEBOOK_PATTERNS:
        if re.search(pattern, url_lower):
            return ContentType.FACEBOOK

    # Check Twitch
    for pattern in TWITCH_PATTERNS:
        if re.search(pattern, url_lower):
            return ContentType.TWITCH

    # Check podcast platforms
    for pattern in PODCAST_PATTERNS:
        if re.search(pattern, url_lower):
            return ContentType.PODCAST

    # Check forum patterns
    for pattern in FORUM_PATTERNS:
        if re.search(pattern, url_lower):
            return ContentType.FORUM

    # Check if it's just a domain (full site)
    parsed = urlparse(url)
    if not parsed.path or parsed.path == '/':
        return ContentType.SITE

    # Default: assume it's an article
    return ContentType.ARTICLE


def detect_youtube_type(url: str) -> Literal["video", "playlist", "channel"]:
    """Detect the type of YouTube content."""
    url_lower = url.lower()

    # Check for playlist (both /playlist? and ?list= query param)
    if 'playlist' in url_lower or 'list=' in url_lower:
        return "playlist"
    elif any(p in url_lower for p in ['/@', '/channel/', '/c/', '/user/']):
        return "channel"
    else:
        return "video"


def detect_facebook_type(url: str) -> Literal["video", "page", "reel"]:
    """Detect the type of Facebook content."""
    url_lower = url.lower()

    # Single video
    if 'fb.watch/' in url_lower or 'video.php' in url_lower:
        return "video"
    # Reel
    elif '/reel/' in url_lower:
        return "reel"
    # Page videos tab (e.g., /PageName/videos/)
    elif '/videos' in url_lower:
        return "page"
    # /watch/ can be single video or page
    elif '/watch/' in url_lower:
        return "video"
    else:
        return "video"


def detect_twitch_type(url: str) -> Literal["vod", "clip", "channel"]:
    """Detect the type of Twitch content."""
    url_lower = url.lower()

    # Single VOD
    if '/videos/' in url_lower or '/video/' in url_lower:
        return "vod"
    # Clips
    elif '/clip/' in url_lower or 'clips.twitch.tv/' in url_lower or '/clips' in url_lower:
        return "clip"
    # Channel page (list VODs)
    else:
        return "channel"


def detect_podcast_type(url: str) -> Literal["rss", "platform", "webpage"]:
    """Detect the type of podcast source."""
    url_lower = url.lower()

    # RSS feed indicators
    if any(p in url_lower for p in ['.xml', '/feed', '/rss', 'feed.', 'rss.']):
        return "rss"

    # Known podcast platforms
    platforms = ['spotify.com', 'apple.com', 'anchor.fm', 'soundcloud.com']
    if any(p in url_lower for p in platforms):
        return "platform"

    # Default: it's a webpage with audio files
    return "webpage"


def detect_forum_platform(url: str) -> Literal["reddit", "discourse", "phpbb", "vbulletin", "generic"]:
    """Detect the forum platform."""
    url_lower = url.lower()

    if 'reddit.com' in url_lower:
        return "reddit"
    elif 'discourse' in url_lower or re.search(r'/t/[^/]+/\d+', url_lower):
        return "discourse"
    elif 'viewtopic.php' in url_lower:
        return "phpbb"
    elif 'showthread.php' in url_lower:
        return "vbulletin"
    else:
        return "generic"


def get_source_name_from_url(url: str, content_type: ContentType) -> str:
    """Extract a reasonable source name from the URL."""
    parsed = urlparse(url)

    if content_type == ContentType.YOUTUBE:
        # Try to extract channel/playlist name from URL
        match = re.search(r'/@([^/?]+)', url)
        if match:
            return match.group(1)
        # For videos, just use youtube
        return "youtube"

    elif content_type == ContentType.FACEBOOK:
        # Try to extract page name from URL
        # Pattern: facebook.com/PageName/videos
        match = re.search(r'facebook\.com/([^/]+)/videos', url)
        if match and match.group(1) not in ['watch', 'reel']:
            return f"facebook-{match.group(1)}"
        # fb.watch links
        if 'fb.watch' in url:
            return "facebook"
        return "facebook"

    elif content_type == ContentType.TWITCH:
        # Try to extract channel name from URL
        # Pattern: twitch.tv/channelname or twitch.tv/channelname/videos
        match = re.search(r'twitch\.tv/([^/]+)', url)
        if match and match.group(1) not in ['videos', 'directory', 'clips']:
            return f"twitch-{match.group(1)}"
        return "twitch"

    elif content_type == ContentType.PODCAST:
        # Use domain for podcasts
        return parsed.netloc.replace('www.', '').replace('.com', '')

    elif content_type == ContentType.FORUM:
        if 'reddit.com' in url:
            # Extract subreddit and thread indicator
            match = re.search(r'/r/([^/]+)', url)
            if match:
                return f"reddit-{match.group(1)}"
        return parsed.netloc.replace('www.', '')

    else:
        # Use domain name
        return parsed.netloc.replace('www.', '').replace('.com', '').replace('.', '-')
