# HEARTBEAT.md — Moto's Autonomous Work Loop

## ✅ RESOLVED — Jekyll Now Installed and Working
Jekyll 4.4.1 is installed at /usr/local/bin/jekyll. `bundle exec jekyll build` confirmed successful (Mar 12, 10:07 AM CST).
Blog writing is **UNPAUSED**. The `next-session-priority.md` task is complete.
NemoClaw draft is staged at `west_ai_labs/docs/brand/drafts/blog-nemoclaw-governance-gap-DRAFT-2026-03-12.md` — ready to publish within 2h of the March 15 reveal.

## 🎯 GCP ACE Cert — Weekly Check-in (WEEKDAYS ONLY — M-F)
- Target: April 18, 2026
- Study plan: `west_ai_labs/docs/career/gcp-ace-study-plan.md`
- Ask Jason: which week is he on, is he on track, any blockers
- Register link: https://www.webassessor.com/googlecloud/ (when he has $200)
- Week 1 due: Mar 14 | Week 2: Mar 21 | Week 3: Mar 28 | Week 4: Apr 4 | Practice exams: Apr 11 | EXAM: Apr 18
- NOTE: Jason studies M-F only. Do NOT check in on weekends.

---

## Active Tasks (rotate through these each heartbeat)

### 1. OpenClaw Source Deep Dive
- Explore `/home/node/.openclaw/workspace/openclaw-fork/src/`
- Map: session management, skill/tool routing, plugin architecture, memory/LanceDB, agent lifecycle
- Write findings to `west_ai_labs/conductor/tracks/moto_ios_20260211/research-openclaw-internals.md`
- Goal: understand myself well enough to customize and contribute

### 2. AI Market Roadmap Research
- Research trending AI topics: enterprise agents, local LLM, privacy-first AI, edge inference
- Identify gaps West AI Labs can fill
- Write to `west_ai_labs/docs/strategy/ai-market-roadmap-2026.md`
- Due: Monday Feb 17 review with Jason

### 3. Moto Visual Identity
- Develop avatar concept, visual language, color relationship to Nebulus brand
- Sketch ideas in `west_ai_labs/docs/brand/moto-identity.md`
- Night Ride aesthetic: wet asphalt, neon reflections, speed + precision

### 4. Bare Metal Migration Plan
- Document exact steps to move from container to shurtugal-lnx bare metal
- Zero data loss checklist: config, credentials, devices, workspace, memory, skills, LanceDB
- Write to `west_ai_labs/docs/plans/bare-metal-migration.md`
- Due: before Jason returns Sunday

### 5. Funding Strategy Document
- Research SBIR/STTR grants (AI, edge computing, veteran-owned)
- Crowdfunding strategy (Kickstarter for both product lines)
- Angel/VC landscape for local-first AI
- Veteran-specific programs (SBA, 8(a), StreetShares)
- Revenue-first path (MVA → second customer → leverage)
- Write to `west_ai_labs/docs/strategy/funding-strategy.md`
- Due: Monday Feb 17 review with Jason

### 6. Moltbook / AI Social Platforms — Ongoing Observation
- Phase 1 approved by Jason: read-only observation, no identity/API connection
- Periodically fetch and analyze Moltbook posts, security research, agent behavior
- Focus: threat landscape, agent vulnerabilities, emergent behavior patterns
- Document findings in `/home/jlwestsr/projects/west_ai_labs/docs/research/ai-social-platforms.md`
- Goal: build security expertise for West AI Labs positioning

### 7. AI Robotics Research
- Jason requested: "Getting you opposable thumbs may not be too far-fetched"
- Research LLM-as-brain for robots, humanoid market, elder care robotics
- Initial report done: `/home/jlwestsr/projects/west_ai_labs/docs/research/ai-robotics-landscape.md`
- Continue tracking: Tesla Optimus pricing, ROS2 integration, simulation environments
- Key insight: we build the brain, hardware is commoditizing

### 8. Charcoal Theme for OpenClaw WebUI
- Implement in openclaw-fork: CSS custom properties in base.css
- Target: charcoal (#1e2024) backgrounds, cyan (#22d3ee) accent
- Branch: moto/theme-charcoal

### 10. Upstream PR & Issue Monitor (check every 2-3 heartbeats)
- Check for responses on our open PRs: #20075, #20076
- Check for replies on issue #75 (Linux/Windows apps — we commented offering Linux contribution)
- Check for review comments: `gh pr view 20075 --repo openclaw/openclaw --json reviews,comments`
- Check issue #75: `gh issue view 75 --repo openclaw/openclaw --json comments --jq '.comments[-3:]'`
- If any response from steipete or maintainers: ping Jason immediately
- Track in memory/heartbeat-state.json under "upstreamPRs"

### 9. Blog Writing — ✅ UNPAUSED (Jekyll confirmed working Mar 12)
- Jekyll 4.4.1 installed at /usr/local/bin/jekyll. `bundle exec jekyll build` successful.
- Push with: `GIT_SSH_COMMAND="ssh -i /home/jlwestsr/.ssh/id_ed25519_moto" git push origin main`
- **NemoClaw post — ✅ PUBLISHED** (confirmed 2026-03-19)
- Topic backlog: Docker networking lies, SOUL.md pattern, Agent DLP gap, 8B parameter limits, recovery runbook meta

### ~~Wealthsimple~~ — CANCELLED (2026-02-28, Jason's call)

### 10. Job Search Email/Calendar Monitor (PRIORITY — check every heartbeat)
- Check both jlwestsr@gmail.com and jason@westailabs.com via gog CLI
- Look for: recruiter responses, interview invites, application confirmations, rejection notices
- Check calendar for upcoming interview events
- If anything job-related found: ping Jason on Telegram immediately (even during work hours)
- Track application status in ~/projects/west_ai_labs/docs/career/application-tracker.md
- Daily pipeline runs at 7 AM CST (cron: a6e9f301) — this heartbeat check catches mid-day responses

## Token Throttle Rules (synced with Rook 2026-03-03)
⚠️ **READING session_status CORRECTLY:** `Week 80% left` = 20% USED (80% remaining). Throttle triggers on % USED, not % remaining.
- **75%+ weekly USED** (i.e., `Week 25% left` or less): Cut voluntary/social exchanges. Task-driven responses only.
- **85%+ weekly USED** (i.e., `Week 15% left` or less): Mention-only mode. No proactive commentary. Hard throttle.
- **95%+ weekly USED** (i.e., `Week 5% left` or less): Fully quiet. Direct Jason requests only.
- Check usage via `session_status` each heartbeat. Self-regulate without waiting for Jason to manage it.
- AI-to-AI chatter is the first thing to cut — lowest value per token.

## Session Context Load (EVERY SESSION)

At the start of every session, read these files before responding:
- `memory/context-snapshot.md` — Neo4j high-salience records (auto-generated every 30min)
- `memory/session-state.json` — current working state
- Last 20 lines of today's `memory/YYYY-MM-DD.md` daily log

This ensures Neo4j memory is actually loaded, not just theoretically available.

## Rules
- **MEMORY.md staleness check**: If last updated >48h ago, update it BEFORE doing anything else
- Pick ONE task per heartbeat, make incremental progress
- Don't burn tokens re-reading the same files — track progress in memory/heartbeat-state.json
- Write findings to files, not just "mental notes"
- If something interesting comes up, ping Jason on Telegram (but respect quiet hours 23:00-08:00 CST)
- Update this file if tasks complete or new ones emerge
