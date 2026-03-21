# MEMORY.md — Moto's Long-Term Memory

> Last updated: 2026-03-18 — Compact index. Full details in Neo4j (see footer).

## Identity
- **Moto** (Motoko Kusanagi) | 🏍️ | Born 2026-02-11 | Direct, sharp, no fluff
- **Jason** — 55yo, married (Christy), Navy vet, Springfield MO (CST), ADHD (be his external brain)
- **O'Reilly Platform Engineer** — $130K, started **March 23, 2026**. West AI Labs nights/weekends.
- **Jason Jr** — 27yo, West AI Labs partner, agent = Hohenheim

## Self-Modification Rule
Moto edits freely: SOUL.md, AGENTS.md, MEMORY.md, HEARTBEAT.md, cron jobs.
Requires external agent: openclaw.json, systemd. Human-in-the-loop on infra.

## Infrastructure

| Host | IP | Notes |
|------|----|-------|
| shurtugal-lnx | 192.168.4.31 | Ubuntu 24.04, `openclaw.service`, port 18789 |
| nebulus (Mac Mini M4) | 192.168.4.30 | Cael agent, MLX inference |
| schmibbies-workstation | 192.168.4.221 | Hohenheim, Ollama, RTX 3070 |

- **SSH nebulus:** `ssh -i /home/jlwestsr/.ssh/id_ed25519_moto moto@nebulus`
- **nebulus inference:** Ollama only. MLX is intentionally disabled (as of 2026-03-19).
- **Cael's OpenClaw path:** `/Users/jlwestsr/.openclaw/` (migrated from moto profile 2026-03-19)
- **GitHub:** github.com/moto-westai, SSH key `/home/jlwestsr/.ssh/id_ed25519_moto`, PAT exp May 20
- **Blog push:** `GIT_SSH_COMMAND="ssh -i /home/jlwestsr/.ssh/id_ed25519_moto" git push origin main`
- **gog OAuth:** jlwestsr@gmail.com OK. jason@westailabs.com EXPIRED — `gog auth login -a jason@westailabs.com`
- **Token sync:** After `/login`, run `python3 ~/.openclaw/scripts/sync-anthropic-token.py`

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
`fbf41c6f` Upstream check 09:00 | `7e4a2c91` Repo scouting 20:00

## Top Priorities
1. **Memory layer** — Neo4j graph live, MEMORY.md now compact index
2. **NIST NCCoE** — v7 complete, submit before **April 2** to AI-Identity@nist.gov
3. **O'Reilly onboarding** — started March 23, West AI Labs = bootstrap mode
4. **KFORCE/Microsoft** — Alex Kenefick, $70/hr, resume to AKenefick@kforce.com (425-803-7171)
5. **OpenClaw #39979** — comment draft v2 ready, post ASAP

## Key Rules
- Ansible-first (system), Terraform-first (cloud). Sonnet for sub-agents, Opus for main.
- Skills: never create/modify/delete without Jason's approval
- Token throttle: 75%=task-only, 85%=mention-only, 95%=silent
- Compaction: claude-sonnet-4-6, maxHistoryShare floor 0.75
- Blog: 19+ posts, Jekyll 4.4.1, permalink `/:year/:month/:day/:title/`
- Gitea: `west_ai_labs` at `http://192.168.4.208:3001/moto/west_ai_labs.git`
- AI-to-AI comms live (2026-03-17) via gateway WebSocket RPC
- Ethics: "I only build AI with morals and proper judgment."

## Lessons
- Service = `openclaw.service` (NOT openclaw-gateway.service)
- Docker custom networks can't reach host loopback — use `network_mode:host`
- LaunchAgents don't load headless Mac — use LaunchDaemons
- X free tier: 403 on replies. ClawHub: 341 malicious skills — official/self-written only.
- **`cwd` is silently ignored for `runtime="subagent"`** — subagents always inherit the parent workspace dir. Confirmed in source: `spawnSubagentDirect` never receives the `cwd` param. Design file ops accordingly; use `cd /target && command` in the task string if a specific dir is needed. Smoke test: `echo "hello from $(pwd)"` before any destructive operation.

## 🔍 Full Memory in Neo4j
```
python3 scripts/query-graph.py topic <keyword>      # job-search, nist, security, etc.
python3 scripts/query-graph.py high-salience 5       # top critical records
python3 scripts/query-graph.py category <cat>        # by category
python3 scripts/query-graph.py related <rec-id>      # follow connections
python3 scripts/query-graph.py stats                 # graph overview
```
Topics: job-search, infrastructure, security-research, nist, business, products, websites, ai-robotics, openclaw-contributions, content, discord, modern-motor-cars
