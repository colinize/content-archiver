#!/usr/bin/env python3
"""
Scrape Slam Tilt Podcast episodes 1-163 from the website.
These episodes are not in the RSS feed (only last 100 episodes).
"""

import requests
from bs4 import BeautifulSoup
import re
import os
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# Episode URLs from sitemap (episodes 1-163)
EPISODE_URLS = [
    "https://www.slamtiltpodcast.com/2016/07/14/episode-1-hello-world",
    "https://www.slamtiltpodcast.com/2016/07/21/episode-2-sophomore-jinx",
    "https://www.slamtiltpodcast.com/2016/07/25/episode-3-freedom-firewood",
    "https://www.slamtiltpodcast.com/2016/08/04/episode-4-hotdoggin-at-replayfx",
    "https://www.slamtiltpodcast.com/2016/08/11/episode-5-ghosting-in-the-machine",
    "https://www.slamtiltpodcast.com/2016/08/18/episode-6-winging-it-in-buffalo",
    "https://www.slamtiltpodcast.com/2016/08/25/episode-7-at-the-movies",
    "https://www.slamtiltpodcast.com/2016/09/01/episode-8-too-slow-for-quicksilver",
    "https://www.slamtiltpodcast.com/2016/09/08/episode-9-welcome-to-the-real-world",
    "https://www.slamtiltpodcast.com/2016/09/15/episode-10-an-evening-with-tsex",
    "https://www.slamtiltpodcast.com/2016/09/22/episode-11-gettin-floaty-with-it",
    "https://www.slamtiltpodcast.com/2016/09/29/episode-12-apologies-are-in-order",
    "https://www.slamtiltpodcast.com/2016/10/06/episode-13-sweet-georgia-brown",
    "https://www.slamtiltpodcast.com/2016/10/13/episode-14-an-evening-with-scott-c",
    "https://www.slamtiltpodcast.com/2016/10/20/episode-15-pinball-expo-tsex-strikes-back",
    "https://www.slamtiltpodcast.com/2016/10/27/episode-16-back-in-the-groove",
    "https://www.slamtiltpodcast.com/2016/11/03/episode-17-papa-goes-pump-dump",
    "https://www.slamtiltpodcast.com/2016/11/10/episode-18-tournament-hunting-with-big-game",
    "https://www.slamtiltpodcast.com/2016/11/17/episode-19-home-sweet-home",
    "https://www.slamtiltpodcast.com/2016/11/24/episode-20-turkey-biscuits-bucci",
    "https://www.slamtiltpodcast.com/2016/12/01/episode-21-into-the-matrix",
    "https://www.slamtiltpodcast.com/2016/12/08/episode-22-kick-me-in-the-jimmy",
    "https://www.slamtiltpodcast.com/2016/12/15/episode-23-on-the-mend",
    "https://www.slamtiltpodcast.com/2016/12/22/episode-24-an-evening-with-jeff-teolis",
    "https://www.slamtiltpodcast.com/2017/01/05/episode-25-ballin-with-bowden",
    "https://www.slamtiltpodcast.com/2017/01/12/episode-26-brown-lava-lamp",
    "https://www.slamtiltpodcast.com/2017/01/19/episode-27-just-a-quick-one",
    "https://www.slamtiltpodcast.com/2017/01/26/episode-28-upstate-agony",
    "https://www.slamtiltpodcast.com/2017/02/02/episode-29-an-unexpected-sale",
    "https://www.slamtiltpodcast.com/2017/02/09/episode-30-we-love-jackpots",
    "https://www.slamtiltpodcast.com/2017/02/16/episode-31-wack-a-willie",
    "https://www.slamtiltpodcast.com/2017/02/23/episode-32-technical-ecstasy",
    "https://www.slamtiltpodcast.com/2017/03/02/episode-33-blackout",
    "https://www.slamtiltpodcast.com/2017/03/09/episode-34-the-die-has-been-cast",
    "https://www.slamtiltpodcast.com/2017/03/23/episode-35-the-arcadeexpo-post-show-spectacular",
    "https://www.slamtiltpodcast.com/2017/03/30/episode-36-texas-tornado",
    "https://www.slamtiltpodcast.com/2017/04/04/episode-37-super-duper-papa-preview-extravaganza",
    "https://www.slamtiltpodcast.com/2017/04/13/episode-38-josh-hates-twilight-zone",
    "https://www.slamtiltpodcast.com/2017/04/20/episode-39-pinball-princess",
    "https://www.slamtiltpodcast.com/2017/04/27/episode-40-bmx",
    "https://www.slamtiltpodcast.com/2017/05/04/episode-41-nick-loves-aerosmith",
    "https://www.slamtiltpodcast.com/2017/05/11/episode-42-s-t-o-m-p",
    "https://www.slamtiltpodcast.com/2017/05/18/episode-43-pinball-poetry",
    "https://www.slamtiltpodcast.com/2017/05/25/episode-44-fun-part-of-the-segment",
    "https://www.slamtiltpodcast.com/2017/06/01/episode-45-redemption",
    "https://www.slamtiltpodcast.com/2017/06/08/episode-46-bunghole-crane",
    "https://www.slamtiltpodcast.com/2017/06/15/episode-47-trim",
    "https://www.slamtiltpodcast.com/2017/06/22/episode-48-humongous-bolus",
    "https://www.slamtiltpodcast.com/2017/06/29/episode-49-plastic-nuts",
    "https://www.slamtiltpodcast.com/2017/07/06/episode-50-thunder-from-down-under",
    "https://www.slamtiltpodcast.com/2017/07/13/episode-51-alex-jones",
    "https://www.slamtiltpodcast.com/2017/07/20/episode-52-stomping-our-way-to-replayfx",
    "https://www.slamtiltpodcast.com/2017/07/23/episode-53-the-2017-pinburgh-preview-spectacular",
    "https://www.slamtiltpodcast.com/2017/08/03/episode-54-black-sheep-squadron",
    "https://www.slamtiltpodcast.com/2017/08/10/episode-55-its-harrison-ford",
    "https://www.slamtiltpodcast.com/2017/08/17/episode-56-cease-and-desist",
    "https://www.slamtiltpodcast.com/2017/08/24/episode-57-hot-tippin-with-steel-panther",
    "https://www.slamtiltpodcast.com/2017/08/31/episode-58-premature-delivery",
    "https://www.slamtiltpodcast.com/2017/09/07/episode-59-chunderstruck",
    "https://www.slamtiltpodcast.com/2017/09/14/episode-60-the-choice-is-made",
    "https://www.slamtiltpodcast.com/2017/09/21/episode-61-the-silverball-saloon",
    "https://www.slamtiltpodcast.com/2017/09/28/episode-62-raven",
    "https://www.slamtiltpodcast.com/2017/10/05/episode-63-its-more-fun-to-compete",
    "https://www.slamtiltpodcast.com/2017/10/11/episode-64-quit-talking-and-start-chalking",
    "https://www.slamtiltpodcast.com/2017/10/19/episode-65-pirates-take-over",
    "https://www.slamtiltpodcast.com/2017/10/26/episode-66-no-one-likes-viper",
    "https://www.slamtiltpodcast.com/2017/11/02/episode-67-everyone-likes-dialed-in",
    "https://www.slamtiltpodcast.com/2017/11/09/episode-68-working-for-the-weekend",
    "https://www.slamtiltpodcast.com/2017/11/16/episode-69-never-beef",
    "https://www.slamtiltpodcast.com/2017/11/23/episode-70-blue-swede",
    "https://www.slamtiltpodcast.com/2017/11/30/episode-71-hiatus",
    "https://www.slamtiltpodcast.com/2018/01/04/episode-72-phoenix",
    "https://www.slamtiltpodcast.com/2018/01/11/episode-73-italians-do-it-better",
    "https://www.slamtiltpodcast.com/2018/01/18/episode-74-pick-barb-wire",
    "https://www.slamtiltpodcast.com/2018/01/25/episode-75-more-choice-easily",
    "https://www.slamtiltpodcast.com/2018/02/01/episode-76-s-t-o-m-p-west",
    "https://www.slamtiltpodcast.com/2018/02/08/episode-77-darth-balls",
    "https://www.slamtiltpodcast.com/2018/02/15/episode-78-ripping-off-is-the-new-gold-standard",
    "https://www.slamtiltpodcast.com/2018/02/22/episode-80-out-of-order",
    "https://www.slamtiltpodcast.com/2018/03/01/episode-79-we-enter-the-matrix",
    "https://www.slamtiltpodcast.com/2018/03/08/episode-81-keith-or-steve",
    "https://www.slamtiltpodcast.com/2018/03/15/episode-82-hold-up-your-weight",
    "https://www.slamtiltpodcast.com/2018/03/22/episode-83-straw-hat",
    "https://www.slamtiltpodcast.com/2018/03/29/episode-84-23-10",
    "https://www.slamtiltpodcast.com/2018/04/05/episode-85-the-game",
    "https://www.slamtiltpodcast.com/2018/04/13/episode-86-new-england-north",
    "https://www.slamtiltpodcast.com/2018/04/18/episode-87-spectrum-sucks",
    "https://www.slamtiltpodcast.com/2018/04/26/episode-88-cluster-vuk-the-guests-take-over",
    "https://www.slamtiltpodcast.com/2018/05/02/episode-89-someday-out-there",
    "https://www.slamtiltpodcast.com/2018/05/09/episode-90-up-with-the-horns",
    "https://www.slamtiltpodcast.com/2018/05/16/episode-91-dynamic-duo",
    "https://www.slamtiltpodcast.com/2018/05/23/episode-92-night-at-the-museum",
    "https://www.slamtiltpodcast.com/2018/05/30/episode-93-hexfield-viewscreen",
    "https://www.slamtiltpodcast.com/2018/06/07/episode-94-day-of-reckoning",
    "https://www.slamtiltpodcast.com/2018/06/13/episode-95-use-your-back-not-your-brain",
    "https://www.slamtiltpodcast.com/2018/06/20/episode-96-super-skill-shot",
    "https://www.slamtiltpodcast.com/2018/06/27/episode-97-motel-6-prison",
    "https://www.slamtiltpodcast.com/2018/07/03/episode-98-congrats-to-ssb",
    "https://www.slamtiltpodcast.com/2018/07/12/episode-99-outlash",
    "https://www.slamtiltpodcast.com/2018/07/18/episode-100-lyman-laments",
    "https://www.slamtiltpodcast.com/2018/08/01/episode-101-the-good-the-bad-and-the-ugly",
    "https://www.slamtiltpodcast.com/2018/08/09/episode-102-fireball-shot",
    "https://www.slamtiltpodcast.com/2018/08/16/episode-103-another-quick-one",
    "https://www.slamtiltpodcast.com/2018/08/22/episode-104-on-the-road-with-elo",
    "https://www.slamtiltpodcast.com/2018/08/30/episode-105-triple-jackpot-seven",
    "https://www.slamtiltpodcast.com/2018/09/06/episode-106-so-stupid-its-good",
    "https://www.slamtiltpodcast.com/2018/09/12/episode-107-tiger-rag",
    "https://www.slamtiltpodcast.com/2018/09/20/episode-108-zero-insertion-force",
    "https://www.slamtiltpodcast.com/2018/09/27/episode-109-carbon-paper-in-a-xerox-machine",
    "https://www.slamtiltpodcast.com/2018/10/03/episode-110-goobe-gone",
    "https://www.slamtiltpodcast.com/2018/10/10/episode-111-center-post",
    "https://www.slamtiltpodcast.com/2018/10/17/episode-112-almost-live",
    "https://www.slamtiltpodcast.com/2018/10/24/episode-113-ron-loves-star-wars",
    "https://www.slamtiltpodcast.com/2018/10/30/episode-114-a-banner-day",
    "https://www.slamtiltpodcast.com/2018/11/06/episode-115-waitlist-jackpot",
    "https://www.slamtiltpodcast.com/2018/11/13/episode-116-freezing-in-florida",
    "https://www.slamtiltpodcast.com/2018/11/20/episode-117-the-final-countdown",
    "https://www.slamtiltpodcast.com/2018/11/27/episode-118-underworld",
    "https://www.slamtiltpodcast.com/2018/12/04/episode-119-viper-bite",
    "https://www.slamtiltpodcast.com/2018/12/12/episode-120-socket-to-me",
    "https://www.slamtiltpodcast.com/2018/12/20/episode-121-ashleys-alley",
    "https://www.slamtiltpodcast.com/2018/12/26/episode-122-baseball-bat-to-a-boxing-match",
    "https://www.slamtiltpodcast.com/2019/01/03/episode-123-clustervuk-2-the-quickening",
    "https://www.slamtiltpodcast.com/2019/02/26/episode-124-back-in-the-saddle",
    "https://www.slamtiltpodcast.com/2019/03/13/episode-125-romper-room",
    "https://www.slamtiltpodcast.com/2019/04/03/episode-126-timballs-of-rage",
    "https://www.slamtiltpodcast.com/2019/04/24/episode-127-a-few-hours-in-chicago",
    "https://www.slamtiltpodcast.com/2019/05/08/episode-128-agri-plexing-in-allentown",
    "https://www.slamtiltpodcast.com/2019/05/25/episode-129-chicken-curry",
    "https://www.slamtiltpodcast.com/2019/06/22/episode-130-space-invader",
    "https://www.slamtiltpodcast.com/2019/07/25/episode-131-missing-tickets",
    "https://www.slamtiltpodcast.com/2019/07/30/episode-132-almost-live-2",
    "https://www.slamtiltpodcast.com/2019/08/18/episode-133-slam-tilt-sells-out",
    "https://www.slamtiltpodcast.com/2019/09/12/episode-134-jurassic-deathballs",
    "https://www.slamtiltpodcast.com/2019/10/02/episode-135-hooray-for-hoops",
    "https://www.slamtiltpodcast.com/2019/10/26/episode-136-wreck-havoc",
    "https://www.slamtiltpodcast.com/2019/11/28/episode-137-rooting-atomic-zombies",
    "https://www.slamtiltpodcast.com/2019/12/23/episode-138-ball-lock-in-the-backbox",
    "https://www.slamtiltpodcast.com/2020/01/22/episode-139-still-here",
    "https://www.slamtiltpodcast.com/2020/02/11/episode-140-low-class",
    "https://www.slamtiltpodcast.com/2020/02/26/episode-141-4-for-4",
    "https://www.slamtiltpodcast.com/2020/03/24/episode-142-quarantine",
    "https://www.slamtiltpodcast.com/2020/04/08/episode-143-daniel-wants-stars",
    "https://www.slamtiltpodcast.com/2020/04/23/episode-144-protect-yourself",
    "https://www.slamtiltpodcast.com/2020/05/13/episode-145-sling-power",
    "https://www.slamtiltpodcast.com/2020/06/01/episode-146-for-senior",
    "https://www.slamtiltpodcast.com/2020/06/23/episode-147-k-turn",
    "https://www.slamtiltpodcast.com/2020/07/09/episode-148-lets-get-stupid-again",
    "https://www.slamtiltpodcast.com/2020/08/05/episode-149-slow-time",
    "https://www.slamtiltpodcast.com/2020/08/25/episode-149-5-farewell-to-the-silverball-saloon",
    "https://www.slamtiltpodcast.com/2020/09/09/episode-150-happy-fathers-day",
    "https://www.slamtiltpodcast.com/2020/09/25/episode-151-hangin-in-the-pinbar",
    "https://www.slamtiltpodcast.com/2020/10/14/episode-152-appetite-for-influencers",
    "https://www.slamtiltpodcast.com/2020/10/28/episode-153-clustervuk-3-season-of-the-witch",
    "https://www.slamtiltpodcast.com/2020/11/17/episode-154-soren-strikes-back",
    "https://www.slamtiltpodcast.com/2020/11/28/episode-155-missing-medallions",
    "https://www.slamtiltpodcast.com/2020/12/12/episode-156-sinatra-chicken",
    "https://www.slamtiltpodcast.com/2020/12/19/episode-157-celebratory-gunfire",
    "https://www.slamtiltpodcast.com/2021/01/12/episode-158-good-times-bad-times",
    "https://www.slamtiltpodcast.com/2021/01/27/episode-159-raiding-bits",
    "https://www.slamtiltpodcast.com/2021/02/09/episode-160-a-glutton-of-problems",
    "https://www.slamtiltpodcast.com/2021/02/24/episode-161-bringin-it-from-the-top-rope",
    "https://www.slamtiltpodcast.com/2021/03/09/episode-162-herd-mentality",
    "https://www.slamtiltpodcast.com/2021/04/03/episode-163-pintastic-quickie",
]

OUTPUT_DIR = Path.home() / "projects" / "content-archiver" / "podcasts" / "The_Slam_Tilt_Podcast"

def extract_mp3_url(page_url):
    """Extract MP3 URL from episode page."""
    try:
        response = requests.get(page_url, timeout=30)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')

        # Look for blubrry media link
        for link in soup.find_all('a', href=True):
            href = link['href']
            if 'blubrry.com' in href and '.mp3' in href:
                return href

        # Also check audio source tags
        for audio in soup.find_all('audio'):
            src = audio.get('src', '')
            if '.mp3' in src:
                return src
            for source in audio.find_all('source'):
                src = source.get('src', '')
                if '.mp3' in src:
                    return src

        return None
    except Exception as e:
        print(f"  Error fetching {page_url}: {e}")
        return None

def download_mp3(mp3_url, episode_num, title):
    """Download MP3 file."""
    try:
        # Create filename from episode number and title
        safe_title = re.sub(r'[^\w\s-]', '', title).strip()
        safe_title = re.sub(r'[-\s]+', '_', safe_title)
        filename = f"SlamTiltPodcast_{safe_title}.mp3"
        filepath = OUTPUT_DIR / filename

        if filepath.exists():
            print(f"  [SKIP] Already exists: {filename}")
            return True, "skipped"

        response = requests.get(mp3_url, stream=True, timeout=120)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        with open(filepath, 'wb') as f:
            downloaded = 0
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)

        size_mb = os.path.getsize(filepath) / (1024 * 1024)
        print(f"  [OK] Downloaded: {filename} ({size_mb:.1f}MB)")
        return True, "downloaded"
    except Exception as e:
        print(f"  [FAIL] Download error: {e}")
        return False, "failed"

def extract_episode_info(url):
    """Extract episode number and title from URL."""
    # URL format: .../episode-123-title-here
    match = re.search(r'/episode-(\d+(?:-\d+)?)-(.+?)/?$', url)
    if match:
        ep_num = match.group(1)
        title = match.group(2).replace('-', ' ').title()
        return ep_num, f"Episode {ep_num} - {title}"
    return "unknown", "Unknown Episode"

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Slam Tilt Podcast Scraper")
    print(f"=" * 50)
    print(f"Episodes to fetch: {len(EPISODE_URLS)}")
    print(f"Output directory: {OUTPUT_DIR}")
    print()

    results = {"downloaded": 0, "skipped": 0, "failed": 0}

    for i, url in enumerate(EPISODE_URLS, 1):
        ep_num, title = extract_episode_info(url)
        print(f"[{i}/{len(EPISODE_URLS)}] {title}")

        mp3_url = extract_mp3_url(url)
        if not mp3_url:
            print(f"  [FAIL] Could not find MP3 URL")
            results["failed"] += 1
            continue

        success, status = download_mp3(mp3_url, ep_num, title)
        results[status] += 1

        # Small delay to be polite
        time.sleep(0.5)

    print()
    print(f"=" * 50)
    print(f"Complete!")
    print(f"  Downloaded: {results['downloaded']}")
    print(f"  Skipped: {results['skipped']}")
    print(f"  Failed: {results['failed']}")

if __name__ == "__main__":
    main()
