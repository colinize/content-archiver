#!/usr/bin/env python3
"""
Scraper for The Pinball Podcast episodes from thepinballpodcast.com

The RSS feed only contains recent episodes. This script scrapes the website
to download all episodes that weren't captured by the RSS feed.
"""

import os
import re
import requests
from bs4 import BeautifulSoup
from pathlib import Path
import time
from urllib.parse import urlparse, unquote

# Episodes already downloaded from RSS (135-141, 218-220)
ALREADY_DOWNLOADED = {135, 136, 137, 138, 139, 140, 141, 218, 219, 220}

# Episode URLs scraped from the website sitemap
# Format: (episode_number_or_id, url)
EPISODE_URLS = [
    ("001", "https://thepinballpodcast.com/the-pinball-podcast-episode-1"),
    ("002", "https://thepinballpodcast.com/the-pinball-podcast-episode-2"),
    ("003", "https://thepinballpodcast.com/the-pinball-podcast-episode-3"),
    ("004", "https://thepinballpodcast.com/the-pinball-podcast-episode-4"),
    ("005", "https://thepinballpodcast.com/the-pinball-podcast-episode-5-thanks-steve"),
    ("006", "https://thepinballpodcast.com/the-pinball-podcast-episode-6"),
    ("007", "https://thepinballpodcast.com/the-pinball-podcast-episode-7-we-didnt-stamp-our-logo-on-it"),
    ("008", "https://thepinballpodcast.com/the-pinball-podcast-episode-8-white-men-cant-flip"),
    ("009", "https://thepinballpodcast.com/the-pinball-podcast-episode-9-the-poop-bumper"),
    ("010", "https://thepinballpodcast.com/the-pinball-podcast-episode-10-trolling-the-greats"),
    ("011", "https://thepinballpodcast.com/the-pinball-podcast-episode-11-the-one-that-should-have-got-away"),
    ("012", "https://thepinballpodcast.com/the-pinball-podcast-episode-12-there-are-some-jerks-out-there-that-dont-play-pinball"),
    ("013", "https://thepinballpodcast.com/the-pinball-podcast-episode-13-1-year-or-exceptional-mediocrity"),
    ("014", "https://thepinballpodcast.com/the-pinball-podcast-episode-14-thankful-for-stuff-and-things"),
    ("015", "https://thepinballpodcast.com/the-pinball-podcast-episode-15"),
    ("016", "https://thepinballpodcast.com/the-pinball-podcast-episode-16-the-one-where-we-dont-mention-maverick"),
    ("017", "https://thepinballpodcast.com/episode-17-white-spiders-or-gtfo"),
    ("018", "https://thepinballpodcast.com/the-pinball-podcast-episode-18-an-end-to-the-madness"),
    ("019", "https://thepinballpodcast.com/the-pinball-podcast-episode-19-taking-it-up-or-down-to-a-new-level"),
    ("020", "https://thepinballpodcast.com/episode-20-fs-rare-maverick"),
    ("021", "https://thepinballpodcast.com/the-pinball-podcast-episode-21-passion-for-premier-pinball"),
    ("022", "https://thepinballpodcast.com/the-pinball-podcast-episode-22-pinsider-i-hardly-knew-er"),
    ("022b", "https://thepinballpodcast.com/episode-22-comic-location-location-location"),
    ("023", "https://thepinballpodcast.com/the-pinball-podcast-episode-23-three-times-the-awkward-silence"),
    ("024", "https://thepinballpodcast.com/the-pinball-podcast-episode-24-madness"),
    ("025", "https://thepinballpodcast.com/the-pinball-podcast-episode-25-limited-production-value"),
    ("026", "https://thepinballpodcast.com/the-pinball-podcast-episode-26-deck-the-balls"),
    ("027", "https://thepinballpodcast.com/the-pinball-podcast-episode-27-looking-for-maverick-in-alderaan-places"),
    ("028", "https://thepinballpodcast.com/the-pinball-podcast-episode-28-totan-les-and-more"),
    ("029", "https://thepinballpodcast.com/episode-29-technically-problematic-somewhere-between-february-frenzy-and-april-absurdity"),
    ("030", "https://thepinballpodcast.com/the-pinball-podcast-episode-30-a-little-dirty-thirty"),
    ("030b", "https://thepinballpodcast.com/the-pinball-podcast-live-from-the-rocky-mountain-pinball-showdown"),
    ("031", "https://thepinballpodcast.com/the-pinball-podcast-episode-31-saint-python"),
    ("032", "https://thepinballpodcast.com/the-pinball-podcast-episode-32-see-we-dont-ignore-ems"),
    ("033", "https://thepinballpodcast.com/the-pinball-podcast-episode-33"),
    ("034", "https://thepinballpodcast.com/the-pinball-podcast-episode-34-fooooooooour"),
    ("035", "https://thepinballpodcast.com/the-pinball-podcast-episode-35-bee-sicks"),
    ("036", "https://thepinballpodcast.com/the-pinball-podcast-episode-36-p-i-n-b-a-l-l-man-vs-shaolin"),
    ("037", "https://thepinballpodcast.com/the-pinball-podcast-episode-37-in-a-row"),
    ("038", "https://thepinballpodcast.com/episode-38-mavericks-dont-play-by-the-rules"),
    ("039", "https://thepinballpodcast.com/episode-39-ninety-minutes-without-talking-about-destiny"),
    ("040", "https://thepinballpodcast.com/episode-40-thunderbats-on-broadway"),
    ("041", "https://thepinballpodcast.com/episode-41-sitting-on-the-sidelines"),
    ("042", "https://thepinballpodcast.com/episode-42-we-didnt-talk-about-bayonetta-2-for-two-hours-happy"),
    ("043", "https://thepinballpodcast.com/episode-43-cheap-tackle-boxes-and-numerous-rags"),
    ("044", "https://thepinballpodcast.com/episode-44-rollers-of-the-roundtable"),
    ("045", "https://thepinballpodcast.com/episode-45-a-whimsical-waste-of-time"),
    ("046", "https://thepinballpodcast.com/episode-46-who-cooks-for-you"),
    ("047", "https://thepinballpodcast.com/episode-47-lights-cena-claytor"),
    ("047b", "https://thepinballpodcast.com/episode-47b-wrestlemania-interview-with-tommy-skinner"),
    ("048", "https://thepinballpodcast.com/episode-48-denver-the-greatest-snow-on-earth"),
    ("049", "https://thepinballpodcast.com/episode-49-sfw-jodie-foster-pinball-discussions"),
    ("050", "https://thepinballpodcast.com/episode-50-between-two-sterns"),
    ("050b", "https://thepinballpodcast.com/the-pinball-podcast-episode-50b-interview-with-barry-oursler"),
    ("051", "https://thepinballpodcast.com/episode-51-real-detroit-futbol"),
    ("052", "https://thepinballpodcast.com/episode-52-find-em-flip-em-and-flee"),
    ("053", "https://thepinballpodcast.com/episode-53-now-100-yawn-free"),
    ("054", "https://thepinballpodcast.com/episode-54-pinweenballwhirlweenween-on-mespirit-of-54"),
    ("055", "https://thepinballpodcast.com/episode-55-the-pinball-podcast-with-tron-and-jeff"),
    ("056", "https://thepinballpodcast.com/episode-56-ding-dongle-the-wizard-is-dead"),
    ("057", "https://thepinballpodcast.com/episode-57-fancy-flexxin"),
    ("058", "https://thepinballpodcast.com/episode-58-live-from-the-rocky-mountain-pinball-showdown-2015"),
    ("059", "https://thepinballpodcast.com/episode-59-southern-fried-monopolee-pinball-showdown"),
    ("060", "https://thepinballpodcast.com/episode-60-virtually-prototypical"),
    ("061", "https://thepinballpodcast.com/episode-61-demoliscious-mold"),
    ("062", "https://thepinballpodcast.com/episode-62-straight-outta-capcom"),
    ("063", "https://thepinballpodcast.com/episode-63-em-barrassed-by-nick-baldridge"),
    ("064", "https://thepinballpodcast.com/episode-64-niftysaurus-isnt-chronologically-accurate"),
    ("065", "https://thepinballpodcast.com/episode-65-slice-soda-and-kick-butt-stuff"),
    ("066", "https://thepinballpodcast.com/episode-66-zen-and-the-art-of-pinball-maintenance"),
    ("067", "https://thepinballpodcast.com/episode-67-a-more-boringless-funny-statler-and-waldorf"),
    ("068", "https://thepinballpodcast.com/episode-68-our-final-episode-pre-fallout-4"),
    ("069", "https://thepinballpodcast.com/episode-69-you-missed-the-post-show-shakira-fan-chat"),
    ("070", "https://thepinballpodcast.com/episode-70-slaves-to-pinball"),
    ("070b", "https://thepinballpodcast.com/episode-70b-rob-zombies-spookshow-international"),
    ("071", "https://thepinballpodcast.com/episode-71-keeping-up-with-the-cardassians"),
    ("071b", "https://thepinballpodcast.com/episode-71b-bonesaw-is-ready-vault-edition-discussion"),
    ("072", "https://thepinballpodcast.com/episode-72-swinging-with-clay-tor"),
    ("073", "https://thepinballpodcast.com/episode-73-dont-buy-pins-down-under"),
    ("074", "https://thepinballpodcast.com/episode-74-predictions-papas-wasatch-zenkus"),
    ("075", "https://thepinballpodcast.com/episode-75-jeff-loses-it"),
    ("076", "https://thepinballpodcast.com/episode-76-post-partum-impressions"),
    ("077", "https://thepinballpodcast.com/episode-77-michael-paul-schmidt-was-not-mentioned-on-this-episode"),
    ("078", "https://thepinballpodcast.com/episode-78-no-time-for-love-dr-john"),
    ("079", "https://thepinballpodcast.com/episode-79-the-call-of-cholula"),
    ("080", "https://thepinballpodcast.com/episode-80-medieval-mountin"),
    ("081", "https://thepinballpodcast.com/episode-81-tim-has-better-things-to-do"),
    ("082", "https://thepinballpodcast.com/episode-82-mitchell-even-his-name-says-is-that-a-beer"),
    ("083", "https://thepinballpodcast.com/episode-83-rocky-mountain-pinball-shoutouts-except-lee"),
    ("084", "https://thepinballpodcast.com/episode-84-the-pinball-podcast-with-don-jeff-and-scott"),
    ("085", "https://thepinballpodcast.com/episode-85-the-most-heinous-dmd-hater"),
    ("086", "https://thepinballpodcast.com/episode-86-shortshowforharambe"),
    ("087", "https://thepinballpodcast.com/episode-87-jeff-has-another-epic-meltdown"),
    ("088", "https://thepinballpodcast.com/episode-88-fart-fairy"),
    ("089", "https://thepinballpodcast.com/the-pinball-podcast-episode-89-oh-yeeeeeeeeeeaaaaaahhh-brother"),
    ("090", "https://thepinballpodcast.com/episode-90-lance-armstrongs-favorite-pins"),
    ("091", "https://thepinballpodcast.com/episode-91-aliens-soothsayers-and-more-batman66-complaints"),
    ("091b", "https://thepinballpodcast.com/episode-91-b-stuck-fern"),
    ("092", "https://thepinballpodcast.com/episode-92-we-effed-up-like-a-bunch"),
    ("093", "https://thepinballpodcast.com/episode-93-h-u-o-positive"),
    ("094", "https://thepinballpodcast.com/episode-94-belles-bad-movies"),
    ("095", "https://thepinballpodcast.com/episode-95-good-movies-and-bad-dogs"),
    ("096", "https://thepinballpodcast.com/episode-96-meatier"),
    ("097", "https://thepinballpodcast.com/episode-97-the-ghosts-of-2016-have-come-for-us"),
    ("098", "https://thepinballpodcast.com/episode-98-we-give-transformers-more-lip-service-on-this-episode-than-our-previous-97-episodes-combined"),
    ("099", "https://thepinballpodcast.com/episode-99-meet-punky-willy-his-boy-elroy"),
    ("099b", "https://thepinballpodcast.com/episode-99b-self-absorbed-narcissists"),
    ("100", "https://thepinballpodcast.com/episode-100-live-from-flipperspiel-underground"),
    ("101", "https://thepinballpodcast.com/episode-101-pinball-therapy"),
    ("102", "https://thepinballpodcast.com/1530"),  # Episode 102
    ("103", "https://thepinballpodcast.com/episode-103-pinbutt"),
    ("105", "https://thepinballpodcast.com/episode-105-a-classy-amount-of-nipple"),
    ("106", "https://thepinballpodcast.com/episode-106-its-always-sunny-in-denver"),
    ("107", "https://thepinballpodcast.com/episode-107-kickstart-my-pinball-heart"),
    ("108", "https://thepinballpodcast.com/episode-108-baby-drive-her"),
    ("109", "https://thepinballpodcast.com/episode-109-yay-pinburgh"),
    ("110", "https://thepinballpodcast.com/episode-110-doggone-dog"),
    ("111", "https://thepinballpodcast.com/episode-111-y1d1ae"),
    ("112", "https://thepinballpodcast.com/episode-112-finding-pinballs-bottom"),
    ("113", "https://thepinballpodcast.com/episode-113-get-well-tesla"),
    ("114", "https://thepinballpodcast.com/episode-114-expo-and-other-things"),
    ("115", "https://thepinballpodcast.com/episode-115-you-missed-a-spot"),
    ("116", "https://thepinballpodcast.com/episode-116-bobalee"),
    ("117", "https://thepinballpodcast.com/episode-117-not-dead-yet"),
    ("118", "https://thepinballpodcast.com/episode-118-pinballs-drain-the-the-other-way-in-australia"),
    ("119", "https://thepinballpodcast.com/episode-119-didgeridont-stop"),
    ("120", "https://thepinballpodcast.com/episode-120-lets-chisel-faces-in-mountains"),
    ("121", "https://thepinballpodcast.com/episode-121-from-the-future"),
    ("121b", "https://thepinballpodcast.com/episode-121b-kaite-martin-discusses-w-i-p-t-at-replay-fx"),
    ("122", "https://thepinballpodcast.com/episode-122-mount-plungemore-it-is"),
    ("122b", "https://thepinballpodcast.com/episode-122b-the-mean-queen-pinball-tournament"),
    ("123", "https://thepinballpodcast.com/episode-123-fedex-freight-sucks"),
    ("123b", "https://thepinballpodcast.com/episode-123b-2018-brisbane-masters"),
    ("123c", "https://thepinballpodcast.com/episode-123c-brisbane-masters-2018-recap"),
    ("123d", "https://thepinballpodcast.com/episode-123d-pinburgh-and-continuing-adventures-recap-with-jimmy-nails-and-secret-guest-its-bowen"),
    ("124", "https://thepinballpodcast.com/episode-124-were-back-and-soon-to-be-better-than-before"),
    ("125", "https://thepinballpodcast.com/episode-125-a-discussion-on-plunging-without-innuendo"),
    ("126", "https://thepinballpodcast.com/episode-126-whats-in-your-gameroom"),
    ("127", "https://thepinballpodcast.com/episode-127-poorly-drawn-podcats"),
    ("128", "https://thepinballpodcast.com/episode-128-jessica-set-to-destroy-head2head"),
    ("129", "https://thepinballpodcast.com/episode-129-we-are-idiot"),
    ("130", "https://thepinballpodcast.com/episode-130-always-trending-up"),
    ("131", "https://thepinballpodcast.com/episode-131-no-its-not-pinburgh-yet"),
    ("132", "https://thepinballpodcast.com/episode-132-hey-wha-happened"),
    ("133", "https://thepinballpodcast.com/episode-133-no-we-werent-invited-either"),
    ("134", "https://thepinballpodcast.com/episode-134-mailing-it-win"),
    # Episodes 135-141 and 218-220 already downloaded from RSS
    # Episodes 142-217 appear to be missing from the website sitemap
]

# Additional bonus/special content
BONUS_URLS = [
    ("bonus_holiday", "https://thepinballpodcast.com/this-flippin-x-the-pinball-podcast-bonus-holiday-episode"),
]

OUTPUT_DIR = Path.home() / "projects" / "content-archiver" / "podcasts" / "The_Pinball_Podcast"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
}

def get_mp3_url(page_url):
    """Scrape a page and extract the Blubrry MP3 URL."""
    try:
        response = requests.get(page_url, headers=HEADERS, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Look for Blubrry links
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'blubrry.com' in href and '.mp3' in href:
                return href

        # Also check in audio elements
        for audio in soup.find_all('audio'):
            src = audio.get('src', '')
            if 'blubrry.com' in src:
                return src
            for source in audio.find_all('source'):
                src = source.get('src', '')
                if 'blubrry.com' in src:
                    return src

        return None
    except Exception as e:
        print(f"  [ERROR] Failed to scrape {page_url}: {e}")
        return None

def sanitize_filename(name):
    """Create a safe filename."""
    # Remove or replace problematic characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.replace(' ', '_')
    name = re.sub(r'_+', '_', name)  # Collapse multiple underscores
    return name[:200]  # Limit length

def download_file(url, output_path):
    """Download a file with progress indication."""
    try:
        response = requests.get(url, headers=HEADERS, stream=True, timeout=300)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0

        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)

        size_mb = downloaded / (1024 * 1024)
        return True, size_mb
    except Exception as e:
        return False, str(e)

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Combine all episodes
    all_episodes = EPISODE_URLS + BONUS_URLS

    # Filter out already downloaded episodes
    episodes_to_download = []
    for ep_id, url in all_episodes:
        # Check if it's a number that we already have
        try:
            ep_num = int(ep_id.replace('b', '').replace('c', '').replace('d', ''))
            if ep_num in ALREADY_DOWNLOADED and 'b' not in ep_id and 'c' not in ep_id and 'd' not in ep_id:
                continue
        except ValueError:
            pass
        episodes_to_download.append((ep_id, url))

    print(f"The Pinball Podcast Scraper")
    print(f"=" * 50)
    print(f"Total episodes to download: {len(episodes_to_download)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    downloaded = 0
    skipped = 0
    failed = 0

    for i, (ep_id, page_url) in enumerate(episodes_to_download, 1):
        print(f"[{i}/{len(episodes_to_download)}] Episode {ep_id}")

        # Get the MP3 URL
        mp3_url = get_mp3_url(page_url)
        if not mp3_url:
            print(f"  [SKIP] No MP3 found on page")
            skipped += 1
            continue

        # Create filename
        filename = f"ThePinballPodcast_Episode_{ep_id}.mp3"
        output_path = OUTPUT_DIR / filename

        # Skip if already exists
        if output_path.exists():
            print(f"  [SKIP] Already exists")
            skipped += 1
            continue

        # Download
        success, result = download_file(mp3_url, output_path)
        if success:
            print(f"  [OK] Downloaded: {filename} ({result:.1f}MB)")
            downloaded += 1
        else:
            print(f"  [FAIL] {result}")
            failed += 1

        # Small delay between requests
        time.sleep(0.5)

    print()
    print("=" * 50)
    print("Complete!")
    print(f"  Downloaded: {downloaded}")
    print(f"  Skipped: {skipped}")
    print(f"  Failed: {failed}")

if __name__ == "__main__":
    main()
