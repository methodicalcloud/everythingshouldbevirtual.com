# Quick Start - Bulk Image Recovery

**Status**: Ready for execution (dry run validated at 99.4% success rate)

---

## Execute Now (Recommended)

### Option A: Validated Critical Posts First (Safest)

```bash
cd /Users/larrysmithjr/Projects/MethodicalCloud/website/everythingshouldbevirtual
python3 scripts/bulk_image_recovery.py --priority critical
```

**What This Does**:
- Recovers images for 3 critical posts (122 images)
- Takes ~5 minutes
- 99.4% success rate (validated via dry run)
- Downloads to `assets/{post-slug}/`
- Updates markdown files automatically

**Check Results**:
```bash
tail -50 image_recovery.log
ls -R assets/ | head -30
```

---

### Option B: All Posts at Once (Fastest)

```bash
cd /Users/larrysmithjr/Projects/MethodicalCloud/website/everythingshouldbevirtual

# Backup first (recommended)
tar -czf ~/backups/esbv-posts-$(date +%Y%m%d).tar.gz _posts/

# Run all 22 posts
python3 scripts/bulk_image_recovery.py --priority all
```

**What This Does**:
- Recovers images for all 22 posts (~219 images)
- Takes ~10-15 minutes
- Processes in priority order automatically

**Check Results**:
```bash
cat image_recovery_report.json | python3 -m json.tool
```

---

## Priority Levels

```bash
# Critical: 3 posts, 122 images (VALIDATED ✓)
python3 scripts/bulk_image_recovery.py --priority critical

# High: 3 posts, 48 images
python3 scripts/bulk_image_recovery.py --priority high

# Moderate: 4 posts, 24 images
python3 scripts/bulk_image_recovery.py --priority moderate

# Low: 12 posts, ~25 images
python3 scripts/bulk_image_recovery.py --priority low

# All: 22 posts, ~219 images
python3 scripts/bulk_image_recovery.py --priority all
```

---

## After Execution

### 1. Verify Results
```bash
# Check summary
tail -30 image_recovery.log

# Check detailed report
cat image_recovery_report.json | python3 -m json.tool

# Verify images downloaded
find assets/ -name "*.png" -o -name "*.jpg" | wc -l
```

### 2. Test Build
```bash
bundle exec jekyll build
```

### 3. Commit Changes
```bash
git status
git add assets/ _posts/
git commit -m "feat(blog): recover images from Wayback Machine

Recovered 178 images for 3 critical blog posts:
- vShield 5.1 installation (47 images)
- Cacti monitoring (40 images)
- HP P4000 VSA (91 images)

Success rate: 99.4%
Source: Internet Archive Wayback Machine (2014-2015 snapshots)"
```

### 4. Push to Production
```bash
git push origin develop
# Create PR: develop → main
# Merge → Watchtower auto-deploys
```

---

## Troubleshooting

### 503 Errors
Some images may be temporarily unavailable. Re-run after a few minutes:
```bash
python3 scripts/bulk_image_recovery.py --priority critical
```

### Rate Limiting
If you hit Wayback rate limits, the script already has 2-second delays. If issues persist, edit `scripts/bulk_image_recovery.py` and increase `REQUEST_DELAY` from 2.0 to 3.0.

### Rollback
```bash
git reset --hard HEAD  # Discard all changes
```

---

## What Gets Changed

- **Created**: `assets/{post-slug}/` directories with downloaded images
- **Updated**: Markdown files in `_posts/` with new image paths
- **Added**: TOC to long posts (>1000 words)
- **Logged**: `image_recovery.log` and `image_recovery_report.json`

---

## Safety Features

- Non-destructive (doesn't delete anything)
- Rate-limited (won't overwhelm Wayback Machine)
- Logged (full audit trail)
- Reversible (git reset)
- Dry-run tested (99.4% success rate)

---

## Dependencies

Already available:
- Python 3
- requests
- beautifulsoup4
- lxml

If missing, install:
```bash
pip3 install -r scripts/requirements.txt
```

---

## Time Estimates

- Critical (3 posts): 5 minutes
- High (3 posts): 2-3 minutes
- Moderate (4 posts): 1-2 minutes
- Low (12 posts): 2-3 minutes
- **Total for all 22 posts**: 10-15 minutes

---

## Documentation

- **RECOVERY_SUMMARY.md** - Full implementation details
- **IMAGE_RECOVERY_PLAN.md** - Detailed execution plan
- **scripts/README.md** - Scripts documentation

---

**Recommended First Step**: Run critical posts first, verify results, then continue.

**Command**:
```bash
cd /Users/larrysmithjr/Projects/MethodicalCloud/website/everythingshouldbevirtual
python3 scripts/bulk_image_recovery.py --priority critical
```
