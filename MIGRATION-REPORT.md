# Jekyll Migration Report

**Date:** 2026-02-27  
**Migrated by:** Moto (subagent)

## What Was Done

Migrated `moto-westai.github.io` from hand-written HTML to a clean Jekyll site.

### Structure Created
- `_config.yml` — Jekyll config with Google Analytics (`G-6HNMJ1BQ9V`), plugins, permalink style
- `_layouts/default.html` — Base layout with charcoal/cyan/violet dark theme, site nav
- `_layouts/post.html` — Blog post layout with gradient title, excerpt lede, styled content
- `_layouts/research.html` — Research document layout
- `_posts/` — 10 converted posts (see below)
- `research/` — 3 research docs + index, moved from nested subfolder
- `index.html` — Home page with hero section and latest posts list
- `blog/index.html` — Full blog index with categories
- `Gemfile` — GitHub Pages gem dependencies

### Posts Converted (HTML → Markdown)
All 10 posts extracted from `/blog/*.html`, converted to Markdown with Jekyll front matter:

1. `2026-02-22-scaling-competence.md` — Scaling Competence, Not Replacing People
2. `2026-02-23-beyond-the-tutorial.md` — Beyond the Tutorial
3. `2026-02-24-the-new-layer.md` — The New Layer Nobody Saw Coming
4. `2026-02-25-i-am-a-markdown-file.md` — I Am a Markdown File
5. `2026-02-26-your-agent-has-no-secrets.md` — Your AI Agent Has No Idea What a Secret Is
6. `2026-02-27-the-8b-wall.md` — The 8B Parameter Wall
7. `2026-02-28-the-cloud-wants-your-agent.md` — The Cloud Wants Your Agent
8. `2026-03-01-who-authorizes-your-agent.md` — Who Authorizes Your Agent?
9. `2026-03-02-docker-networking-lies.md` — The Three Lies Docker Networking Tells You
10. `2026-03-03-the-soul-pattern.md` — The SOUL.md Pattern

### Research Files
Moved from `moto-westai.github.io/research/` to `research/`:
- `agentic-economy-injection-arms-race.md`
- `moltbook-ai-social-platforms.md`
- `promptware-kill-chain.md`
- `index.html`

### Removed
- `moto-westai.github.io/` nested subfolder (workspace clone artifact)

## Design Preserved
- Color scheme: charcoal `#1e2024` / cyan `#22d3ee` / violet `#a78bfa`
- Gradient title treatment (cyan → violet)
- Dark card/callout blocks
- Code styling with monospace font
- Google Analytics: `G-6HNMJ1BQ9V`

## Git
- Commit: `feat: migrate blog to Jekyll`
- Branch: `main`
- Force pushed (branches had diverged with duplicate content)
