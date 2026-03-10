# Scrapling MCP Server — Setup & Integration Research

**Date:** 2026-02-23  
**Researcher:** Moto subagent (scrapling-mcp-research)  
**System:** Ubuntu 24.04, Python 3.12.3, OpenClaw 2026.2.23  

---

## Summary

✅ **Scrapling v0.4 is installed and working.** The MCP server runs in both stdio and HTTP modes. `get` and `bulk_get` (HTTP-only fetchers) work without browser deps. Browser-based tools (`fetch`, `stealthy_fetch`) are also available — playwright/patchright browsers are installed in `~/.cache/ms-playwright/`.

⚠️ **OpenClaw does not natively support MCP servers yet** (feature request: openclaw/openclaw#4834, filed ~3 weeks ago). However, **two reliable workarounds exist today** and are tested working.

---

## Installation

### What was installed

```bash
pip3 install "scrapling[ai]" --user --break-system-packages
```

- **Package:** `scrapling==0.4` at `/home/jlwestsr/.local/bin/scrapling`
- **Deps installed:** playwright, patchright, curl_cffi, markdownify, browserforge, mcp (FastMCP), uvicorn
- **Browsers:** patchright/playwright chromium available in `~/.cache/ms-playwright/chromium-1194/`

> ⚠️ Ubuntu 24.04 uses an "externally managed" Python environment. The `--break-system-packages` flag was used. Safe here since it's user-local (`--user`). Alternatively use `pipx install scrapling` or a venv.

### `scrapling install` browser deps

The `scrapling install` command tries to run `playwright install-deps` which requires root for apt packages. It failed. However, the browsers themselves were already successfully installed via `python3 -m patchright install chromium`. The browser binaries are present and functional.

**To install system browser deps (requires sudo — do once if browser tools fail):**
```bash
sudo python3 -m playwright install-deps chromium
```

---

## MCP Server Details

### Start Commands

**Stdio mode (default — for MCP protocol):**
```bash
scrapling mcp
```

**HTTP/SSE mode (persistent server):**
```bash
scrapling mcp --http --host 0.0.0.0 --port 8000
```

### Transport Behavior

- **stdio**: Reads JSON-RPC from stdin, writes to stdout. Standard MCP protocol. ✅ Tested working.
- **streamable-http**: Runs a uvicorn/FastAPI server. Requires clients to accept both `application/json` AND `text/event-stream` headers. Standard curl won't work; needs an MCP-aware client.

### Tools Exposed (6 total)

All tools return `{ status: int, content: [str], url: str }`.

| Tool | Description | Requires Browser |
|------|-------------|-----------------|
| `get` | HTTP GET — fast, TLS fingerprint spoofing, Chrome impersonation | ❌ HTTP only |
| `bulk_get` | Parallel HTTP GET for multiple URLs | ❌ HTTP only |
| `fetch` | Playwright browser fetch — handles JS-rendered pages | ✅ Patchright/Chromium |
| `bulk_fetch` | Parallel browser fetch for multiple URLs | ✅ Patchright/Chromium |
| `stealthy_fetch` | Full stealth mode — Cloudflare Turnstile bypass, fingerprint spoofing | ✅ Patchright/Chromium |
| `bulk_stealthy_fetch` | Parallel stealthy fetch for multiple URLs | ✅ Patchright/Chromium |

#### Tool Parameters (key ones)

All tools share these common parameters:
- `url` / `urls` — required
- `extraction_type` — `"markdown"` (default), `"html"`, `"text"`
- `css_selector` — optional, CSS selector to target specific page elements
- `main_content_only` — default `true`, extracts `<body>` content only
- `impersonate` — browser version to spoof (e.g. `"chrome"`, `"firefox135"`, `"safari184"`)
- `proxy` — optional proxy URL
- `timeout` — seconds (default 30 for HTTP, 30000ms for browser tools)
- `retries` — default 3 (HTTP tools)

Browser tools also support:
- `headless` — default `true`
- `network_idle` — wait for network to settle
- `solve_cloudflare` — auto-solve Cloudflare Turnstile (stealthy tools only)
- `real_chrome` — use the system's Chrome install instead of patchright

---

## OpenClaw Integration

### Current State (OpenClaw 2026.2.23)

OpenClaw does **not** natively support `agents.mcp.servers` config yet. The feature was requested in issue #4834 and is listed as "High priority." No `mcp` key exists in the current config schema.

### Working Integration Option 1: mcporter via npx ⭐ RECOMMENDED

`mcporter` v0.7.3 is available via `npx` and can spawn the scrapling MCP server as a stdio subprocess:

```bash
npx mcporter call --stdio "scrapling mcp" get url=https://example.com extraction_type=text
```

**Output:**
```json
{
  "status": 200,
  "content": ["Example Domain\nThis domain is for use in documentation examples..."],
  "url": "https://example.com/"
}
```

**Moto can use this today** via the `exec` tool. The JSON output is clean and structured.

**Bulk fetch example:**
```bash
npx mcporter call --stdio "scrapling mcp" bulk_get urls='["https://example.com","https://example.org"]' extraction_type=markdown
```

**Stealthy fetch (Cloudflare bypass):**
```bash
npx mcporter call --stdio "scrapling mcp" stealthy_fetch url=https://target.com solve_cloudflare=true extraction_type=text
```

> Note: `npx mcporter` has a cold-start overhead (spawns node + MCP server per call). Acceptable for occasional use.

### Working Integration Option 2: Scrapling CLI Extract Command

```bash
scrapling extract get 'https://example.com' /tmp/output.md
scrapling extract fetch 'https://example.com' /tmp/output.md  # browser
scrapling extract stealthy-fetch 'https://example.com' /tmp/output.html --solve-cloudflare
```

Then Moto reads the output file. Slightly less elegant (two steps), but dead simple.

**With CSS selector:**
```bash
scrapling extract get 'https://news.ycombinator.com' /tmp/hn.md --css-selector '.athing .titleline'
```

### Future Integration: Native OpenClaw MCP Config

When openclaw adds native MCP support (issue #4834), the `~/.openclaw/openclaw.json` config will look like:

```json
{
  "agents": {
    "list": [
      {
        "id": "main",
        "mcp": {
          "servers": [
            {
              "name": "scrapling",
              "command": "/home/jlwestsr/.local/bin/scrapling",
              "args": ["mcp"]
            }
          ]
        }
      }
    ]
  }
}
```

This will expose all 6 scrapling tools natively to Moto as first-class tools (alongside web_search, exec, etc.).

### Future Integration: Persistent HTTP Service

For high-frequency usage, run scrapling as a background service:

```bash
# Start service (add to systemd or openclaw cron)
scrapling mcp --http --host 127.0.0.1 --port 8765
```

Create a startup entry in OpenClaw or systemd for auto-start. Then use `mcporter` or a custom HTTP client skill to call it.

---

## Gotchas & Known Issues

1. **Ubuntu 24.04 externally-managed Python** — Must use `--break-system-packages --user` or a venv. Don't use system-wide `pip install` without `--user`.

2. **Browser system deps missing** — `scrapling install` fails without root. The browser binaries themselves are installed. If you get errors with `fetch`/`stealthy_fetch` about missing libs, run:
   ```bash
   sudo python3 -m playwright install-deps chromium
   ```

3. **HTTP transport needs SSE-aware client** — Direct `curl` or `requests` won't work with `--http` mode. Use mcporter or an official MCP client library.

4. **mcporter cold-start** — Each `npx mcporter call --stdio "scrapling mcp"` spawns a new Node process + Python process. Budget ~2-3 seconds overhead per call on first run (faster on subsequent due to npx cache).

5. **OpenClaw MCP is a feature request, not shipped** — Don't modify `openclaw.json` with `agents.list.mcp` yet; it won't be read. Use mcporter bridge in the meantime.

6. **`stealthy_fetch` / `bulk_stealthy_fetch` are slow** — They launch a full stealth browser. Budget 10-30 seconds per page. Only use when you need Cloudflare bypass.

7. **PATH note** — The `scrapling` binary is at `/home/jlwestsr/.local/bin/scrapling`. This is in PATH. Subagents spawned by OpenClaw inherit this PATH correctly.

---

## Recommendation: Is This Worth Integrating? YES ✅

Scrapling MCP gives Moto genuinely powerful web scraping capabilities that go well beyond the current `web_fetch` tool:

| Capability | web_fetch (current) | scrapling MCP |
|------------|---------------------|---------------|
| Basic HTTP fetch | ✅ | ✅ |
| TLS fingerprint spoofing | ❌ | ✅ |
| JS-rendered pages | ❌ | ✅ (`fetch`) |
| Cloudflare bypass | ❌ | ✅ (`stealthy_fetch`) |
| CSS selector targeting | ❌ | ✅ |
| Parallel/bulk URLs | ❌ | ✅ (bulk_* tools) |
| Markdown extraction | ✅ (readability) | ✅ (markdownify) |
| Anti-bot headers | ❌ | ✅ |

**Immediate action:** Moto can start using scrapling **today** via:
```bash
npx mcporter call --stdio "scrapling mcp" get url=<URL> extraction_type=markdown
```

**Next milestone:** When OpenClaw ships native MCP support, add the `agents.list.mcp.servers` config entry to make it a first-class tool.

---

## Quick Reference Card

```bash
# Simple HTTP fetch (Markdown)
npx mcporter call --stdio "scrapling mcp" get url=https://example.com

# Simple HTTP fetch (text only)
npx mcporter call --stdio "scrapling mcp" get url=https://example.com extraction_type=text

# Browser fetch (JS-rendered pages)
npx mcporter call --stdio "scrapling mcp" fetch url=https://example.com

# Stealthy fetch (Cloudflare, high protection)
npx mcporter call --stdio "scrapling mcp" stealthy_fetch url=https://example.com solve_cloudflare=true

# Bulk fetch (multiple URLs)
npx mcporter call --stdio "scrapling mcp" bulk_get urls='["https://url1.com","https://url2.com"]'

# CLI alternative (saves to file)
scrapling extract get 'https://example.com' /tmp/out.md
```
