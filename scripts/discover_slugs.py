#!/usr/bin/env python3
"""
Discover actual WordPress slugs from Wayback Machine

Since Jekyll filenames may not match original WordPress slugs,
this script attempts to find the actual archived URLs by trying
common variations.
"""

import requests
import time
from pathlib import Path

WAYBACK_API = "https://archive.org/wayback/available"
POSTS_DIR = Path("/Users/larrysmithjr/Projects/MethodicalCloud/website/everythingshouldbevirtual/_posts")

def generate_slug_variations(filename):
    """Generate possible slug variations from filename"""
    # Remove .md extension and date prefix
    slug = filename.replace('.md', '')
    parts = slug.split('-')

    # Remove date (YYYY-MM-DD)
    if len(parts) >= 4 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        slug_no_date = '-'.join(parts[3:])
    else:
        slug_no_date = slug

    variations = [
        slug_no_date,  # Basic slug
        slug_no_date.rstrip('-2').rstrip('-3'),  # Remove -2, -3 suffix
    ]

    # Try without trailing numbers
    if slug_no_date.endswith(('-2', '-3', '-4')):
        variations.append(slug_no_date[:-2])

    return list(set(variations))  # Remove duplicates

def test_slug(slug, year='2013'):
    """Test if a slug exists in Wayback Machine"""
    url = f"http://everythingshouldbevirtual.com/{slug}"

    # Try multiple timestamps (blog may have been archived later)
    timestamps = ['20130101', '20140101', '20150101']

    try:
        time.sleep(1)  # Rate limiting
        response = requests.get(
            WAYBACK_API,
            params={'url': url, 'timestamp': timestamps[0]},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        if data.get('archived_snapshots', {}).get('closest', {}).get('available'):
            archive_url = data['archived_snapshots']['closest']['url']
            return archive_url

    except Exception as e:
        print(f"  Error testing {slug}: {e}")

    return None

def discover_post_slug(post_file):
    """Discover the actual WordPress slug for a post"""
    filename = post_file.name
    print(f"\nTesting: {filename}")

    # Extract year from filename for better Wayback targeting
    parts = filename.split('-')
    year = parts[0] if parts[0].isdigit() else '2013'

    variations = generate_slug_variations(filename)
    print(f"  Variations: {variations}")

    for slug in variations:
        archive_url = test_slug(slug, year)
        if archive_url:
            print(f"  ✓ Found: {slug}")
            print(f"    Archive: {archive_url}")
            return slug

    print(f"  ✗ Not found in Wayback Machine")
    return None

def main():
    """Discover slugs for all posts that need recovery"""
    critical_posts = [
        "2012/2012-11-15-how-to-install-vshield-5-1-manager-app-and-endpoint-2.md",
        "2012/2012-09-28-cacti-monitoring-for-windows-servers.md",
        "2012/2012-09-06-hp-p4000-vsa-initial-installation-storvirtual-vsa.md",
    ]

    results = {}

    for post_path in critical_posts:
        full_path = POSTS_DIR / post_path
        if full_path.exists():
            slug = discover_post_slug(full_path)
            if slug:
                results[post_path] = slug

    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    for post, slug in results.items():
        print(f"{post}")
        print(f"  → {slug}")

    print(f"\nFound {len(results)}/{len(critical_posts)} posts")

if __name__ == "__main__":
    main()
