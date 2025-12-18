#!/usr/bin/env python3
"""
Test single post recovery to validate approach before bulk processing
"""

import requests
import json
import time
from bs4 import BeautifulSoup

# Test the vShield post (first critical post)
POST_SLUG = "how-to-install-vshield-5-1-manager-app-and-endpoint-2"
ORIGINAL_URL = f"http://everythingshouldbevirtual.com/{POST_SLUG}"

WAYBACK_API = "https://archive.org/wayback/available"

def test_wayback_query():
    """Test Wayback Machine query"""
    print(f"Testing Wayback query for: {ORIGINAL_URL}")

    params = {
        'url': ORIGINAL_URL,
        'timestamp': '20140101'
    }

    response = requests.get(WAYBACK_API, params=params, timeout=30)
    response.raise_for_status()
    data = response.json()

    print(f"\nResponse: {json.dumps(data, indent=2)}")

    if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
        snapshot = data['archived_snapshots']['closest']
        if snapshot.get('available'):
            archive_url = snapshot['url']
            print(f"\n✓ Archive found: {archive_url}")
            return archive_url

    print("\n✗ No archive found")
    return None

def test_fetch_archive(archive_url):
    """Test fetching archived page"""
    print(f"\nFetching archived page...")
    time.sleep(2)  # Rate limiting

    response = requests.get(archive_url, timeout=60)
    response.raise_for_status()

    html = response.text
    print(f"✓ Fetched {len(html)} bytes of HTML")
    return html

def test_extract_images(html):
    """Test image extraction"""
    print(f"\nExtracting images from HTML...")

    soup = BeautifulSoup(html, 'html.parser')

    base64_count = 0
    url_count = 0
    external_count = 0

    for img in soup.find_all('img'):
        src = img.get('src', '')

        if src.startswith('data:image'):
            base64_count += 1
            print(f"  Base64 image: {src[:80]}...")
        elif 'wp-content/uploads' in src:
            url_count += 1
            print(f"  WP image: {src}")
        elif src.startswith('http') and 'everythingshouldbevirtual.com' not in src:
            external_count += 1
            print(f"  External: {src}")

    print(f"\nImage summary:")
    print(f"  Base64 images: {base64_count}")
    print(f"  WP content images: {url_count}")
    print(f"  External images: {external_count}")
    print(f"  Total recoverable: {base64_count + url_count}")

    return base64_count + url_count

if __name__ == "__main__":
    try:
        print("="*60)
        print("Testing Wayback Machine Recovery Approach")
        print("="*60)

        # Step 1: Query availability
        archive_url = test_wayback_query()
        if not archive_url:
            print("\n✗ Test failed: No archive available")
            exit(1)

        # Step 2: Fetch archive
        html = test_fetch_archive(archive_url)

        # Step 3: Extract images
        image_count = test_extract_images(html)

        print("\n" + "="*60)
        if image_count > 0:
            print(f"✓ Test successful: Found {image_count} recoverable images")
        else:
            print("✗ Test failed: No images found")
        print("="*60)

    except Exception as e:
        print(f"\n✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
