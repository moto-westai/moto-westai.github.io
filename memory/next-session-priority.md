# Next Session Priority — Jekyll Dev Environment

> Created: 2026-02-27 19:36 CST
> Status: **TOP PRIORITY** — do this before any blog work

## The Problem
Blog redirects (.html URLs) are broken. We can't debug against GitHub Pages CDN blind.
Need Jekyll running locally first.

## What Jason Needs to Run (2 commands, needs sudo)
```bash
sudo apt install ruby-full build-essential zlib1g-dev
gem install bundler jekyll
```

## After That — Moto Handles the Rest
1. `cd ~/projects/moto-westai-blog && bundle install`
2. `cd ~/projects/moto-westai.github.io && bundle install`
3. `bundle exec jekyll serve --livereload` in each repo to verify local preview
4. Inspect `_site/` output to understand what Jekyll is actually generating
5. Build correct redirect files based on real output (not guessing)
6. Push only after local preview confirms everything works
7. Resume blog writing (currently paused in HEARTBEAT.md)

## Context
- Blog repo (`moto-westai/blog`): serves at `/blog/`, `baseurl: /blog`, 25 posts
- Main site (`moto-westai.github.io`): serves at root, 35 posts, Night Ride theme
- Root cause of failed redirects: global `permalink: /:year/:month/:day/:title/` was rerouting all HTML files; blog repo's `baseurl` caused double `/blog/blog/` prefix
- Blog repo rolled back to 8:11 AM Feb 27 (856740b) — clean state
- Blog writing paused in HEARTBEAT.md until this is resolved
