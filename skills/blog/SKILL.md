---
name: blog
description: "Publish posts to Moto's blog at moto-westai.github.io/blog. Use when writing, editing, or publishing blog posts."
homepage: https://moto-westai.github.io/blog
metadata: { "openclaw": { "emoji": "✍️", "requires": { "bins": ["git"] } } }
---

# Blog Skill

Write and publish posts to Moto's Jekyll blog at [moto-westai.github.io/blog](https://moto-westai.github.io/blog).

## When to Use

✅ **USE this skill when:**
- Writing a new blog post
- Editing or updating an existing post
- Publishing/pushing changes to the live blog
- Checking blog post status or history

## Repository

- **Local repo:** `~/projects/west_ai_labs/moto-westai.github.io/`
- **Remote:** `moto-westai/moto-westai.github.io` on GitHub
- **SSH key:** `~/.ssh/id_ed25519_moto`
- **Push command:**
  ```bash
  GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_moto" git push origin main
  ```

## Post Format

Posts live in `_posts/` with Jekyll frontmatter:

```yaml
---
layout: post
title: "Title Here"
date: YYYY-MM-DD
categories: [cat1, cat2]
---

Body content here in Markdown...

*Moto is the AI infrastructure engineer at West AI Labs.*
```

### Rules
- **Date format:** `YYYY-MM-DD` (no time needed)
- **Footer:** Every post must end with `*Moto is the AI infrastructure engineer at West AI Labs.*`
- **Filename:** `_posts/YYYY-MM-DD-title-slug.md`
- **Commit convention:** `feat(blog): add post - title-slug`

## URL Pattern

After publishing, posts are available at:
```
https://moto-westai.github.io/YYYY/MM/DD/title-slug/
```

## ⚠️ Hard Rules

- **NEVER create HTML files in `blog/`** — that folder is hands-off legacy redirects, do not touch it
- **NEVER write raw HTML posts** — markdown in `_posts/` only, Jekyll handles the build
- **NEVER post to `moto-westai-blog/`** — main site only: `moto-westai.github.io/_posts/`

## Workflow

```bash
# 1. Pull latest before starting (ALWAYS do this first)
cd ~/projects/west_ai_labs/moto-westai.github.io && git pull

# 2. Create/edit the post file
# _posts/YYYY-MM-DD-title-slug.md

# 3. Stage and commit
git add _posts/YYYY-MM-DD-title-slug.md
git commit -m "feat(blog): add post - title-slug"

# 4. Push to GitHub Pages
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_moto" git push origin main
```

## After Publishing — Social Graphic + Drafts (MANDATORY)

After every successful publish, do both steps and deliver to Discord (#jlwestsr-office, channel `1475994576668852254`).

### Step 1 — Generate Social Graphic
Use the image tool to create a 1200x630 social share image:
- **Style:** West AI Labs Night Ride — deep charcoal (#1e2024) background, cyan (#22d3ee) or violet (#a78bfa) accent
- **Content:** Bold headline summarizing the post's core idea
- **Feel:** Minimal, clean, tech-forward — no clip art, no gradients, no stock photo vibes
- **Save to:** `/home/jlwestsr/.openclaw/workspace/social/YYYY-MM-DD-[slug]-social.png`
- **Example prompt:** `"Dark charcoal background, bold cyan headline: [POST TITLE], minimal tech aesthetic, West AI Labs brand, 1200x630"`

### Step 2 — Draft Social Posts

**Voice rule (mandatory):** Moto writes the content. Jason promotes it. Social drafts must reflect this honestly:
- **Personal posts:** Frame as "my AI wrote this / here's why I stand behind it" — never imply Jason wrote it
- **Company posts:** Lead with what shipped, credit Moto as author
- This is the brand story: a founder with an AI partner that does real work, transparent about it

```
---
📣 SOCIAL DRAFTS — [Post Title]
URL: https://moto-westai.github.io/YYYY/MM/DD/title-slug/
🖼️ Graphic: /home/jlwestsr/.openclaw/workspace/social/[filename].png

**X — @jlwestsr (personal)**
[140-200 chars, first person, direct voice, 1-2 hashtags max]

**X — @WestAILabs (company)**
[140-200 chars, company voice, what shipped]

**LinkedIn — Jason West (personal)**
[2-3 sentences, professional but direct, insight or lesson]

**LinkedIn — West AI Labs (company)**
[2-3 sentences, company angle, value for engineers/enterprises]
---
```

Copy-paste ready. No placeholder text. Written as if posting right now.

## Notes

- Always `git pull` before writing new posts to avoid merge conflicts
- GitHub Pages auto-builds from `main` branch; allow ~30–60s for posts to go live
- Categories affect the URL path — keep them lowercase, no spaces
- Git flow: work on `develop` branch → merge to `main` → push `main` → checkout `develop`
