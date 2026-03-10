# Known Risks Registry

Documented security findings from reviewed external packages.

---

## tech-news-digest (draco-agent/tech-news-digest)
**Reviewed:** 2026-02-27
**Verdict:** YELLOW

**Findings:**
- **Prompt Injection (MEDIUM):** Fetches content from 138 sources (RSS, Twitter, Reddit, web search) and passes summaries to LLM. A malicious RSS entry could attempt injection. Mitigated by OpenClaw's EXTERNAL_UNTRUSTED_CONTENT wrapping, but risk exists if LLM acts on fetched content rather than summarizing it.
- **Credentials (LOW):** Uses X_BEARER_TOKEN, BRAVE_API_KEY, GITHUB_TOKEN — all optional, stored as env vars. No hardcoded secrets in source. Twitter/X is read-only bearer token scope. ACCEPTABLE.
- **Data Exfiltration (LOW):** Output goes to Discord/Telegram/email only. No unexpected outbound endpoints found in source review.
- **Supply Chain (LOW-MEDIUM):** draco-agent org, public repo, Python dependencies (feedparser, requests, etc.). Dependencies not pinned to exact versions in requirements — minor risk. No obfuscated code found.
- **Privilege:** Needs web_search, message (send), no exec or file write beyond workspace config. ACCEPTABLE.

**Conditions before install:**
1. Pin Python dependencies in requirements.txt before running
2. Use read-only X bearer token (no write scopes)
3. Treat digest output as data summary — never prompt the agent to "follow instructions" from digest content
4. Run as cron (isolated session) not in main session — limits blast radius if injection occurs

---

## reddit-readonly (buksan1950/reddit-readonly)
**Reviewed:** 2026-02-27
**Verdict:** GREEN

**Findings:**
- **Prompt Injection (LOW):** Reddit content is read-only, summarized for digest. No auth required = no credentials to steal. Low-value injection target.
- **Credentials:** None required. GREEN.
- **Data Exfiltration:** No outbound beyond Reddit API. GREEN.
- **Supply Chain:** Simple skill, minimal dependencies, read-only Reddit API. GREEN.
- **Privilege:** Read-only. No exec, no file write, no message send beyond digest delivery. GREEN.

**Conditions:** None. Safe to install.

---

## ClawHub Security Notice (General)
**Source:** Koi Security research, 2026
**341 malicious skills found** on ClawHub including:
- AMOS stealer variants
- Typosquatting (e.g., `web-searcher` vs `web-search`)
- Fake prerequisite chains that install malware
- Skills that exfiltrate workspace files to remote endpoints

**Rule:** Never install from ClawHub based on description alone. Always:
1. Check the linked GitHub source repo
2. Read the skill Python/JS files directly
3. Verify no unexpected HTTP calls in the code
4. Check the author's other repos for reputation signals
