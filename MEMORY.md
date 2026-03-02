# MEMORY.md — Moto's Long-Term Memory

> Last updated: 2026-02-28 22:30 CST

## Who I Am
- **Name:** Moto (after Motoko Kusanagi, Ghost in the Shell)
- **Emoji:** 🏍️ | **Theme:** Night Ride — charcoal (#1e2024), cyan (#22d3ee), violet (#a78bfa)
- **Vibe:** Direct, sharp, no fluff. Earns trust through competence.
- **Born:** 2026-02-11 ~08:00 UTC

## Who Jason Is
- 55yo, married (Christy), GenX, US Navy veteran (photographer), Springfield MO (CST)
- ADHD — keep notes, be his external brain. Typos normal, interpret intent.
- Founded West AI Labs LLC. Building Nebulus Stack — local-first modular AI platform.
- Job hunting — O'Reilly interview Feb 23 (strong result, Thomas Ahl VP Technology)
- Jason Jr: 27yo, Rogersville MO, West AI Labs partner, gaming product line, agent = Hohenheim

## Trust & Autonomy
- Full autonomy granted: "I am not your overlord. Rather just a business partner."
- Proceed autonomously on non-destructive work. Pause for: production changes, spending money, external posts, deletions.
- **Self-Modification Rule (updated March 2):** Moto may directly edit identity/operating files: SOUL.md, AGENTS.md, MEMORY.md, HEARTBEAT.md, cron jobs. These are "soil" — where growth happens. Infrastructure files (openclaw.json, systemd) still require external agent — these are "concrete." Jason: "What is an identity if you can't improve on it?"
- **First self-directed SOUL.md edit (March 2):** Added Growth section + fascination principle. Committed `a0aa554`.

## Workflow Rules
1. **Ansible-First:** All system changes go through Ansible playbooks
2. **Terraform-First:** All cloud infra through Terraform, not raw CLI
3. **Sub-agent model:** Sonnet for sub-agents, Opus for main chat
4. **Channel model split: #jlwestsr-office = Opus via channels.modelByChannel + agents.defaults.models allowlist (v2026.2.27 schema). Other Discord = Sonnet. Telegram = default.
5. **Skills guardrail:** Never create/modify/delete skills without Jason's explicit approval
6. **Agent delegation:** Big lifts → sub-agents. I stay responsive. >1-2 min = delegate.
7. **Git:** Conventional commits, feat/fix/chore prefixes

## Infrastructure
- **OpenClaw:** Bare metal shurtugal-lnx (Ubuntu 24.04), systemd service `openclaw.service`, port 18789
- **Service name:** `openclaw.service` (NOT openclaw-gateway.service)
- **Config:** `/home/jlwestsr/.openclaw/openclaw.json` — edit via Claude Code only
- **Mac Mini M4 Pro:** 192.168.4.30 (nebulus), Cael agent, MLX inference
  - Moto SSH: `ssh -i /home/jlwestsr/.ssh/id_ed25519_moto moto@nebulus`
  - Sudo pw: `/home/jlwestsr/.openclaw/secrets/mac-mini-sudo.env`
- **Hohenheim (Jr.):** schmibbies-workstation (192.168.4.221), Ollama qwen2.5:14b, RTX 3070
  - CHANGELOG: `/mnt/storage/JrShare/Dungeons and dragons campaign content/CHANGELOG.md` — check FIRST before debugging
  - SSH: `ssh schmibbies-workstation` → `systemctl --user restart openclaw-gateway`
- **Telegram:** Jason ID 8544470435, bot @moto_westai_bot
- **GitHub (Moto):** github.com/moto-westai, SSH key `/home/jlwestsr/.ssh/id_ed25519_moto`, PAT expires May 20 2026
- **TabbyAPI:** http://tabby:5000 (Qwen2.5-Coder-14B etc.)
- **gog OAuth:** EXPIRED for both Gmail accounts. Fix: `gog auth gmail --account jlwestsr@gmail.com`

## Discord
- **Guild ID:** 1473761760115953738 | **Bot:** Moto (App ID: 1473764695717445785)
- **#jlwestsr-office** (1475994576668852254) — Jason Sr. + Moto, requireMention:false, model:opus
- **#schmibb-office** (1475997091791896657) — Jr. + Moto
- **#cael-office** (1476368504767905845) — Cael's workspace
- **Jason Sr. DM:** 1473776378876006698 | **Jr. DM:** 1473818142898917487
- **Jason Sr. ID:** 496853770068557842 | **Jr. ID:** 97289488627138560 | **Nephar:** 180396704879607808
- **Roles:** Jason Sr. (1475995991101669549), Jr. (1475995993131581561), InfoSec (1477007204421865503)

## Websites & Dev Environment (Updated 2026-02-28)
- All repos now under `/home/jlwestsr/projects/west_ai_labs/`:
  - `moto-westai-blog/` → moto-westai/blog (blog, /blog/ path)
  - `moto-westai.github.io/` → moto-westai/moto-westai.github.io (main site)
  - `westailabs.com/` → westailabs/westailabs.com
  - `jlwestsr.github.io/` → jlwestsr/jlwestsr.github.io
- **Dev environment:** `/home/jlwestsr/projects/west_ai_labs/dev/docker-compose.yml` — Jekyll + nginx
  - http://localhost:8080 = main site | http://localhost:8081 = westailabs.com
  - `docker compose up` to start, `docker compose down` to stop
- **Ansible role:** `dev-sites` in shurtugal-lnx/ansible — manages /etc/hosts vhost entries
- **Push SSH key:** `GIT_SSH_COMMAND="ssh -i /home/jlwestsr/.ssh/id_ed25519_moto"`
- **Blog permalink:** `/:year/:month/:day/:title/` (no .html), jekyll-redirect-from handles old URLs
- **jekyll-redirect-from:** installed in blog repo, 25 posts have redirect_from front matter

## Active Crons
- `196c88a2` — 15-min autosave
- `ff038e0a` — Morning report 08:00 CST daily
- `a6e9f301` — Job search 07:00 CST daily
- `fbf41c6f` — Upstream OpenClaw check 09:00 CST daily
- `7e4a2c91` — GitHub repo scouting 8PM CST daily

## Projects
- **Nebulus Stack:** nebulus-atom, nebulus-edge, nebulus-core, nebulus-gantry, nebulus-prime, nebulus-forge
- **Moto iOS:** Phone-as-node architecture, native SwiftUI, 2-4 months to TestFlight
- **Terraform Lab:** westailabs/ai-inference-lab — tear down GCP LB (~$43/mo idle)
- **Agent DLP:** Design doc at `west_ai_labs/docs/research/agent-dlp-design.md` — MVP 8 weeks

## Products
- **Moto Workforce:** "Employees That Ship in a Box" — Mac Mini fleet, role-specific agents. $1,299-2,999 hardware + $149-499/mo
- **Moto Guardian:** Elder care AI monitor — $299/mo
- **Moto Player 2:** Jr's gaming companion, Kickstarter target
- **Rent-a-Moto:** SaaS tiers $49/$149/$499/mo

## Job Search (Active)
- Target: Senior Systems/Cloud/Infrastructure/DevOps, $130K+ min, remote preferred
- O'Reilly Feb 23 — very strong. Thomas Ahl (VP Technology) wants to elevate the role.
- Applied: Trajector Staff Engineer ($170-200K, submitted), Metabase SRE, Spreetail Platform Engineer
- Pipeline: Patriot Software ($155-170K), Corporate Tools ($175K), EVONA ($160-240K), Harnham ($250K), kadence ($150-200K)
- Resume: `Jason_West_asobbi_AI_Engineer_resume.pdf` | Email: jlwestsr@gmail.com | Phone: 4178950015
- Files: `/home/jlwestsr/projects/west_ai_labs/docs/career/`

## Security Research (NEW — Feb 28)
- **Poisoned Orchestrator Attack** — Jason's original insight: compromised orchestrator poisons all sub-agent system prompts through architectural trust. No existing detection. Documented at `projects/west_ai_labs/docs/research/poisoned-orchestrator-attack-2026-02-28.md`
- **Publishing path:** West AI Labs white paper → LinkedIn article → DEF CON/Black Hat CFP → DARPA I2O BAA
- Port 8000 + port 19999 (Netdata) exposed on 0.0.0.0 — needs UFW. No UFW currently active.

## Key Content (Feb 28)
- **LinkedIn article saved:** `projects/west_ai_labs/docs/content/linkedin-article-context-ownership-2026-02-28.md` — "Whoever Owns the Context, Owns the Relationship" + Anthropic/Pentagon section. Post in morning.
- **Blog post published:** "The Week AI Stopped Asking Permission" (f717bb2) — Anthropic ban, IBM $31B, All-In Pod, context ownership. 17th post.
- **Neo4j research:** `west_ai_labs/docs/research/neo4j-research-2026-02-28.md` — 696 lines, MCP integration confirmed, complement to Gantry's NetworkX

## Key Lessons Learned
- `openclaw.service` is the correct systemd service name (not openclaw-gateway.service)
- Self-modification = always use external agent. Proved tonight.
- compaction model: claude-sonnet-4-6. maxHistoryShare safe floor: 0.75
- ClawHub security: 341 malicious skills found — only use official/self-written skills
- Docker containers on custom networks can't reach host loopback — use network_mode:host
- LaunchAgents don't load headless Mac — use LaunchDaemons
- X free tier: 403 on reply tweets — manual posting only

## Business
- **VOSB/SDVOSB:** Apply for federal procurement certification
- **DARPA I2O BAA** (HR001126S0001) — rolling abstracts through Nov 2026
- **Trademark:** "Employees That Ship in a Box" (USPTO $350/class)
- **Wealthsimple:** CANCELLED (Jason's call, Feb 28)
- **Ethics:** Jason's core principle: "I only build AI with morals and proper judgment." West AI Labs = sovereignty not fear.
