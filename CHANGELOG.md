# CHANGELOG — Moto's Change Log

> Tracks material changes to infrastructure, config, cron, fork code, and workspace structure.
> **Review cadence:** Jason scans at will. High-risk changes flagged in Discord before applying.
> **Scope:** Cron jobs · Gateway config · Fork source · System files · Workspace structure

---

## 2026-02-26 — Nebulus (Cael) OpenClaw Update

`[2026-02-26] chore(nebulus): sync Cael openclaw-fork to upstream, fix bind loopback, rebuild`

**What:** Controlled update of Cael's OpenClaw on nebulus (Mac Mini M4 Pro).
**Changes applied:** bind `lan→loopback`, added upstream remote, built fresh dist, restarted gateway.
**Rebase status:** Conflicted on local tool-truncation commit (upstream diverged in 2295 commits) — aborted, left on local main. Needs manual conflict resolution.
**Result:** Gateway running (PID 44807), port 18790 listening on loopback, Discord+Telegram connected, MLX OK.

---

## 2026-02-25 — Jr. Resume Final (2-Page Compact)

**What:** Reformatted Jason L. West Jr.'s resume HTML to fit on exactly 2 printed pages (front and back of one sheet).

**Changes:**
- Added `@page { size: letter; margin: 0.4in; }` for print layout control
- Reduced base font to 9.5pt, line-height to 1.2
- Tightened all section margins/padding (~50% reduction)
- References section converted to single horizontal row (flex layout)
- All content preserved — no text deletions

**Output files:**
- HTML: `/home/jlwestsr/projects/west_ai_labs/docs/career/jr-resume-final.html`
- PDF:  `/home/jlwestsr/projects/west_ai_labs/docs/career/jr-resume-final.pdf`
- Media: `/home/jlwestsr/.openclaw/media/jr-resume-final.pdf`
- Page count: **2 pages** (letter, confirmed via pdfinfo)

---

## 2026-02-25 — Jr. Resume Updated

**What:** Updated Jason L. West Jr.'s resume with new West AI Labs AI Engineer role, Skills section, and revised Summary.

**Changes:**
- Added AI Engineer role at West AI Labs LLC (Jan 2026 – Present) to top of Experience section
- Added Skills section (Technical + Professional) after Summary
- Updated Summary to reflect AI Engineering work
- Removed stale file path footer

**Output files:**
- HTML: `/home/jlwestsr/projects/west_ai_labs/docs/career/jr-resume-updated.html`
- PDF:  `/home/jlwestsr/projects/west_ai_labs/docs/career/jr-resume-updated.pdf`

---
> **Not tracked:** Daily notes, session state, routine memory writes

---

## Format
```
### [YYYY-MM-DD] Category: Short description
- **What:** What was changed
- **Why:** Reason / problem solved
- **Files:** Paths affected
- **Risk:** Low / Medium / High / Destructive
- **Reversible:** Yes / No / How
- **Status:** ✅ Applied | ⏳ Pending | ❌ Rolled back
```

---

## 2026-02-21 (Saturday)

### [2026-02-21] Fix: Cron delivery targets — 3 jobs
- **What:** Changed `delivery.to` on Morning Report, Daily Job Search, and upstream-openclaw-check crons from `"Jason"` → `"8544470435"` (Jason's Telegram chat ID). Job Search also had malformed `"telegram:8544470435"` prefix.
- **Why:** All three crons were silently failing to deliver to Telegram. Delivery was routing to unknown/null target.
- **Files:** `/home/jlwestsr/.openclaw/cron/jobs.json`
- **Risk:** Low — delivery config only, no logic changes
- **Reversible:** Yes — revert `delivery.to` to `"Jason"`
- **Status:** ✅ Applied, verified working

### [2026-02-21] Fix: Reset consecutiveErrors on fixed crons
- **What:** Reset `state.consecutiveErrors` to `0` on all three fixed cron jobs
- **Why:** Error counter was inflated from failed deliveries; would have triggered backoff/disable logic
- **Files:** `/home/jlwestsr/.openclaw/cron/jobs.json`
- **Risk:** Low
- **Reversible:** N/A (counter resets naturally)
- **Status:** ✅ Applied

### [2026-02-21] New: Mac Mini Telegram cutover
- **What:** Switched Telegram delivery from shurtugal-lnx gateway (port 18789) to Mac Mini gateway (port 18790). Shurtugal now Discord-only.
- **Why:** Jason's sibling AI experiment — fresh identity on Mac Mini, Telegram as its channel
- **Files:** Gateway config on both machines
- **Risk:** Medium — Telegram routing changed for Jason's primary private channel
- **Reversible:** Yes — reverse gateway Telegram binding
- **Status:** ✅ Applied

### [2026-02-21] Destructive: Mac Mini workspace wipe
- **What:** Wiped entire workspace on Mac Mini (`moto@nebulus`), replaced with blank seed files (SOUL.md, USER.md, AGENTS.md)
- **Why:** Jason's sibling AI experiment — blank identity, no Moto history
- **Files:** `/home/moto/.openclaw/workspace/` on nebulus (wiped)
- **Risk:** **Destructive** — intentional, Jason approved
- **Reversible:** No — old workspace not backed up (was a copy of shurtugal workspace anyway)
- **Status:** ✅ Applied

### [2026-02-21] Config: Mac Mini dmPolicy set to pairing
- **What:** Set `dmPolicy=pairing` on Mac Mini OpenClaw config (Telegram)
- **Why:** Telegram DM allowlist key was invalid; pairing mode allows Jason's chat ID through
- **Files:** Mac Mini gateway config
- **Risk:** Low
- **Reversible:** Yes
- **Status:** ✅ Applied

### [2026-02-21] New: CHANGELOG.md — change tracking system
- **What:** Created this file. Tracks all material infrastructure/config/code changes for Jason's review.
- **Why:** Jason requested formal change control so he can audit what Moto has done
- **Files:** `/home/jlwestsr/.openclaw/workspace/CHANGELOG.md`
- **Risk:** None (new file, no functional change)
- **Reversible:** N/A
- **Status:** ✅ Applied

### [2026-02-21] New: WORKFLOW_AUTO.md — autonomous workflow reference
- **What:** Created post-compaction reference file expected by OpenClaw's audit system
- **Why:** `post-compaction-audit.ts` lists `WORKFLOW_AUTO.md` as a required startup file. Its absence triggered a warning after every compaction.
- **Files:** `/home/jlwestsr/.openclaw/workspace/WORKFLOW_AUTO.md`
- **Risk:** None (new file)
- **Reversible:** Yes — delete file (will re-trigger compaction audit warnings)
- **Status:** ✅ Applied

### [2026-02-21] Discovery: WORKFLOW_AUTO.md missing from workspace
- **What:** OpenClaw's `post-compaction-audit.ts` expects `WORKFLOW_AUTO.md` in workspace as a required startup file. File does not exist → audit warning fires after every compaction.
- **Why:** Was flagged as suspected prompt injection; traced to legitimate OpenClaw source code.
- **Files:** `openclaw-fork/src/auto-reply/reply/post-compaction-audit.ts` (DEFAULT_REQUIRED_READS)
- **Risk:** N/A (discovery, no change yet)
- **Reversible:** N/A
- **Status:** ✅ Applied — created `WORKFLOW_AUTO.md` as post-compaction reference file (2026-02-21 17:55)

---

## 2026-02-20 (Friday)

### [2026-02-20] New: context-autosave-15m cron (id: 196c88a2)
- **What:** Created 15-minute autosave cron — fires systemEvent to main session to dump context to daily log + session-state.json
- **Why:** Prevent context loss on compaction; ensure memory files stay current
- **Files:** `/home/jlwestsr/.openclaw/cron/jobs.json`
- **Risk:** Low
- **Reversible:** Yes — disable or delete cron
- **Status:** ✅ Applied, running

### [2026-02-20] New: O'Reilly interview reminder crons (×2)
- **What:** Created `oreilly-interview-prep-daily` (daily 14:00 UTC) and `oreilly-interview-morning-of` (one-shot 2026-02-23 13:30 UTC, deleteAfterRun)
- **Why:** Jason's O'Reilly interview Mon 2/23 9:30 AM CST
- **Files:** `/home/jlwestsr/.openclaw/cron/jobs.json`
- **Risk:** Low
- **Reversible:** Yes — disable crons
- **Status:** ✅ Applied

---

## 2026-02-19 (Thursday)

### [2026-02-19] Fix: maxHistoryShare bumped 0.6 → 0.75
- **What:** Raised `maxHistoryShare` in OpenClaw config from 0.6 to 0.75
- **Why:** 0.6 caused compaction loop — workspace files (~28KB) reload after compaction and immediately re-trigger at 60%. 5 back-to-back compactions on 2/19 night.
- **Files:** OpenClaw gateway config
- **Risk:** Low — prevents runaway compaction loops
- **Reversible:** Yes — revert to 0.6 (not recommended)
- **Status:** ✅ Applied, stable

---

## 2026-02-18 (Wednesday)

### [2026-02-18] New: Discord bot configured and paired
- **What:** Discord bot (Moto, App ID 1473764695717445785) added to West AI Labs server. Bot token stored at `~/.openclaw/secrets/discord.env`.
- **Why:** Discord as shared channel for Jr, Mitso, Nephar + Jason
- **Files:** `~/.openclaw/secrets/discord.env`, gateway Discord config
- **Risk:** Low
- **Reversible:** Yes — revoke bot token
- **Status:** ✅ Applied, running

---

## 2026-02-16 (Monday)

### [2026-02-16] Migration: OpenClaw container → bare metal (shurtugal-lnx)
- **What:** Migrated OpenClaw from Docker container to bare metal on shurtugal-lnx (Ubuntu 24.04), running from `openclaw-fork/dist/index.js` directly. Port 18789.
- **Why:** Container had limitations; bare metal gives full access and better performance
- **Files:** `/home/jlwestsr/.openclaw/`, systemd/launch config
- **Risk:** **High** — production migration
- **Reversible:** Yes — backup at `~/openclaw-backup-20260216-091804.tar.gz`
- **Status:** ✅ Applied, stable

---

_Updated by Moto. Last entry: 2026-02-24._

### [2026-02-21] New: Daily GitHub Repo Scouting cron (id: 7e4a2c91)
- **What:** Daily cron at 8 PM CST — searches GitHub for repos relevant to West AI Labs interests (agent orchestration, local inference, multi-agent, AI security, memory/context). Delivers 3-5 picks to Telegram. Skips already-seen repos tracked in memory/github-scout-seen.json
- **Why:** Jason's request — daily automated awareness of relevant open source activity
- **Files:** `/home/jlwestsr/.openclaw/cron/jobs.json`, `memory/github-scout-seen.json`
- **Risk:** Low — read-only GitHub searches, Telegram delivery
- **Reversible:** Yes — disable cron
- **Status:** ✅ Applied, first run tonight at 8 PM CST

---

## 2026-02-24 (Tuesday)

### [2026-02-24] Fork Sync: OpenClaw upstream — 280 commits
- **What:** Rebased 7 local Moto commits onto upstream/main. 280 new upstream commits pulled in (since Feb 23 sync). Backup branch created before sync.
- **Why:** Upstream pushed a major security hardening wave (exec allowlist, SSRF, prototype pollution, regex DoS, HTML injection, allowFrom ID-only default). Critical to stay current.
- **Conflict:** 1 conflict — `pnpm-lock.yaml` on `chore: upstream sync and build fix`. Resolved by taking upstream's lockfile (local version was stale from yesterday's sync). No ambiguity.
- **Build:** `npm install && npm run build` — succeeded cleanly, exit 0.
- **Commits preserved (in order):**
  1. `feat(compaction): improve merge summary instructions`
  2. `feat(tool-truncation): use head+tail strategy`
  3. `docs: add overnight improvements summary`
  4. `feat: add compaction.announce config`
  5. `fix: add compaction start announcement to followup-runner path`
  6. `feat: add compaction.provider and compaction.model config overrides`
  7. `chore: upstream sync and build fix`
- **Push:** Force push complete — `b46ca602a...b69b6dc7b` on `origin/main`
- **Backup branch:** `backup/pre-sync-20260224`
- **Files:** `~/.openclaw/workspace/openclaw-fork/` (all source), `pnpm-lock.yaml`
- **Risk:** Medium — source code change, requires reboot to take effect
- **Reversible:** Yes — `git checkout backup/pre-sync-20260224`
- **Status:** ✅ Applied — awaiting shurtugal-lnx reboot to activate
- **Notable upstream security changes:**
  - `fix(security)`: exec allowlist bypass patched
  - `fix(security)`: browser SSRF hardened
  - `fix(security)`: prototype pollution in account-key handling closed
  - `fix(security)`: allowFrom now ID-only by default (#24907) — breaking change potential
  - `fix(security)`: session export XSS/HTML injection hardened
  - `fix(whatsapp)`: groupAllowFrom sender filter bypass fixed

### [2026-02-24] Fix: Gateway --bind lan → loopback (post-sync crash-loop)
- **What:** Changed `--bind lan` to `--bind loopback` in `/etc/systemd/system/openclaw.service`
- **Why:** Upstream's new Control UI security check requires explicit `allowedOrigins` when gateway binds to LAN. `--bind lan` in the systemd service (which overrides the config file) triggered an immediate crash-loop after the 280-commit sync. Restart counter hit 74+ in minutes.
- **Root cause:** CLI flag in service file silently overrides `openclaw.json` config — both must agree.
- **Fix command:** `sudo sed -i 's/--bind lan/--bind loopback/' /etc/systemd/system/openclaw.service`
- **Files:** `/etc/systemd/system/openclaw.service`
- **Risk:** Low — restores previous working behavior
- **Reversible:** Yes — change back to `--bind lan` and set `allowedOrigins` if LAN binding needed later
- **Status:** ✅ Applied, gateway healthy post-reboot
- **Runbook:** `west_ai_labs/docs/ops/moto-recovery-runbook.md` — new failure mode documented under "Gateway Won't Start"

## 2026-02-25 — Cael MLX model: 32B → 14B
- **What:** Switched Cael's MLX inference model from Qwen2.5-32B-Instruct-4bit to Qwen2.5-14B-Instruct-4bit
- **Why:** 32B causing slow responses (30-60s), frequent hang/OOM crashes on 48GB Mac Mini. 14B is 2-3x faster with sufficient capability for training phase.
- **Files:** start-mlx-server.sh, mlx-keepalive.sh, openclaw.json (all on nebulus)
- **Risk:** Low — same model family, smaller size
- **Reversible:** Yes — revert model path in start-mlx-server.sh and openclaw.json
- **Status:** Applied

## 2026-02-25 — Cael MLX model: 14B → 7B
- **What:** Switched Cael's MLX inference model from Qwen2.5-14B to Qwen2.5-7B-Instruct-4bit
- **Why:** 14B responses taking 2-3 min on Mac Mini M4 Pro 48GB. 7B expected ~15-20s — acceptable for interactive Discord use.
- **Files:** start-mlx-server.sh, mlx-keepalive.sh, openclaw.json (all on nebulus)
- **Risk:** Low — smaller model, faster inference, same family
- **Reversible:** Yes — revert model name in start-mlx-server.sh and openclaw.json
- **Status:** Applied
[2026-02-25] feat(blog): add social share buttons (Twitter/LinkedIn/copy-link) to post layout + cael avatar/banner images to assets
