#!/usr/bin/env python3
"""
Bulk Image Recovery from Wayback Machine for Jekyll Blog Posts

This script systematically recovers missing images from the Internet Archive's
Wayback Machine for multiple Jekyll blog posts. It handles both base64-encoded
inline images and wp-content/uploads URL-based images.

Usage:
    python3 bulk_image_recovery.py [--dry-run] [--priority LEVEL]

Priority Levels:
    critical - Posts with 36+ images (3 posts, 122 images)
    high     - Posts with 13-21 images (3 posts, 48 images)
    moderate - Posts with 3-10 images (4 posts, 24 images)
    low      - Posts with 1-3 images (12 posts, ~25 images)
    all      - Process all posts (default)
"""

import argparse
import base64
import json
import logging
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('image_recovery.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Base paths
BLOG_ROOT = Path("/Users/larrysmithjr/Projects/MethodicalCloud/website/everythingshouldbevirtual")
POSTS_DIR = BLOG_ROOT / "_posts"
ASSETS_DIR = BLOG_ROOT / "assets"

# Wayback Machine API
WAYBACK_API = "https://archive.org/wayback/available"
WAYBACK_CDN = "https://web.archive.org"

# Rate limiting
REQUEST_DELAY = 2.0  # seconds between Wayback requests

# Post definitions with priority levels
POSTS_TO_RECOVER = {
    "critical": [
        {
            "file": "2012/2012-11-15-how-to-install-vshield-5-1-manager-app-and-endpoint-2.md",
            "slug": "how-to-install-vshield-5-1-manager-app-and-endpoint-2",
            "images": 47
        },
        {
            "file": "2012/2012-09-28-cacti-monitoring-for-windows-servers.md",
            "slug": "cacti-monitoring-for-windows-servers",
            "images": 39
        },
        {
            "file": "2012/2012-09-06-hp-p4000-vsa-initial-installation-storvirtual-vsa.md",
            "slug": "hp-p4000-vsa-initial-installation-storvirtual-vsa",
            "images": 36
        },
    ],
    "high": [
        {
            "file": "2012/2012-10-18-vsphere-5-1-autodeploy.md",
            "slug": "vsphere-5-1-autodeploy",
            "images": 21
        },
        {
            "file": "2013/2013-02-01-veeam-backup-and-replication-to-nexenta-nfs.md",
            "slug": "veeam-backup-and-replication-to-nexenta-nfs",
            "images": 14
        },
        {
            "file": "2012/2012-07-21-nexentastoresxi53750glacpvdsnfsiscsi-part-1.md",
            "slug": "nexentastoresxi53750glacpvdsnfsiscsi-part-1",
            "images": 13
        },
    ],
    "moderate": [
        {
            "file": "2012/2012-08-19-setup-storage-cluster-with-sdrs-vsphere5.md",
            "slug": "setup-storage-cluster-with-sdrs-vsphere5",
            "images": 10
        },
        {
            "file": "2012/2012-09-17-upgrade-existing-vds-to-5-1-using-web-ui.md",
            "slug": "upgrade-existing-vds-to-5-1-using-web-ui",
            "images": 6
        },
        {
            "file": "2012/2012-08-11-support-howto-how-to-export-and-import-platespin-migrateprotectforge-database.md",
            "slug": "support-howto-how-to-export-and-import-platespin-migrateprotectforge-database",
            "images": 5
        },
        {
            "file": "2012/2012-11-04-ubuntu-utm-homebrew-network-graphing.md",
            "slug": "ubuntu-utm-homebrew-network-graphing",
            "images": 3
        },
    ],
    "low": [
        {
            "file": "2013/2013-03-04-new-nexenta-server-coming-soon.md",
            "slug": "new-nexenta-server-coming-soon",
            "images": 9  # External Newegg - may not recover
        },
        {
            "file": "2012/2012-08-01-issue-with-sophosastaro-utm-9-and-xbox-live.md",
            "slug": "issue-with-sophosastaro-utm-9-and-xbox-live",
            "images": 3
        },
        {
            "file": "2012/2012-10-19-ubuntu-utm-homebrew.md",
            "slug": "ubuntu-utm-homebrew",
            "images": 3
        },
        {
            "file": "2012/2012-08-08-using-ibm-xiv-and-vsphere5-you-need-to-install-the-vasa-and-management-console-for-vcenter.md",
            "slug": "using-ibm-xiv-and-vsphere5-you-need-to-install-the-vasa-and-management-console-for-vcenter",
            "images": 2
        },
        # Add remaining posts with 1 image each
        {
            "file": "2012/2012-08-21-configure-horizon-data-for-view-composer.md",
            "slug": "configure-horizon-data-for-view-composer",
            "images": 1
        },
        {
            "file": "2012/2012-08-22-install-view-composer.md",
            "slug": "install-view-composer",
            "images": 1
        },
        {
            "file": "2012/2012-09-25-ubuntu-utm-homebrew-monitor-wan-traffic-and-graph-top-talkers.md",
            "slug": "ubuntu-utm-homebrew-monitor-wan-traffic-and-graph-top-talkers",
            "images": 1
        },
        {
            "file": "2012/2012-10-01-using-ubuntu-server-12-04-for-ansible.md",
            "slug": "using-ubuntu-server-12-04-for-ansible",
            "images": 1
        },
        {
            "file": "2012/2012-10-13-migrate-veeam-replica-vmdk-from-one-host-to-another.md",
            "slug": "migrate-veeam-replica-vmdk-from-one-host-to-another",
            "images": 1
        },
        {
            "file": "2013/2013-02-01-install-snmp-on-ubuntu-server.md",
            "slug": "install-snmp-on-ubuntu-server",
            "images": 1
        },
        {
            "file": "2013/2013-02-04-install-hp-lefthand-centralized-management-console.md",
            "slug": "install-hp-lefthand-centralized-management-console",
            "images": 1
        },
        {
            "file": "2013/2013-02-28-installing-oracle-xe-11g-on-ubuntu-server-12-04.md",
            "slug": "installing-oracle-xe-11g-on-ubuntu-server-12-04",
            "images": 1
        },
    ]
}


class ImageRecoveryStats:
    """Track recovery statistics"""

    def __init__(self):
        self.posts_attempted = 0
        self.posts_succeeded = 0
        self.posts_failed = 0
        self.posts_no_archive = 0
        self.images_found = 0
        self.images_downloaded = 0
        self.images_failed = 0
        self.external_images = 0
        self.start_time = datetime.now()
        self.errors: List[str] = []

    def summary(self) -> str:
        """Generate summary report"""
        duration = datetime.now() - self.start_time
        return f"""
===== Image Recovery Summary =====
Duration: {duration}
Posts Attempted: {self.posts_attempted}
Posts Succeeded: {self.posts_succeeded}
Posts Failed: {self.posts_failed}
Posts Not in Archive: {self.posts_no_archive}

Images Found: {self.images_found}
Images Downloaded: {self.images_downloaded}
Images Failed: {self.images_failed}
External Images Skipped: {self.external_images}

Success Rate: {(self.posts_succeeded / max(self.posts_attempted, 1) * 100):.1f}%
Image Recovery Rate: {(self.images_downloaded / max(self.images_found, 1) * 100):.1f}%

Errors:
{chr(10).join(f"  - {e}" for e in self.errors[-10:])}  # Last 10 errors
"""


class WaybackImageRecovery:
    """Main recovery class"""

    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.stats = ImageRecoveryStats()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })

    def query_wayback_availability(self, url: str, timestamp: str = "20130101") -> Optional[str]:
        """Query Wayback Machine for archived version of URL"""
        try:
            params = {
                'url': url,
                'timestamp': timestamp
            }
            response = self.session.get(WAYBACK_API, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if 'archived_snapshots' in data and 'closest' in data['archived_snapshots']:
                snapshot = data['archived_snapshots']['closest']
                if snapshot.get('available'):
                    archive_url = snapshot['url']
                    logger.info(f"Found archive: {archive_url}")
                    return archive_url

            logger.warning(f"No archive found for {url}")
            return None

        except Exception as e:
            logger.error(f"Error querying Wayback API for {url}: {e}")
            self.stats.errors.append(f"Wayback query failed for {url}: {e}")
            return None

    def fetch_archived_page(self, archive_url: str) -> Optional[str]:
        """Fetch HTML content from Wayback Machine"""
        try:
            time.sleep(REQUEST_DELAY)  # Rate limiting
            response = self.session.get(archive_url, timeout=60)
            response.raise_for_status()
            return response.text

        except Exception as e:
            logger.error(f"Error fetching archived page {archive_url}: {e}")
            self.stats.errors.append(f"Page fetch failed for {archive_url}: {e}")
            return None

    def extract_images(self, html: str, post_slug: str) -> List[Dict]:
        """Extract images from archived HTML"""
        soup = BeautifulSoup(html, 'html.parser')
        images = []

        # Find all img tags
        for idx, img in enumerate(soup.find_all('img')):
            image_data = {
                'index': idx,
                'type': None,
                'src': None,
                'data': None,
                'filename': None
            }

            src = img.get('src', '')

            # Check for base64 inline image
            if src.startswith('data:image'):
                match = re.match(r'data:image/(\w+);base64,(.+)', src)
                if match:
                    ext = match.group(1)
                    data = match.group(2)
                    image_data['type'] = 'base64'
                    image_data['data'] = data
                    image_data['filename'] = f"image-{idx:03d}.{ext}"
                    images.append(image_data)
                    logger.debug(f"Found base64 image: {image_data['filename']}")

            # Check for wp-content/uploads URL
            elif 'wp-content/uploads' in src:
                image_data['type'] = 'url'
                image_data['src'] = src
                # Extract filename from URL
                filename = os.path.basename(urlparse(src).path)
                image_data['filename'] = filename
                images.append(image_data)
                logger.debug(f"Found wp-content image: {filename}")

            # Check for external images
            elif src.startswith('http') and 'everythingshouldbevirtual.com' not in src:
                logger.info(f"Skipping external image: {src}")
                self.stats.external_images += 1

        self.stats.images_found += len(images)
        logger.info(f"Extracted {len(images)} images from archived page")
        return images

    def download_image(self, image: Dict, output_dir: Path) -> bool:
        """Download or decode image to output directory"""
        output_path = output_dir / image['filename']

        try:
            if image['type'] == 'base64':
                # Decode base64 data
                img_data = base64.b64decode(image['data'])
                if not self.dry_run:
                    output_path.write_bytes(img_data)
                logger.info(f"Decoded base64 image to {output_path}")
                return True

            elif image['type'] == 'url':
                # Download from URL (may need Wayback prefix)
                url = image['src']
                if not url.startswith('http'):
                    logger.warning(f"Relative URL, cannot download: {url}")
                    return False

                time.sleep(0.5)  # Brief delay for image downloads
                response = self.session.get(url, timeout=30)
                response.raise_for_status()

                if not self.dry_run:
                    output_path.write_bytes(response.content)
                logger.info(f"Downloaded image from {url} to {output_path}")
                return True

            return False

        except Exception as e:
            logger.error(f"Error downloading image {image['filename']}: {e}")
            self.stats.errors.append(f"Image download failed for {image['filename']}: {e}")
            return False

    def update_markdown(self, post_path: Path, images: List[Dict], slug: str) -> bool:
        """Update markdown file with new image paths"""
        try:
            content = post_path.read_text()

            # Read front matter
            parts = content.split('---', 2)
            if len(parts) < 3:
                logger.error(f"Invalid front matter in {post_path}")
                return False

            front_matter = parts[1]
            body = parts[2]

            # Add toc if long post (>1000 words)
            word_count = len(body.split())
            if word_count > 1000 and 'toc:' not in front_matter:
                front_matter = front_matter.rstrip() + "\ntoc: true\ntoc_label: \"Contents\"\n"
                logger.info(f"Added TOC to {post_path.name} ({word_count} words)")

            # Update image references
            # Pattern: ![...](../../assets/filename)
            updated_body = body
            for idx, img in enumerate(images):
                old_filename = img['filename']
                new_path = f"/assets/{slug}/{old_filename}"

                # Try to find and replace the image reference
                # This is a simplified approach - may need refinement
                pattern = rf'!\[([^\]]*)\]\([^)]*{re.escape(old_filename.replace("-", "[-_]?"))}[^)]*\)'

                # Add alt text if missing
                def add_alt(match):
                    alt = match.group(1)
                    if not alt:
                        alt = f"Step {idx + 1}"
                    return f'![{alt}]({new_path})'

                updated_body = re.sub(pattern, add_alt, updated_body)

            # Reconstruct file
            new_content = f"---{front_matter}---{updated_body}"

            if not self.dry_run:
                post_path.write_text(new_content)

            logger.info(f"Updated markdown file: {post_path}")
            return True

        except Exception as e:
            logger.error(f"Error updating markdown {post_path}: {e}")
            self.stats.errors.append(f"Markdown update failed for {post_path}: {e}")
            return False

    def process_post(self, post_info: Dict) -> bool:
        """Process a single post"""
        post_file = post_info['file']
        slug = post_info['slug']
        expected_images = post_info['images']

        logger.info(f"\n{'='*60}")
        logger.info(f"Processing: {post_file}")
        logger.info(f"Expected images: {expected_images}")
        logger.info(f"{'='*60}")

        self.stats.posts_attempted += 1

        # Construct paths
        post_path = POSTS_DIR / post_file
        if not post_path.exists():
            logger.error(f"Post file not found: {post_path}")
            self.stats.posts_failed += 1
            return False

        assets_dir = ASSETS_DIR / slug

        # Create assets directory
        if not self.dry_run:
            assets_dir.mkdir(parents=True, exist_ok=True)

        # Query Wayback Machine
        original_url = f"http://everythingshouldbevirtual.com/{slug}"
        archive_url = self.query_wayback_availability(original_url)

        if not archive_url:
            logger.warning(f"No archive found for {original_url}")
            self.stats.posts_no_archive += 1
            return False

        # Fetch archived page
        html = self.fetch_archived_page(archive_url)
        if not html:
            self.stats.posts_failed += 1
            return False

        # Extract images
        images = self.extract_images(html, slug)
        if not images:
            logger.warning(f"No images found in archive for {slug}")
            self.stats.posts_failed += 1
            return False

        # Download images
        successful_downloads = 0
        for img in images:
            if self.download_image(img, assets_dir):
                successful_downloads += 1
                self.stats.images_downloaded += 1
            else:
                self.stats.images_failed += 1

        logger.info(f"Downloaded {successful_downloads}/{len(images)} images")

        # Update markdown
        if successful_downloads > 0:
            if self.update_markdown(post_path, images, slug):
                self.stats.posts_succeeded += 1
                logger.info(f"✓ Successfully processed {post_file}")
                return True

        self.stats.posts_failed += 1
        return False

    def run(self, priority: str = "all"):
        """Run bulk recovery for specified priority level"""
        logger.info(f"Starting bulk image recovery (priority: {priority})")
        logger.info(f"Dry run: {self.dry_run}")

        # Determine which posts to process
        posts_to_process = []
        if priority == "all":
            for level in ["critical", "high", "moderate", "low"]:
                posts_to_process.extend(POSTS_TO_RECOVER[level])
        elif priority in POSTS_TO_RECOVER:
            posts_to_process = POSTS_TO_RECOVER[priority]
        else:
            logger.error(f"Invalid priority level: {priority}")
            return

        logger.info(f"Processing {len(posts_to_process)} posts")

        # Process each post
        for post in posts_to_process:
            try:
                self.process_post(post)
            except Exception as e:
                logger.error(f"Unexpected error processing {post['file']}: {e}")
                self.stats.errors.append(f"Unexpected error for {post['file']}: {e}")
                self.stats.posts_failed += 1

            # Delay between posts
            time.sleep(REQUEST_DELAY)

        # Print summary
        logger.info(self.stats.summary())

        # Save detailed log
        if not self.dry_run:
            log_file = BLOG_ROOT / "image_recovery_report.json"
            report = {
                'timestamp': datetime.now().isoformat(),
                'priority': priority,
                'stats': {
                    'posts_attempted': self.stats.posts_attempted,
                    'posts_succeeded': self.stats.posts_succeeded,
                    'posts_failed': self.stats.posts_failed,
                    'posts_no_archive': self.stats.posts_no_archive,
                    'images_found': self.stats.images_found,
                    'images_downloaded': self.stats.images_downloaded,
                    'images_failed': self.stats.images_failed,
                    'external_images': self.stats.external_images,
                },
                'errors': self.stats.errors
            }
            log_file.write_text(json.dumps(report, indent=2))
            logger.info(f"Detailed report saved to {log_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Bulk recover images from Wayback Machine for Jekyll blog posts"
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help="Test run without making changes"
    )
    parser.add_argument(
        '--priority',
        choices=['critical', 'high', 'moderate', 'low', 'all'],
        default='all',
        help="Priority level of posts to process (default: all)"
    )

    args = parser.parse_args()

    recovery = WaybackImageRecovery(dry_run=args.dry_run)
    recovery.run(priority=args.priority)


if __name__ == "__main__":
    main()
