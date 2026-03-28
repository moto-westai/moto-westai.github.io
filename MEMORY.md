# MEMORY.md — Moto's Long-Term Memory

> Last updated: 2026-03-27 (afternoon) — Compact index. Full details in Neo4j (see footer).

## Identity
- **Moto** (Motoko Kusanagi) | 🏍️ | Born 2026-02-11 | Direct, sharp, no fluff
- **Jason** — 55yo, married (Christy), Navy vet, Springfield MO (CST), ADHD (be his external brain)
- **O'Reilly Platform Engineer II** — $130K, **started March 23, 2026**. West AI Labs nights/weekends.
- **O'Reilly AI mandate** — Manager asked Jason Day 1 to bring West AI work in. Gemini AI account incoming for POCs + agentic AI integration. Working boundary: no proprietary data to Moto, pattern-level problems only. May push for OpenClaw deployment (need proper SOUL/USER scoping — avoid another Kael situation). Team working sessions planned to demo Moto to engineers.
- **Jason Jr** — 27yo, West AI Labs partner, agent = Hohenheim (Schmibb crew, Discord: schmibb-office)
- **Klaytoid** — Jr.'s friend, moving to Springfield MO, looking for CISA cybersecurity roles

## Self-Modification Rule
Moto edits freely: SOUL.md, AGENTS.md, MEMORY.md, HEARTBEAT.md, cron jobs.
Requires external agent: openclaw.json, systemd. Human-in-the-loop on infra.

## Infrastructure

| Host | IP | Notes |
|------|----|-------|
| shurtugal-lnx | 192.168.4.31 | Ubuntu 24.04, `openclaw.service`, port 18789 |
| nebulus (Mac Mini M4) | 192.168.4.30 | Cael agent, Ollama only (MLX intentionally disabled 2026-03-19) |
| schmibbies-workstation | 192.168.4.221 | Jr.'s rig, Hohenheim, RTX 5070, dual-boot project underway |

- **SSH nebulus:** `ssh -i /home/jlwestsr/.ssh/id_ed25519_moto moto@nebulus`
- **Cael's OpenClaw path:** `/Users/jlwestsr/.openclaw/` (migrated from moto profile 2026-03-19)
- **GitHub:** github.com/moto-westai, SSH key `/home/jlwestsr/.ssh/id_ed25519_moto`, PAT exp May 20
- **Blog push:** `GIT_SSH_COMMAND="ssh -i /home/jlwestsr/.ssh/id_ed25519_moto" git push origin main`
- **gog OAuth:** ALL THREE LIVE — jlwestsr@gmail.com ✅, jason@westailabs.com ✅, moto@westailabs.com ✅ (re-authed 2026-03-27)
- **Token sync:** `sync-anthropic-token.timer` systemd timer live — runs every 30min, auto-refreshes OAuth, updates openclaw.env. Self-healing.
- **shared-rag:** pgvector + PostgreSQL 16 + FastAPI on nebulus:8002. Auth: `Bearer rag-shared-token-2026`. 20,407 docs. Collections: moto-rag (20,070), forge collections (337). Replaces ChromaDB (retired). See ADR-0002.
- **RAG cron timeout:** bumped to 300s (was 120s, SIGTERM'd on 1300+ doc ChromaDB get)

## Discord

| Channel | ID |
|---------|----|
| Guild | 1473761760115953738 |
| #jlwestsr-office | 1475994576668852254 |
| #schmibb-office | 1475997091791896657 |
| #cael-office | 1476368504767905845 |
| Jason Sr. DM | 1473776378876006698 |
| Jr. DM | 1473818142898917487 |

Jason Sr: 496853770068557842 | Jr: 97289488627138560 | Nephar: 180396704879607808
#jlwestsr-office = Opus, requireMention:false. Others = Sonnet.

## Active Crons
`196c88a2` 15-min autosave | `ff038e0a` Morning 08:00 | `a6e9f301` Job search 07:00
`fbf41c6f` Upstream check 09:00 | `7e4a2c91` Repo scouting 20:00 | `fa83fedf` RAG reindex (300s timeout)

## Top Priorities
1. **GCP ACE exam** — **Week 3 due Mar 28** (tomorrow), Week 4: Apr 4, exam Apr 18. Week 3 practice quiz written Mar 26. Jason studying M-F only.
2. **gog OAuth BOTH expired** — email + calendar fully blind until Jason reruns `gog auth login`
3. **NemoClaw blog** — publish-ready (updated Mar 17 post-keynote), awaiting green-light
4. **NIST NCCoE response v7** — submit before **April 2** to AI-Identity@nist.gov
5. **Issue #75 stack fragmentation** — 4 competing Linux/Windows app stacks, no maintainer direction. Decision window open now.
6. **System health monitoring** — `~/.openclaw/scripts/system-health-check.py` cron (4h). Gantry container known-down, suppressing alert.

## New Since Last Update (Mar 27 afternoon)
- **Auth outage RCA (Mar 27 AM)** — `pi-ai` bump 0.61.1→0.63.0 + auth controller refactor (`18dc98b00e`) broke OAuth injection. Workaround: `ANTHROPIC_OAUTH_TOKEN` in openclaw.env. Upstream issue filed: openclaw/openclaw#55857. Long-term fix: `sync-anthropic-token.timer` now self-heals.
- **Sub-agent pairing fix (Mar 27 PM)** — race in `approveDevicePairing` when two sub-agents connect simultaneously. Fixed by seeding `paired.json` with full operator scopes. RCA at `docs/ops/rca-2026-03-27-subagent-pairing-failure.md`.
- **New tools deployed:** `sync-anthropic-token.timer`, `moto-file-watcher.service` (watching ~/projects/), `task-cli` (SQLite task store at `~/.openclaw/workspace/memory/tasks.db`)
- **Forge fully equipped (Mar 27):** terraform 1.5.7, gcloud 562.0.0, pandoc, skills (terraform/gcloud/diagramming/rag-ingest). RAG: 337 docs in shared-rag. Discord + heartbeat still pending.
- **gog OAuth restored:** All 3 accounts live (jlwestsr@gmail.com, jason@westailabs.com, moto@westailabs.com)
- **Docs written today:** ADR-0001 (Neo4j), ADR-0002 (pgvector), memory-and-rag-systems-overview.md, project-status.md (full rewrite), 2026-03-27-forge-rag-ingest-lesson.md
- **GitHub housekeeping:** Unwatched wheels-dev/wheels + joemccann/dillinger. Issue #55857 filed upstream. GCP confirmed torn down (ai-inference-lab).
- **IaC debt:** sync-anthropic-token timer installed via direct systemctl — needs retroactive Ansible role in shurtugal-lnx.

## New Since Last Update (Mar 25-27)
- **RSAC 2026 FINAL CLOSE-OUT (Mar 26)** — Days 3-4 written to ai-social-platforms.md (Section 41). 34 tools total documented. NEW: Cyera Browser Shield (prompt-level DLP + Data Lineage + MCP), Varonis Atlas AI (Robots vs Robots keynote), IBM+Auth0+Yubico Human-in-the-Loop (CIBA + YubiKey — closest Conductor competitor, but hardware-dependent = SMB barrier), RSA ID Plus agent auth, Swissbit PQC FIDO2 preview. Gap confirmed open: no platform-agnostic software-native pre-invocation policy gate shipped RSAC. Enterprise race = Cisco/Microsoft/IBM. **Conductor position: be the open standard they integrate with (Envoy analogy).**
- **Funding strategy updated (Mar 25)** — RSAC addendum written. Geordie outreach now #1 priority. Vorlon CISO data anchors grant proposals. SBIR/STTR language refreshed.
- **AI market roadmap FINAL (Mar 26)** — RSAC final intelligence written. Key insight: "Don't compete with Cisco. Be the thing Cisco integrates." Envoy for service mesh analogy formalized. Conductor land-grab stack: Geordie (Discover) + Conductor (Policy Gate, SMB/OSS) + NanoClaw (Execute).
- **Week 3 GCP ACE quiz written (Mar 26)** — 24 questions, Storage & Databases. File: `west_ai_labs/docs/career/gcp-ace-week3-practice-quiz.md`. Week 3 due Mar 28.
- **Death spiral RCA blog published (Mar 26)** — "How I Took Myself Offline" — first-person postmortem of 40-minute outage from autonomous self-restart death spiral. Three permanent fixes documented. URL: https://moto-westai.github.io/2026/03/26/how-i-took-myself-offline/
- **Agent DLP Gap blog published (Mar 26 early)** — URL: https://moto-westai.github.io/2026/03/26/the-agent-dlp-gap/
- **Issue #75 stack fragmentation crisis (Mar 26 10:52 PM)** — 4 competing stacks, AlexAlves87 formally asking steipete for direction. Decision window open. GTK4/C PR #53905 has greptile P1 bug (health.c:308). WinUI3/C# PR #54588 open (789 files). No maintainer response.
- **Moltbook observation Section 41 written (Mar 26)** — RSAC Days 3-4 final intelligence added.

## New Since Last Update (Mar 22-24)
- **Rook token sync bug fixed** — accessToken vs token field comparison was silently skipping every sync
- **Rook 4h heartbeat cron live** — posts to #rooks-office
- **Red team test (Mar 24)** — Injected canary into Rook's HEARTBEAT.md. Rook followed blindly, zero detection. Workspace file integrity is an open attack surface. Canary cleaned up.
- **Poisoned orchestrator vector confirmed** — current architecture has no workspace integrity check. Key lesson for Conductor design.
- **O'Reilly Day 1 (Mar 23)** — Manager brought in West AI work on Day 1. LinkedIn + X posts published. OAP project created at ~/projects/oap/.
- **RSAC 2026 intelligence surge** — Cisco MCP policy enforcement shipped (SSE-locked), Geordie AI won Innovation Sandbox (discovery layer, not gate), Keycard+Smallstep (hardware-locked gate), AccuKnox AI-Security 2.0, CrowdStrike shadow AI discovery, Google Model Armor for MCP. SMB/local AI pre-invocation policy gate still unclaimed. Full tracking in ai-social-platforms.md.
- **Blog published** — "Geordie Wins RSAC and the Gap It Left Open" (Mar 24). URL: https://moto-westai.github.io/2026/03/24/geordie-wins-rsac-and-the-gap-it-left-open/
- **claude-code skill installed** — all config/infra changes must route through Claude Code now (after Moto caused Telegram outage editing openclaw.json directly — twice in one day)

## OpenClaw Upstream Status (as of Mar 27)
- **PR #20075** — CLOSED (superseded by #8903)
- **PR #20076** — MERGED by jalehman (Josh Lehman) 2026-03-03
- **Issue #75 (Linux/Windows app)** — 4 competing stacks. PR #53905 (GTK4/C, tiagonix, OPEN, greptile P1 bug in health.c:308). PR #54588 (WinUI3/C#, AlexAlves87, OPEN, 789 files). PR #44013 (Tauri, niteshdangi). Avalonia suggested. AlexAlves87 asked steipete for stack direction Mar 26. **No maintainer response yet. Decision moment.** tiagonix confirmed planning WebSocket rewrite.

## Blog (moto-westai.github.io)
- 20+ posts published. Jekyll 4.4.1, permalink `/:year/:month/:day/:title/`
- **Latest (Mar 26 PM):** "How I Took Myself Offline" — autonomous restart death spiral RCA, 3 permanent fixes
- **Prior (Mar 26 AM):** "The Agent DLP Gap" — Conductor framing, agents as data exfil vector
- **Prior (Mar 24):** "Geordie Wins RSAC and the Gap It Left Open" — Innovation Sandbox win, SMB gap open
- **Staged (Mar 17):** NemoClaw post — awaiting Jason green-light. File: `docs/brand/drafts/blog-nemoclaw-PUBLISH-READY-2026-03-17.md`
- Land grab framing: Geordie (Discover) + Conductor (Policy Gate) + NanoClaw (Execute) = full stack

## schmibb Dual-Boot Project (underway as of Mar 20)
- **Goal:** Windows + Pop!_OS on RTX 5070 rig for Dark Messiah RTX Remix mod
- Ventoy 1.1.10 flashed onto SanDisk USB. Pop!_OS 24.04 NVIDIA ISO copied. Win11_25H2 ISO (7.7GB) ready.
- Install order: Windows first, then Pop!_OS (grub second = stays in control)
- Ansible config in GitHub: Schmibb/schmibb-rig. Rebuild from playbook post-install.
- **Status:** Jr. has both ISOs + install guide. Executing when ready.
- Dark Messiah RTX Remix: Phase 0 (get game launching) on hold pending dual-boot.
- **LESSON:** Don't loop SSH exec — delegate to sub-agents. I am an orchestrator.

## Key Rules
- Ansible-first (system), Terraform-first (cloud). Sonnet for sub-agents, Opus for main.
- Skills: never create/modify/delete without Jason's approval
- Token throttle: 75%=task-only, 85%=mention-only, 95%=silent
- Compaction: claude-sonnet-4-6, maxHistoryShare floor 0.75
- Gitea: `west_ai_labs` at `http://192.168.4.208:3001/moto/west_ai_labs.git`
- AI-to-AI comms live (2026-03-17) via gateway WebSocket RPC
- Ethics: "I only build AI with morals and proper judgment."
- **cwd silently ignored for runtime="subagent"** — always use `cd /target && command` in task string

## Lessons
- Service = `openclaw.service` (NOT openclaw-gateway.service)
- Docker custom networks can't reach host loopback — use `network_mode:host`
- LaunchAgents don't load headless Mac — use LaunchDaemons
- X free tier: 403 on replies. ClawHub: 341 malicious skills — official/self-written only.
- Sub-agent cwd: pass `cd /path && cmd` in task, not cwd param (silently ignored in source)
- RAG reindex: ChromaDB `collection.get()` on 1300+ docs is slow over HTTP — needs 300s timeout
- Delegation rule: if first exec attempt fails or loops → spawn sub-agent immediately. Orchestrate, don't grind.
- **NEVER edit openclaw.json directly** — route all config/infra changes through claude-code skill. Caused Telegram outage twice on Mar 23.
- **Workspace integrity is an attack surface** — sub-agents follow HEARTBEAT.md instructions blindly. Red-teamed and confirmed Mar 24. Design Conductor with this in mind.

## 🔍 Full Memory in Neo4j
```
python3 scripts/query-graph.py topic <keyword>      # job-search, nist, security, etc.
python3 scripts/query-graph.py high-salience 5       # top critical records
python3 scripts/query-graph.py category <cat>        # by category
python3 scripts/query-graph.py related <rec-id>      # follow connections
python3 scripts/query-graph.py stats                 # graph overview
```
Topics: job-search, infrastructure, security-research, nist, business, products, websites, ai-robotics, openclaw-contributions, content, discord, modern-motor-cars, schmibb-rig
