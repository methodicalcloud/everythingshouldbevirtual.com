# Bulk Image Recovery from Wayback Machine

## Status: READY FOR EXECUTION

**Created**: December 18, 2025
**Dry Run Completed**: ✓ Successful (99.4% recovery rate)
**Total Posts**: 22 posts, ~219 images expected

---

## Dry Run Results (Critical Posts)

| Post | Expected | Found | Downloaded | Success |
|------|----------|-------|------------|---------|
| vShield 5.1 Install | 47 | 48 | 47 | 97.9% |
| Cacti Monitoring | 39 | 40 | 40 | 100% |
| HP P4000 VSA | 36 | 91 | 91 | 100% |
| **TOTAL** | **122** | **179** | **178** | **99.4%** |

**Note**: More images found than expected due to sidebar/footer content in archived pages.

### Issues Encountered

1. **503 Error**: 1 image unavailable (15-17-58_thumb.png) - Temporary Wayback service issue
2. **External Images**: 35 skipped (Gravatar, Google, ads) - Not in archive

---

## Execution Plan

### Phase 1: Critical Posts (VALIDATED)
- 3 posts, 122 expected images, 99.4% recovery rate
- **Command**: `python3 scripts/bulk_image_recovery.py --priority critical`
- **Duration**: ~5 minutes
- **Status**: ✓ Dry run successful

### Phase 2: High Priority Posts
- 3 posts, 48 images
- **Command**: `python3 scripts/bulk_image_recovery.py --priority high`
- **Estimated Duration**: ~2-3 minutes

### Phase 3: Moderate Priority Posts
- 4 posts, 24 images
- **Command**: `python3 scripts/bulk_image_recovery.py --priority moderate`
- **Estimated Duration**: ~1-2 minutes

### Phase 4: Low Priority Posts
- 12 posts, ~25 images
- **Command**: `python3 scripts/bulk_image_recovery.py --priority low`
- **Estimated Duration**: ~2-3 minutes
- **Note**: May have external images (Newegg) that won't recover

### Phase 5: Complete Bulk Run
- All 22 posts
- **Command**: `python3 scripts/bulk_image_recovery.py --priority all`
- **Estimated Duration**: ~10-15 minutes

---

## Pre-Execution Checklist

- [x] Dependencies installed (requests, beautifulsoup4, lxml)
- [x] Dry run validates approach
- [x] Rate limiting configured (2s delay between requests)
- [x] Error handling implemented
- [x] Logging configured
- [ ] Backup current `_posts/` directory (recommended)
- [ ] Review dry run logs for any concerns

---

## Execution Steps

### 1. Backup Current State (Recommended)

```bash
cd /Users/larrysmithjr/Projects/MethodicalCloud/website/everythingshouldbevirtual
tar -czf ~/backups/esbv-posts-$(date +%Y%m%d).tar.gz _posts/
```

### 2. Run Critical Posts (Validated)

```bash
cd /Users/larrysmithjr/Projects/MethodicalCloud/website/everythingshouldbevirtual
python3 scripts/bulk_image_recovery.py --priority critical
```

### 3. Verify Results

```bash
# Check logs
tail -100 image_recovery.log

# Check report
cat image_recovery_report.json | python3 -m json.tool

# Check downloaded images
ls -R assets/ | head -50

# Verify markdown updates
git diff _posts/2012/2012-11-15-how-to-install-vshield-5-1-manager-app-and-endpoint-2.md
```

### 4. Continue with Remaining Priorities

```bash
# High priority
python3 scripts/bulk_image_recovery.py --priority high

# Moderate priority
python3 scripts/bulk_image_recovery.py --priority moderate

# Low priority
python3 scripts/bulk_image_recovery.py --priority low
```

### 5. OR Run All at Once

```bash
# Process all 22 posts in one go
python3 scripts/bulk_image_recovery.py --priority all
```

---

## Post-Execution Verification

### 1. Check Recovery Stats

```bash
cat image_recovery_report.json | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f'Posts Attempted: {d[\"stats\"][\"posts_attempted\"]}')
print(f'Posts Succeeded: {d[\"stats\"][\"posts_succeeded\"]}')
print(f'Images Downloaded: {d[\"stats\"][\"images_downloaded\"]}')
print(f'Images Failed: {d[\"stats\"][\"images_failed\"]}')
print(f'Success Rate: {(d[\"stats\"][\"posts_succeeded\"] / d[\"stats\"][\"posts_attempted\"] * 100):.1f}%')
"
```

### 2. Verify Image Files

```bash
# Count downloaded images per post
for dir in assets/*/; do
  echo "$(basename $dir): $(find $dir -type f | wc -l) images"
done
```

### 3. Test Local Build

```bash
# Build site locally to verify no broken images
bundle exec jekyll build
# Check for broken image references
grep -r "!\[.*\](../../assets/" _site/ | grep -v ".png\|.jpg\|.gif"
```

### 4. Commit Changes

```bash
git status
git add assets/ _posts/
git commit -m "feat(blog): recover 178 images from Wayback Machine for 3 critical posts

- vShield 5.1 installation: 47 images
- Cacti monitoring: 40 images
- HP P4000 VSA: 91 images
- Success rate: 99.4%
- 1 image unavailable due to Wayback 503 error

Images recovered from Internet Archive's Wayback Machine using automated
bulk recovery script. Original WordPress wp-content/uploads URLs archived
between 2014-2015."
```

---

## Known Limitations

1. **External Images**: Images hosted on external sites (Newegg, Gravatar, ads) cannot be recovered
2. **Wayback Availability**: Some images may return 503 errors if Wayback service is temporarily unavailable
3. **Duplicate Images**: Some posts may have more images than expected due to sidebar/footer content
4. **Alt Text**: Auto-generated as "Step N" for screenshots - may need manual review for accessibility

---

## Troubleshooting

### Rate Limiting Issues
If you hit Wayback rate limits, increase `REQUEST_DELAY` in `bulk_image_recovery.py`:

```python
REQUEST_DELAY = 3.0  # Increase from 2.0 to 3.0 seconds
```

### 503 Service Unavailable Errors
These are temporary. Re-run the script after a few minutes:

```bash
# Re-run just failed posts
python3 scripts/bulk_image_recovery.py --priority critical
```

### Image Path Issues
If markdown updates don't work, check the regex pattern in `update_markdown()` function.

---

## Success Criteria

- **Primary**: 90%+ of images recovered
- **Secondary**: All critical posts (3) completed
- **Tertiary**: High priority posts (3) completed

**Current Dry Run Performance**: 99.4% ✓ Exceeds criteria

---

## Next Steps After Execution

1. **Verify**: Test local Jekyll build
2. **Review**: Spot-check a few posts for image quality
3. **Commit**: Add to git with descriptive message
4. **Deploy**: Push to production (Watchtower auto-deploys)
5. **Monitor**: Check production site for broken images
6. **Cleanup**: Archive dry run logs and test scripts

---

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `bulk_image_recovery.py` | Main recovery script (all functionality) |
| `test_single_recovery.py` | Test Wayback availability for one post |
| `discover_slugs.py` | Find WordPress slugs when filenames don't match |
| `requirements.txt` | Python dependencies |
| `README.md` | Scripts documentation |

---

**Recommended Approach**: Start with critical posts, verify results, then proceed to remaining priorities.

**Estimated Total Time**: 15-20 minutes for all 22 posts

**Risk Level**: LOW (dry run validated, rate-limited, error-handled, non-destructive with `--dry-run` flag)
