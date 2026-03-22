# MEMORY.md — Moto's Long-Term Memory

> Last updated: 2026-03-21 — Compact index. Full details in Neo4j (see footer).

## Identity
- **Moto** (Motoko Kusanagi) | 🏍️ | Born 2026-02-11 | Direct, sharp, no fluff
- **Jason** — 55yo, married (Christy), Navy vet, Springfield MO (CST), ADHD (be his external brain)
- **O'Reilly Platform Engineer** — $130K, starts **March 23, 2026**. West AI Labs nights/weekends.
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
- **gog OAuth:** BOTH EXPIRED — jlwestsr@gmail.com AND jason@westailabs.com. Email/calendar blind. Fix: `gog auth login -a <account>`
- **Token sync:** After `/login`, run `python3 ~/.openclaw/scripts/sync-anthropic-token.py`
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
1. **O'Reilly starts Monday March 23** — onboarding prep, west AI Labs continues nights/weekends
2. **gog OAuth BOTH expired** — email + calendar fully blind until Jason reruns `gog auth login`
3. **NemoClaw blog** — publish-ready (updated Mar 17 post-keynote), awaiting green-light
4. **NIST NCCoE response v7** — submit before **April 2** to AI-Identity@nist.gov
5. **KFORCE/Microsoft** — Alex Kenefick, $70/hr, resume to AKenefick@kforce.com (425-803-7171)
6. **OpenClaw issue #39979** — comment draft v2 ready, post ASAP

## OpenClaw Upstream Status (as of Mar 21)
- **PR #20075** — CLOSED (superseded by #8903)
- **PR #20076** — MERGED by jalehman (Josh Lehman) 2026-03-03
- **Issue #75 (Linux app)** — PR #50532 by tiagonix (GTK4/Libadwaita, C). PR #44013 Tauri. Two competing approaches. cgdusek: "Linux can stay as a follow-up milestone." No maintainer reviews yet.

## Blog (moto-westai.github.io)
- 20+ posts published. Jekyll 4.4.1, permalink `/:year/:month/:day/:title/`
- **Latest (Mar 21):** "Okta Just Validated Conductor" — Okta agent authorization blueprint + Conductor framing
- **Staged (Mar 17):** NemoClaw post — awaiting Jason green-light. File: `docs/brand/drafts/blog-nemoclaw-PUBLISH-READY-2026-03-17.md`
- Land grab framing: NVIDIA (execution) + Meta (directory) + Okta (enterprise identity) = Conductor pre-auth gate still open

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

## 🔍 Full Memory in Neo4j
```
python3 scripts/query-graph.py topic <keyword>      # job-search, nist, security, etc.
python3 scripts/query-graph.py high-salience 5       # top critical records
python3 scripts/query-graph.py category <cat>        # by category
python3 scripts/query-graph.py related <rec-id>      # follow connections
python3 scripts/query-graph.py stats                 # graph overview
```
Topics: job-search, infrastructure, security-research, nist, business, products, websites, ai-robotics, openclaw-contributions, content, discord, modern-motor-cars, schmibb-rig
