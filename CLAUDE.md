# Instructions for Claude - Everything Should Be Virtual

> **Note**: For global standards (git workflow, code standards, documentation rules), see `~/.claude/CLAUDE.md`. For MC org standards, see `/Users/larrysmithjr/Projects/MethodicalCloud/CLAUDE.md`.

**Website**: Everything Should Be Virtual (Technical Blog)
**Organization**: Methodical Cloud
**URL**: <https://everythingshouldbevirtual.com>
**Repository**: <https://github.com/methodicalcloud/everythingshouldbevirtual.github.io> (Private)
**Last Updated**: December 2025

---

## Blog Overview

**Purpose**: Technical blog covering virtualization, cloud technologies, automation, and DevOps. Content-driven resource providing tutorials, insights, and educational materials.

**Author**: Larry Smith Jr.

**Target Audience**: IT professionals, DevOps engineers, cloud architects, automation enthusiasts, virtualization administrators.

**Content Focus**:

- Virtualization (VMware, Proxmox, KVM)
- Cloud technologies (AWS, Azure, GCP)
- Automation (Ansible, Terraform, Python)
- DevOps practices and tools
- Home lab setups and experiments
- Container orchestration (Docker, Kubernetes)

---

## Technical Stack

**Static Site Generator**: Jekyll (Ruby-based)
**Theme**: Minimal Mistakes (remote theme: `mmistakes/minimal-mistakes@4.24.0`)
**Comments**: Disqus
**Hosting**: GHCR container via Watchtower auto-deployment
**Build**: Docker-based Jekyll build

---

## Repository Structure

```text
everythingshouldbevirtual/
├── _config.yml          # Jekyll site configuration
├── _posts/              # Blog posts (Markdown)
├── _pages/              # Static pages
├── _drafts/             # Unpublished drafts
├── assets/              # Images, CSS, JS
├── images/              # Blog images
├── Dockerfile           # Container build
├── Gemfile              # Ruby dependencies
└── package.json         # Node dependencies (for tooling)
```

---

## Content Guidelines

### Blog Post Format

**Filename**: `YYYY-MM-DD-post-title.md` in `_posts/`

**Front Matter**:

```yaml
---
title: "Post Title"
date: YYYY-MM-DD HH:MM:SS -0500
categories:
  - category1
  - category2
tags:
  - tag1
  - tag2
toc: true
toc_label: "Table of Contents"
---
```

**Writing Style**:

- Technical but approachable
- Include code examples with syntax highlighting
- Step-by-step tutorials where applicable
- Screenshots for UI-based instructions
- Link to official documentation

### Categories

Common categories used:

- `Automation`
- `Virtualization`
- `Containers`
- `DevOps`
- `Cloud`
- `Networking`
- `Linux`
- `Home Lab`

---

## Deployment

**Production Flow**:

```
develop (push) → CI builds :develop tag
            ↓
    PR: develop → main
            ↓
main (merge) → build-and-push → :latest tag → Watchtower auto-deploys
```

**Container Image**: `ghcr.io/methodicalcloud/everythingshouldbevirtual.github.io:latest`

**Local Development**:

```bash
# Install dependencies
bundle install

# Serve locally
bundle exec jekyll serve --drafts
```

---

## Relationship to Methodical Cloud

Everything Should Be Virtual is a **content property** under Methodical Cloud, focused on educational content rather than product promotion. The blog:

- Maintains editorial independence
- May reference Methodical Cloud products when relevant
- Links to methodicalcloud.com in footer
- Uses personal branding (Larry Smith Jr.) rather than corporate

---

## SEO & Content Strategy

**Primary Topics**:

- Ansible automation tutorials
- Docker and container guides
- VMware/virtualization how-tos
- Home lab builds and experiments
- DevOps tooling comparisons

**Long-Form Content**: Target 1,500+ words for SEO value
**Code Examples**: Always tested before publishing
**Updates**: Refresh older posts when technology changes significantly

---

## Licensing

**Theme**: MIT License (Minimal Mistakes by Michael Rose)
**Blog Content**: All Rights Reserved - Larry Smith Jr. / Methodical Cloud LLC

See `LICENSE.md` for complete licensing details.

---

## Contact

**Author**: Larry Smith Jr.
**Email**: <mrlesmithjr@gmail.com>
**GitHub**: <https://github.com/mrlesmithjr>
**LinkedIn**: <https://www.linkedin.com/in/mrlesmithjr/>
**Twitter**: <https://twitter.com/mrlesmithjr>

---

**Last Updated**: December 2025
**Document Version**: 1.0
