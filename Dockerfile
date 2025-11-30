# Multi-stage Dockerfile for Everything Should Be Virtual (Jekyll blog)
# Stage 1: Build Jekyll site
# Stage 2: Serve with nginx

# Build stage - Jekyll
FROM ruby:3.2-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /site

# Copy Gemfile first for layer caching
COPY Gemfile Gemfile.lock* ./

# Install Jekyll and dependencies
RUN bundle install --jobs 4 --retry 3

# Copy site source
COPY . .

# Build the Jekyll site
RUN bundle exec jekyll build --destination /site/_site

# Production stage - nginx
FROM nginx:alpine AS production

# Copy built site to nginx
COPY --from=builder /site/_site /usr/share/nginx/html

# Copy custom nginx config if needed
# COPY nginx.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Run nginx
CMD ["nginx", "-g", "daemon off;"]
