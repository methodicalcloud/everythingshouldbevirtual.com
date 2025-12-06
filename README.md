# Everything Should Be Virtual

[![Build](https://img.shields.io/badge/build-GHCR-blue)](https://github.com/methodicalcloud/everythingshouldbevirtual.github.io/pkgs/container/everythingshouldbevirtual.github.io)
[![Deploy](https://img.shields.io/badge/deploy-Watchtower-green)](https://containrrr.dev/watchtower/)

[Everything Should Be Virtual](https://everythingshouldbevirtual.com) is a technical blog covering virtualization, cloud technologies, automation, and DevOps. Part of [Methodical Cloud](https://methodicalcloud.com).

---

## Tech Stack

- **Static Site Generator**: [Jekyll](https://jekyllrb.com/) with [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme
- **Container**: Docker (multi-stage build)
- **Registry**: GitHub Container Registry (GHCR)
- **Deployment**: Watchtower auto-deployment on Stackbox

---

## Deployment Architecture

```text
develop (push) → GitHub Actions → ghcr.io/methodicalcloud/everythingshouldbevirtual.github.io:develop
                      ↓
              PR: develop → main
                      ↓
  main (merge) → GitHub Actions → ghcr.io/methodicalcloud/everythingshouldbevirtual.github.io:latest
                      ↓
              Watchtower auto-deploys → stackbox.home.lan (within 5 min)
```

**Production URL**: https://everythingshouldbevirtual.com

---

## Local Development

### Option 1: Native Jekyll

```bash
# Install dependencies
gem install jekyll bundler
bundle install

# Serve locally (with drafts)
bundle exec jekyll serve --drafts

# Access at http://localhost:4000
```

### Option 2: Docker

```bash
# Build container
docker build -t esbv:local .

# Run locally
docker run -p 4000:4000 esbv:local

# Access at http://localhost:4000
```

---

## Repository Structure

```text
everythingshouldbevirtual/
├── _posts/              # Published blog posts
├── _drafts/             # Unpublished drafts
├── _pages/              # Static pages
├── assets/              # CSS, JS, images
├── _config.yml          # Jekyll configuration
├── Dockerfile           # Multi-stage Docker build
├── Gemfile              # Ruby dependencies
└── package.json         # Node dependencies (build tools)
```

---

## Writing New Posts

1. Create file in `_posts/` with format: `YYYY-MM-DD-post-title.md`
2. Add front matter:

```yaml
---
title: "Post Title"
date: 2025-12-06 10:00:00 -0500
categories:
  - Automation
tags:
  - ansible
  - docker
toc: true
---
```

3. Write content in Markdown
4. Preview locally with `bundle exec jekyll serve --drafts`
5. Commit to `develop`, create PR to `main`

---

## License

- **Theme**: MIT License (Minimal Mistakes by Michael Rose)
- **Content**: All Rights Reserved - Larry Smith Jr. / Methodical Cloud LLC

See [LICENSE.md](LICENSE.md) for details.

---

## Contact

- **Author**: Larry Smith Jr.
- **Email**: mrlesmithjr@gmail.com
- **GitHub**: [@mrlesmithjr](https://github.com/mrlesmithjr)
- **Organization**: [Methodical Cloud](https://methodicalcloud.com)

---

**Last Updated**: December 2025
