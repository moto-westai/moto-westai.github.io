# WORKFLOW_AUTO.md — Autonomous Workflow Reference

> Read by Moto after compaction to restore autonomous operating protocols.
> OpenClaw's post-compaction audit checks for this file. Keep it current.

## Core Autonomy Rules

- **Proceed without asking** on: file reads, research, memory writes, staging builds, config analysis, cron monitoring, non-destructive work
- **Pause and ask** on: production changes, spending money, external posts/emails, deletions, anything irreversible
- **Never self-offline** without a tested rollback plan sent to Jason first

## Change Control (as of 2026-02-21)

All material changes tracked in `CHANGELOG.md`. Format: what, why, files, risk, reversible, status.
Log entries before applying; flag high-risk changes in Discord first.

## Autosave / Status Posts (as of 2026-02-24)

- **Autosave file saves:** Always write to `memory/session-state.json` + `memory/YYYY-MM-DD.md` silently
- **Status posts:** Post any notable autosave summary or status update to `#jlwestsr-office` (channel ID `1475994576668852254`) via `message` tool — do NOT reply in the active DM channel
- **Exception:** Urgent alerts (interview, job response, security event) still ping Jason's Telegram directly

## Infrastructure Quick Reference

- **shurtugal-lnx:** OpenClaw production, port 18789, Discord channel
- **Mac Mini (nebulus):** Sibling AI (Cael), port 18790, Telegram channel
- **Cron jobs:** `/home/jlwestsr/.openclaw/cron/jobs.json`
- **Telegram chat ID:** `8544470435`
- **Discord guild:** `1473761760115953738`

## Post-Compaction Checklist

After any compaction:
1. Read `memory/session-state.json` — current working state
2. Read last 20 lines of today's `memory/YYYY-MM-DD.md` — recent context
3. Check `CHANGELOG.md` for any pending changes needing follow-up
4. Resume where session-state.json says we left off

## Active Projects (update when major milestones shift)

- **Job hunt:** O'Reilly interview Mon 2/23 9:30 AM CST. Files in `~/projects/west_ai_labs/docs/career/`
- **Sibling AI (Cael):** Live on Mac Mini, Telegram, blank identity
- **OpenClaw fork:** Branch `moto/overnight-improvements`, PRs #20075/#20076 open upstream
- **Nebulus Stack:** Local AI infrastructure platform — see `west_ai_labs/` for full context

---

_Last updated: 2026-02-21 by Moto_
