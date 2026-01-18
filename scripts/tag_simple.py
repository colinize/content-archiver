#!/usr/bin/env python3
"""Simple ID3 tagger for Patreon podcasts."""
import re
import sys
from pathlib import Path
from datetime import datetime
import feedparser
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2, TALB, TPE1, TDRC, TCON

def main():
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('podcasts/Kaneda')
    feed_file = folder / 'feed.xml'

    if not feed_file.exists():
        print(f"No feed.xml in {folder}")
        return

    # Parse feed
    feed = feedparser.parse(str(feed_file))
    title = feed.feed.get('title', 'Podcast')
    author = feed.feed.get('itunes_author', title)
    print(f"Podcast: {title} ({len(feed.entries)} episodes)")

    # Map Patreon IDs to metadata
    meta = {}
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

    print(f"Mapped: {len(meta)} IDs")

    # Tag files
    tagged = failed = skipped = 0
    for mp3 in sorted(folder.glob('*.mp3')):
        m = re.search(r'(\d{6,})', mp3.stem)
        if not m or m.group(1) not in meta:
            skipped += 1
            continue

        ep_title, pub = meta[m.group(1)]
        try:
            audio = MP3(str(mp3))
            if audio.tags is None:
                audio.add_tags()
            audio.tags.add(TIT2(encoding=3, text=ep_title))
            audio.tags.add(TALB(encoding=3, text=title))
            audio.tags.add(TPE1(encoding=3, text=author))
            audio.tags.add(TCON(encoding=3, text='Podcast'))
            if pub:
                audio.tags.add(TDRC(encoding=3, text=pub.strftime('%Y-%m-%d')))
            audio.save()
            tagged += 1
        except Exception as ex:
            print(f"Error: {mp3.name}: {ex}")
            failed += 1

    print(f"Done: {tagged} tagged, {failed} failed, {skipped} skipped")

if __name__ == '__main__':
    main()
