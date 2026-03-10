---
name: scrapling
description: "Scrape any website with anti-bot bypass using Scrapling. Use when you need to fetch web content from protected sites (LinkedIn, job boards, Cloudflare-protected pages), extract structured data, or scrape pages that block web_fetch."
homepage: https://github.com/D4Vinci/Scrapling
metadata: { "openclaw": { "emoji": "🕷️", "requires": { "bins": ["npx"] } } }
---

# Scrapling Skill

Bypass bot protection and scrape pages that block `web_fetch`. Backed by Scrapling MCP via mcporter.

## When to Use

| Situation | Tool |
|-----------|------|
| Public docs, GitHub READMEs, simple pages | `web_fetch` (faster, no overhead) |
| Mild bot protection, standard HTTP needed | `scrapling get` |
| LinkedIn, job boards, Cloudflare-protected | `scrapling stealthy_fetch` |
| JS-rendered pages (React/Vue SPAs) | `scrapling fetch` (Playwright) |

## Commands

### Fast HTTP Fetch
```bash
npx mcporter call --stdio "scrapling mcp" get 'url=URL' extraction_type=markdown
```

### Stealthy — Cloudflare Bypass, LinkedIn, Job Boards
```bash
npx mcporter call --stdio "scrapling mcp" stealthy_fetch 'url=URL' extraction_type=markdown
```

### JS-Rendered Pages (Playwright browser)
```bash
npx mcporter call --stdio "scrapling mcp" fetch 'url=URL' extraction_type=markdown
```

### With CSS Selector
```bash
npx mcporter call --stdio "scrapling mcp" get 'url=URL' 'css_selector=.job-title' extraction_type=markdown
```

### Parse Output (always JSON)
```bash
... | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0])"
```

### extraction_type Options
- `markdown` — clean readable text (default, best for LLM consumption)
- `html` — raw HTML (use for CSS selectors / structure inspection)
- `text` — plain text, no formatting

---

## Common Patterns

### 1. LinkedIn Job Search
```bash
npx mcporter call --stdio "scrapling mcp" stealthy_fetch \
  'url=https://www.linkedin.com/jobs/search/?keywords=software+engineer&location=St.+Louis' \
  extraction_type=markdown \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0])"
```
> Always use `stealthy_fetch` for LinkedIn — regular HTTP is blocked.

### 2. Indeed Job Search
```bash
npx mcporter call --stdio "scrapling mcp" stealthy_fetch \
  'url=https://www.indeed.com/jobs?q=software+engineer&l=remote' \
  extraction_type=markdown \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0])"
```

### 3. GitHub Search
```bash
npx mcporter call --stdio "scrapling mcp" get \
  'url=https://github.com/search?q=scrapling&type=repositories' \
  extraction_type=markdown \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0])"
```
> GitHub rarely needs stealth; use `get` unless blocked.

### 4. Generic News / Article Fetch
```bash
npx mcporter call --stdio "scrapling mcp" get \
  'url=https://techcrunch.com/some-article' \
  extraction_type=markdown \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['content'][0])"
```
> Use `stealthy_fetch` if `get` returns empty or a CAPTCHA page.

### 5. Status / Accessibility Check
```bash
# Check if a page is reachable and what it returns
npx mcporter call --stdio "scrapling mcp" get 'url=URL' extraction_type=text \
  | python3 -c "
import sys, json
d = json.load(sys.stdin)
content = d.get('content', [''])[0]
print(f'Status: OK | Length: {len(content)} chars')
print(content[:500])
"
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Empty content / CAPTCHA text returned | Switch to `stealthy_fetch` |
| Page renders blank (SPA) | Switch to `fetch` (Playwright) |
| Playwright/browser errors | `sudo python3 -m playwright install-deps chromium` |
| `mcporter` not found | `npm install -g mcporter` |

---

## Notes

- **Binary:** `/home/jlwestsr/.local/bin/scrapling`
- **mcporter** bridges stdio MCP transport — required to call scrapling tools from the shell
- `stealthy_fetch` is slower (rotating fingerprints + headers) but far more reliable for protected sites
- `fetch` spins up a real Chromium browser; slowest but handles any JS-heavy page
- Prefer `markdown` extraction for LLM tasks; `html` when you need to dig into structure
- Playwright browser deps: `sudo python3 -m playwright install-deps chromium` if browser tools fail
