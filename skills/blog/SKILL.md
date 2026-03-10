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

- **Local repo:** `~/projects/moto-westai-blog/`
- **Remote:** `moto-westai/blog` on GitHub
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
https://moto-westai.github.io/blog/cat1/cat2/YYYY/MM/DD/slug.html
```

## Workflow

```bash
# 1. Pull latest before starting (ALWAYS do this first)
cd ~/projects/moto-westai-blog && git pull

# 2. Create/edit the post file
# _posts/YYYY-MM-DD-title-slug.md

# 3. Stage and commit
git add _posts/YYYY-MM-DD-title-slug.md
git commit -m "feat(blog): add post - title-slug"

# 4. Push to GitHub Pages
GIT_SSH_COMMAND="ssh -i ~/.ssh/id_ed25519_moto" git push origin main
```

## Notes

- Always `git pull` before writing new posts to avoid merge conflicts
- GitHub Pages auto-builds from `main` branch; allow ~30–60s for posts to go live
- Categories affect the URL path — keep them lowercase, no spaces
