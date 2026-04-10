# Everything Should Be Virtual

[Everything Should Be Virtual](https://everythingshouldbevirtual.com) is a technical blog covering virtualization, cloud technologies, automation, and DevOps. Part of [Methodical Cloud](https://methodicalcloud.com).

---

## Tech Stack

- **Static Site Generator**: [Jekyll](https://jekyllrb.com/) with [Minimal Mistakes](https://mmistakes.github.io/minimal-mistakes/) theme
- **Hosting**: [Cloudflare Pages](https://pages.cloudflare.com/)
- **CI**: GitHub Actions (`ruby/setup-ruby` + `cloudflare/wrangler-action`)

---

## Deployment

Push to `main` triggers a full build and deploy automatically.

```text
develop → PR → main → GitHub Actions → Cloudflare Pages (everythingshouldbevirtual.com)
```

Manual deploy (if needed):

```bash
bundle exec jekyll build
wrangler pages deploy _site --project-name everythingshouldbevirtual --branch main
```

**GitHub Secrets required**:
- `CLOUDFLARE_ACCOUNT_ID`
- `CLOUDFLARE_PAGES_TOKEN`

---

## Local Development

```bash
bundle install
bundle exec jekyll serve --drafts
```

Requires Ruby 3.x. The site builds with Ruby 3.3 in CI.

---

## Writing Posts

Add a file to `_posts/` with the format `YYYY-MM-DD-title.md`:

```yaml
---
title: "Post Title"
date: YYYY-MM-DD HH:MM:SS -0500
categories:
  - Automation
tags:
  - ansible
toc: true
---
```

Drafts go in `_drafts/` and are excluded from production builds.

---

**Author**: Larry Smith Jr. | **Last Updated**: April 2026
