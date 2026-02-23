"""Fix Knapp Arcade publish dates for posts migrated on Aug 19-20, 2021.

These posts got stamped with the CMS migration date instead of their real
publish date. Most have (Month Year) or (Mon Year) in their title, which
we parse and use as the corrected date (defaulting to the 1st of the month).

Updates _all_posts.json in-place and adds publish_date to markdown frontmatter.
"""

import json
import re
import os
from datetime import datetime

KNAPP_DIR = "/Users/calsheimer/projects/content-archiver/articles/knapparcade.org"
JSON_PATH = os.path.join(KNAPP_DIR, "_all_posts.json")

MONTH_MAP = {
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}

# Match (Month Year) or (Mon Year) at end of title or within parens
MONTH_YEAR_RE = re.compile(
    r"\((?:.*?)("
    + "|".join(MONTH_MAP.keys())
    + r")\s+(20\d{2})\)",
    re.IGNORECASE,
)

MIGRATION_DATES = {"2021-08-19", "2021-08-20"}


def extract_date_from_title(title: str) -> str | None:
    """Try to extract a real date from the title. Returns ISO date string or None."""
    match = MONTH_YEAR_RE.search(title)
    if match:
        month_str = match.group(1).lower()
        year = int(match.group(2))
        month = MONTH_MAP[month_str]
        return f"{year}-{month:02d}-01T12:00:00.000"
    return None


def main():
    with open(JSON_PATH) as f:
        posts = json.load(f)

    migration_posts = [
        p for p in posts if p["publish_date"][:10] in MIGRATION_DATES
    ]
    print(f"Total posts: {len(posts)}")
    print(f"Posts with migration date (Aug 19-20, 2021): {len(migration_posts)}")

    fixed = 0
    unfixed = []

    for post in migration_posts:
        new_date = extract_date_from_title(post["title"])
        if new_date:
            old = post["publish_date"]
            post["publish_date"] = new_date
            post["published_at"] = new_date
            print(f"  FIXED: {old[:10]} -> {new_date[:10]}  {post['title'][:70]}")
            fixed += 1
        else:
            unfixed.append(post)

    print(f"\nFixed: {fixed}")
    print(f"Unfixable (no date in title): {len(unfixed)}")
    for p in unfixed:
        print(f"  SKIPPED: {p['title']}")

    # Write updated JSON
    with open(JSON_PATH, "w") as f:
        json.dump(posts, f, indent=2)
    print(f"\nUpdated {JSON_PATH}")

    # Update markdown files with publish_date in frontmatter
    md_updated = 0
    for post in posts:
        # Find matching markdown file by slug
        slug = post.get("slug", "")
        # Markdown filenames use title, not slug - search by ID in content
        md_files = [
            f
            for f in os.listdir(KNAPP_DIR)
            if f.endswith(".md") and f != "_index.json"
        ]

        for md_file in md_files:
            md_path = os.path.join(KNAPP_DIR, md_file)
            with open(md_path, "r") as f:
                content = f.read()

            # Match by ID line in the markdown
            if f"**ID:** {post['id']}\n" not in content:
                continue

            # Check if publish_date already present
            if "**Publish Date:**" in content:
                break

            # Add publish_date after the ID line
            date_str = post["publish_date"][:10]
            content = content.replace(
                f"**ID:** {post['id']}\n",
                f"**ID:** {post['id']}\n**Publish Date:** {date_str}\n",
            )

            with open(md_path, "w") as f:
                f.write(content)
            md_updated += 1
            break

    print(f"Updated {md_updated} markdown files with publish_date frontmatter")


if __name__ == "__main__":
    main()
