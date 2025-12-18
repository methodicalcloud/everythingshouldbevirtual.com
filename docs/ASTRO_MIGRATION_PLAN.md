# ESBV Astro Migration Plan

**Status**: Planned (Deferred)
**Created**: December 15, 2025
**Author**: Methodical Cloud Architect

## Summary

Migration from Jekyll + Minimal Mistakes to Astro for better performance, modern design, and improved developer experience.

---

## Current State

- **Stack**: Jekyll 4.4 + Minimal Mistakes theme
- **Content**: ~349 markdown posts (2012-2025)
- **Deployment**: Docker → GHCR → Watchtower
- **Comments**: Disqus
- **Permalink**: `/:categories/:title/`

## Target State

- **Stack**: Astro 4.x + Tailwind CSS + MC Design System
- **Comments**: Giscus (GitHub Discussions)
- **Search**: Pagefind (static, zero-JS)
- **Theme**: Dark (MC navy aesthetic)

---

## Phases

### Phase 1: Astro Setup (2 days)

```bash
mkdir astro-esbv && cd astro-esbv
npm create astro@latest -- --template minimal
npm install @astrojs/sitemap @astrojs/rss astro-icon sharp
npm install -D @tailwindcss/typography tailwindcss postcss autoprefixer
```

**Key files:**
- `astro.config.mjs` - Site config, integrations
- `tailwind.config.cjs` - MC colors, typography
- `src/content/config.ts` - Content collection schema

### Phase 2: Components (3 days)

Build these Astro components:
- `BaseLayout.astro` - HTML shell with MC styling
- `EcosystemBar.astro` - MC ecosystem navigation
- `Header.astro` - Site masthead with logo
- `Footer.astro` - MC branded footer
- `PostCard.astro` - Blog post preview card
- `Comments.astro` - Giscus integration

### Phase 3: Content Migration (3-5 days)

Migration script handles:
- Jekyll frontmatter → Astro content collections
- Date format normalization
- Category/tag array normalization
- Image path fixes (`../../assets/` → `/assets/`)
- Jekyll includes → HTML/Astro components
- Generate redirects file for SEO

### Phase 4: Dynamic Routes (2 days)

- `[...slug].astro` - Blog posts with preserved URLs
- `categories/[category].astro` - Category archives
- `tags/[tag].astro` - Tag archives
- `rss.xml.ts` - RSS feed

### Phase 5: Search (1 day)

Pagefind integration:
```json
{
  "scripts": {
    "build": "astro build && npx pagefind --site dist"
  }
}
```

### Phase 6: Docker (1 day)

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Phase 7: Testing (2 days)

- Lighthouse audits (target: 90+ performance)
- URL validation (no 404s)
- Image rendering check
- RSS feed validation
- Mobile responsiveness

### Phase 8: Deployment (1 day)

- Update GitHub Actions workflow for Node.js build
- Merge to main, Watchtower auto-deploys
- Monitor for errors

---

## Giscus Setup

1. Enable GitHub Discussions on repo
2. Install Giscus app: https://github.com/apps/giscus
3. Configure at https://giscus.app
4. Add component with repo/category IDs

---

## Content Collection Schema

```typescript
import { defineCollection, z } from 'astro:content';

const blog = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    categories: z.array(z.string()).optional().default([]),
    tags: z.array(z.string()).optional().default([]),
    description: z.string().optional(),
    draft: z.boolean().optional().default(false),
    legacyUrl: z.string().optional(),
  }),
});

export const collections = { blog };
```

---

## MC Design Integration

### Tailwind Colors
```javascript
colors: {
  'mc-navy': {
    900: '#0f172a',
    800: '#1e293b',
    700: '#334155',
  },
  'mc-blue': {
    700: '#1D4ED8',
    600: '#2563EB',
    500: '#3b82f6',
    400: '#60a5fa',
    300: '#93C5FD',
  },
}
```

### Base Styling
- Dark theme default
- MC navy background
- MC blue accents for links/CTAs
- Ecosystem bar at top of footer
- MC logo in header

---

## Success Criteria

- [ ] All 349 posts migrated
- [ ] Zero 404s on existing URLs
- [ ] Lighthouse Performance > 90
- [ ] Lighthouse SEO > 95
- [ ] Comments working via Giscus
- [ ] RSS feed functional
- [ ] Search operational
- [ ] Build time < 2 minutes
- [ ] Docker image < 50MB

---

## Rollback Plan

Keep Jekyll Dockerfile tagged as `jekyll-backup`:
```bash
docker tag esbv:local ghcr.io/methodicalcloud/everythingshouldbevirtual.github.io:jekyll-backup
docker push ghcr.io/methodicalcloud/everythingshouldbevirtual.github.io:jekyll-backup
```

---

## Resources

- [Astro Docs](https://docs.astro.build)
- [Pagefind](https://pagefind.app)
- [Giscus](https://giscus.app)
- [AstroPaper Template](https://github.com/satnaing/astro-paper)

---

**Estimated Duration**: 16-18 days
