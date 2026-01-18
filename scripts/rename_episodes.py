#!/usr/bin/env python3
"""Rename podcast episodes using ID3 metadata or feed data."""
import re
import sys
from pathlib import Path
from datetime import datetime
import feedparser
from mutagen.mp3 import MP3

def sanitize(name: str) -> str:
    """Make filename safe."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    return name[:150]

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('podcasts/Kaneda')
    feed_file = folder / 'feed.xml'

    # Build metadata from feed
    meta = {}
    if feed_file.exists():
        feed = feedparser.parse(str(feed_file))
        for e in feed.entries:
            for enc in getattr(e, 'enclosures', []):
                url = enc.get('href', '')
                m = re.search(r'/(\d{6,})\.mp3', url)
                if m:
                    pub = None
                    if hasattr(e, 'published_parsed') and e.published_parsed:
                        try: pub = datetime(*e.published_parsed[:6])
                        except: pass
                    meta[m.group(1)] = (e.get('title', ''), pub)
                    break
        print(f"Feed metadata: {len(meta)} episodes")

    renamed = skipped = 0
    for mp3 in sorted(folder.glob('*.mp3')):
        m = re.search(r'(\d{6,})', mp3.stem)
        if not m:
            skipped += 1
            continue

        pid = m.group(1)

        # Get title from ID3 or feed
        title = None
        pub_date = None

        try:
            audio = MP3(str(mp3))
            if audio.tags:
                title = str(audio.tags.get('TIT2', ''))
                date_tag = audio.tags.get('TDRC')
                if date_tag:
                    pub_date = str(date_tag)[:10]
        except:
            pass

        # Fallback to feed
        if (not title or title == 'None') and pid in meta:
            title, pub = meta[pid]
            if pub:
                pub_date = pub.strftime('%Y-%m-%d')

        if not title or title == 'None':
            skipped += 1
            continue

        # Build new filename
        safe_title = sanitize(title)
        if pub_date:
            new_name = f"{pub_date}_{safe_title}.mp3"
        else:
            new_name = f"{safe_title}.mp3"

        new_path = mp3.parent / new_name

        if new_path.exists() and new_path != mp3:
            # Add suffix if collision
            new_name = f"{pub_date}_{safe_title}_{pid}.mp3" if pub_date else f"{safe_title}_{pid}.mp3"
            new_path = mp3.parent / new_name

        if new_path != mp3:
            try:
                mp3.rename(new_path)
                renamed += 1
            except Exception as ex:
                print(f"Error renaming {mp3.name}: {ex}")
                skipped += 1
        else:
            skipped += 1

    print(f"Done: {renamed} renamed, {skipped} skipped")

if __name__ == '__main__':
    main()
