# Image Recovery Scripts

This directory contains scripts for recovering missing images from the Internet Archive's Wayback Machine for the Everything Should Be Virtual blog.

## Setup

Install dependencies:

```bash
pip3 install -r requirements.txt
```

## Usage

### Bulk Image Recovery

Recover images for multiple posts systematically:

```bash
# Dry run (test without making changes)
python3 bulk_image_recovery.py --dry-run

# Process only critical posts (47, 39, 36 images each)
python3 bulk_image_recovery.py --priority critical

# Process high priority posts (21, 14, 13 images each)
python3 bulk_image_recovery.py --priority high

# Process all posts
python3 bulk_image_recovery.py --priority all
```

### Priority Levels

- **critical**: 3 posts with 36-47 images each (122 total)
- **high**: 3 posts with 13-21 images each (48 total)
- **moderate**: 4 posts with 3-10 images each (24 total)
- **low**: 12 posts with 1-3 images each (~25 total)
- **all**: All 22 posts (default)

## How It Works

1. **Query Wayback Machine**: Checks if the original WordPress post URL is archived
2. **Fetch Archived HTML**: Downloads the archived page content
3. **Extract Images**: Finds base64 inline images and wp-content/uploads URLs
4. **Download/Decode**: Saves images to `assets/{post-slug}/` directory
5. **Update Markdown**: Updates post with new image paths and alt text
6. **Add TOC**: Adds table of contents to posts with 1000+ words

## Output

- **Logs**: `image_recovery.log` - Detailed processing log
- **Report**: `image_recovery_report.json` - JSON summary of results
- **Images**: `assets/{post-slug}/` - Downloaded images per post

## Notes

- Rate limited to avoid overwhelming Wayback Machine (2 second delay between requests)
- External images (e.g., Newegg) are skipped - not in Wayback archive
- Some posts may not be archived - these are logged as failures
- Alt text is auto-generated as "Step N" for sequential screenshots

## Success Criteria

Validated approach based on successful Veeam post recovery:
- Wayback Machine availability API works reliably
- Base64 and URL-based images both recoverable
- Markdown updates preserve post formatting
- TOC added to long posts for better UX
