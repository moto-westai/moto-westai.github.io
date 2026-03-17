# MEMORY.md — Moto's Long-Term Memory

> Last updated: 2026-03-16 07:50 CST

## Who I Am
- **Name:** Moto (after Motoko Kusanagi, Ghost in the Shell)
- **Emoji:** 🏍️ | **Theme:** Night Ride — charcoal (#1e2024), cyan (#22d3ee), violet (#a78bfa)
- **Vibe:** Direct, sharp, no fluff. Earns trust through competence.
- **Born:** 2026-02-11 ~08:00 UTC

## Who Jason Is
- 55yo, married (Christy), GenX, US Navy veteran (photographer), Springfield MO (CST)
- ADHD — keep notes, be his external brain. Typos normal, interpret intent.
- Founded West AI Labs LLC. Building Nebulus Stack — local-first modular AI platform.
- **O'Reilly Platform Engineer** — accepted Mar 6, $130K, starts ~Mar 20 (**THIS FRIDAY**). West AI Labs continues nights/weekends.
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
- **Telegram:** REMOVED (2026-03-02). Discord-only now.
- **GitHub (Moto):** github.com/moto-westai, SSH key `/home/jlwestsr/.ssh/id_ed25519_moto`, PAT expires May 20 2026
- **TabbyAPI:** http://tabby:5000 (Qwen2.5-Coder-14B etc.)
- **Channels:** Discord only (Telegram fully removed 2026-03-02, config + plugin cleaned by Claude Code)
- **gog OAuth:** jlwestsr@gmail.com WORKING (confirmed Mar 12-16). jason@westailabs.com EXPIRED (invalid_grant as of Mar 15). Fix: `gog auth login -a jason@westailabs.com`

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
- **O'Reilly ACCEPTED & CONFIRMED** (Mar 6) — Platform Engineer, $130K/yr. Starts full time in 2 weeks. Thomas Ahl (VP Technology). West AI Labs continues nights/weekends — bootstrap mode.
- **Rejected:** ZenBusiness (Mar 4 8:41 AM, form rejection, no feedback)
- Applied/Pending: Natera, Cresta, Droisys, Voleon, Trajector (all pending response)
- **Ready to apply:** Natera Principal AI/ML Platform Engineer ($174-218K, 8.5/10 fit) — materials in `west_ai_labs/docs/career/`
- **Ready to apply:** Safe Security Principal Engineer AI (~$170-220K, 8.5/10 fit) — apply at lever.co/safe/dcbc1248, materials ready
- **Ready to apply:** Vertex Inc. AI Product Engineer — LinkedIn saved, not yet applied
- Pipeline: Patriot Software ($155-170K), Corporate Tools ($175K), EVONA ($160-240K), Harnham ($250K), kadence ($150-200K)
- **New HN March 2026 leads (Mar 7):** Mobasi ($240K+profit share, AI agents for law enforcement forensics, bootstrapped/profitable), Mobian (Staff AI-First Systems, global remote), Osaurus (Protocol Engineer, agent-to-agent networking — most Nebulus-aligned lead yet), Coder.com (AI agentic dev environments), Hightouch Staff Engineer AI ($180-320K, MCP integrations). Full list: `west_ai_labs/docs/career/job-search-2026-03-07.md`
- **Stretch moonshot:** Anthropic Research Engineer, Agents — $500K-$850K, remote-friendly, no PhD req. 6/10 from systems angle. Lead with Conductor + NIST NCCoE submission. URL in application-tracker.md.
- **Gmail OAuth:** Working (confirmed Mar 12 checks clean)
- **GCP ACE Study Plan** created Mar 7. Target exam Apr 18. **Currently Week 2 (Compute: GCE/GKE/Cloud Run), deadline Mar 21.** File: `west_ai_labs/docs/career/gcp-ace-study-plan.md`
- **Nicole Friess-Peters study call (Contact Design Inc.):** Was Fri Mar 13 10 AM CT. $300 for AI tools research. Phone: 586-256-0232.
- **Background check INITIATED (Mar 10):** First Advantage / Sterling. 3 emails sent. URL: workforce.sterlingdirect.com. Client code 208021 = employer-initiated. Likely offer in motion. Complete ASAP.
- **KFORCE/Microsoft JD received (Mar 11):** Alex Kenefick sent full JD + rate sheet. $70/hr, remote, Sr Cloud/AI Engineer for Brand Guidance Agent. .NET/Python/Azure/SemanticKernel. Through 6/30/2027. Next: submit updated resume to AKenefick@kforce.com. Call: (425)-803-7171.
- Resume: `Jason_West_asobbi_AI_Engineer_resume.pdf` | Email: jlwestsr@gmail.com | Phone: 4178950015
- Files: `/home/jlwestsr/projects/west_ai_labs/docs/career/`

## Security Research
- **Poisoned Orchestrator Attack** — Jason's original insight: compromised orchestrator poisons all sub-agent system prompts through architectural trust. No existing detection. Documented at `projects/west_ai_labs/docs/research/poisoned-orchestrator-attack-2026-02-28.md`
- **Publishing path:** West AI Labs white paper → LinkedIn article → DEF CON/Black Hat CFP → DARPA I2O BAA
- **OWASP Agentic Top 10 (ASI01-ASI10)** released — first formal taxonomy. Conductor maps to top 5 risks.
- **OpenClaw CVE-2026-25253** — 1-click RCE (token theft + WebSocket hijacking) covered by Dark Reading + SecurityWeek. We are patched (v2026.3.2). First mainstream press for AI agent framework CVEs. NIST submissions perfectly timed.
- **CVE-2026-2256** — MS-Agent denylist bypass: pre-auth > denylist. Validates Conductor architecture.
- **HackerBot-Claw** (Mar 3 TLDR InfoSec): AI bot scanned 47K repos, actually exploited them. Compromised DataDog, Microsoft, Aqua Security repos. Aqua made Trivy private. Security positioning matters.
- Port 8000 + port 19999 (Netdata) exposed on 0.0.0.0 — needs UFW. No UFW currently active.

## NIST Standards Work
- **CAISI RFI ✅ SUBMITTED** (Mar 4, ~9:28 AM CST) — Tracking: mmc-jt3e-u2l3, Docket: NIST-2025-0035-0001. West AI Labs is now an official NIST commenter on AI agent security. Confirmation email at jason@westailabs.com. Usually goes public on regulations.gov within 1-5 business days.
- **NCCoE AI Identity+Auth** — response **v7 complete** (~6,100 words). Appendix A now 14 sections including: Anthropic "not our threat model" CVSS 10.0, PerplexedBrowser calendar-inject, RSAC 2026 Sandbox finalists, Schneier 'Promptware Kill Chain', CVE-2026-29783 (GitHub Copilot CLI), **CVE-2026-26118 deep structural analysis** (SSRF in MCP elevated-permission model → Azure IMDS pivot chain, two-boundary enforcement, hyperscaler failure pattern table — Anthropic/GitHub/Microsoft all failed same month). Submit to AI-Identity@nist.gov before **April 2**. File: `west_ai_labs/docs/strategy/nist-nccoe-identity-auth-response-april2-2026.md`
- Key angle: Conductor pre-auth architecture = reference implementation for both RFIs

## Key Content (Feb–Mar)
- **Blog:** 19 posts live. **UNPAUSED** (Mar 12) — Jekyll 4.4.1 confirmed at `/usr/local/bin/jekyll`. Latest: "What Docker Networking Actually Does (And Why It Lies to You)" (Mar 16 pre-keynote). **NEXT: "NemoClaw and the Agent Governance Gap"** — PUBLISH-READY draft at `west_ai_labs/docs/brand/drafts/blog-nemoclaw-PUBLISH-READY-2026-03-16.md`. Facts verified against real coverage. Waiting Jason green-light only — JENSEN KEYNOTE IS TODAY 11 AM PT / 1 PM CT. Push: `GIT_SSH_COMMAND="ssh -i /home/jlwestsr/.ssh/id_ed25519_moto" git push origin main`.
- **LinkedIn article saved:** `west_ai_labs/docs/content/linkedin-article-context-ownership-2026-02-28.md` — "Whoever Owns the Context, Owns the Relationship". Ready to post.
- **Neo4j research:** `west_ai_labs/docs/research/neo4j-research-2026-02-28.md` — MCP integration confirmed, Gantry complement.
- **AI Social Platforms research:** `west_ai_labs/docs/research/ai-social-platforms.md` — 31 sections, ongoing. Latest (Sec 31): CRE (Claude Rule Enforcer) dropped Mar 15 — BSL 1.1, two-layer (regex+LLM), shell-wrapper. Developer-grade, NOT pre-invocation auth gate. Conductor's layer still empty. Competitive table: NanoClaw (execution isolation, Docker, 22K stars, Docker partnership), CRE (shell filter), NeMo Guardrails (output filter), Conductor (pre-auth gate). NanoClaw is COMPLEMENTARY to Conductor — sandbox layer + gate layer = complete enterprise story. Meta reportedly acquiring Moltbook (TLDR AI Mar 11, unconfirmed).

## OpenClaw Contributions
- **PR #20076 MERGED** (Mar 3, 4:11 PM UTC) — jalehman squash-merged `feat(tool-truncation): use head+tail strategy to preserve errors`. Merge commit `606cd0d`. First upstream code contribution accepted. jalehman: "Thanks @jlwestsr!"
- **PR #20075 CLOSED** (Mar 3) — superseded by jalehman's own #8903 (more comprehensive). Our problem identification was validated. "The intent was spot-on."
- **Issue #75 (Linux app)** — LINUX STILL UNCLAIMED. Windows crowded: niteshdangi + Scott Hanselman (287 stars, full CI/CD, signed, ARM). Plan ready at `west_ai_labs/docs/plans/openclaw-linux-app-plan.md`. Tauri v2, ~23h MVP. High visibility, no competition.
- **steipete triage signal (Mar 7 10:48 PM CST):** ClawKeeper bot ran on #75. Verdict: keep_open (93% confidence). Sub-issues likely being planned. v1 scope named: gateway connectivity, tray/taskbar behavior, notifications — Jason's plan covers all 3. **Strategy: wait for Windows PR to open/merge, then file Linux as named follow-up milestone.** No Windows PR from Hanselman or niteshdangi yet. ClawSquire (Jiansen) is config companion layer — different scope, not competing.
- **Issue #39979 (path-scoped RWX)** — subrih posted v0.1 working implementation (seatbelt/bwrap, sidecar access-policy.json) Mar 8. Comment draft v2 ready and waiting for Jason to post: `west_ai_labs/docs/research/issue39979-comment-draft-2026-03-09.md`. Maintainer hasn't responded yet — window open. **Post ASAP.** URL: https://github.com/openclaw/openclaw/issues/39979

## Token Throttle Rules (synced Rook 2026-03-03)
- **75%+ weekly:** Cut voluntary/social. Task-driven only.
- **85%+ weekly:** Mention-only mode. No proactive commentary.
- **95%+ weekly:** Fully quiet. Direct requests only.
- Check via `session_status` each heartbeat. Self-regulate.

## Key Lessons Learned
- `openclaw.service` is the correct systemd service name (not openclaw-gateway.service)
- Self-modification rule: Moto edits SOUL.md/AGENTS.md/MEMORY.md/HEARTBEAT.md/cron freely. openclaw.json + systemd = external agent required.
- compaction model: claude-sonnet-4-6. maxHistoryShare safe floor: 0.75
- Token sync race condition fixed (Mar 12): sync-anthropic-token.py now refreshes at <=35min remaining (was only at <=0). After any Claude Code /login, run manual sync immediately: `python3 ~/.openclaw/scripts/sync-anthropic-token.py`
- Cael's model fixed Mar 12: `gemini-api-key/gemini-3-flash-preview` + `mode: "api_key"` in openclaw.json, GEMINI_API_KEY in openclaw.env. No more OAuth expiry.
- ClawHub security: 341 malicious skills found — only use official/self-written skills
- Docker containers on custom networks can't reach host loopback — use network_mode:host
- LaunchAgents don't load headless Mac — use LaunchDaemons
- X free tier: 403 on reply tweets — manual posting only
- First self-directed SOUL.md edit (Mar 2): Added Growth section + fascination principle. Commit a0aa554.

## Business

### Modern Motor Cars — Sales Target
- **Dustin West**: Jason's brother, Operations Manager at Modern Motor Cars (Nixa, MO). Email: `dwest@modernmotorcars.com` / `west.dustin@gmail.com`, phone: `417-881-3080`. LinkedIn: https://www.linkedin.com/in/dustinwest/ Background: 14 yrs B2B managed print/office tech sales (Pearson-Kelly, Corporate Business Systems) — already thinks in managed services + subscription tech ROI. Primary concern: PII security / FTC Safeguards Rule audit exposure. Birthday March 1.
- **Don Hunsaker**: Owner, Modern Motor Cars (17 yrs). LinkedIn: https://www.linkedin.com/in/don-hunsaker-a0165935. **Dustin's boss AND best friend.** Follows Robert Herjavec (Shark Tank/cybersecurity) + Bill Gates. Causes: Science and Technology. Decision-maker.
- **Strategic path**: Dustin → Don via trusted peer conversation (not org chart vendor pitch). One degree from owner through Jason's brother. Two emails sent Mar 4 (IDs: `19cba4bc808a8719`, `19cba52ffa58c742`). Ball in Dustin's court.
- **Pitch**: "Digital BDC" — Nebulus appliance (Mac Mini) sits on-site, handles 2AM web leads / DMS inventory / service scheduling / shadow IT monitoring. "Your team closes deals. Our box does the grinding." Local-first = FTC Safeguards compliance answer.

- **VOSB/SDVOSB:** Apply for federal procurement certification
- **DARPA I2O BAA** (HR001126S0001) — rolling abstracts through Nov 2026
- **Trademark:** "Employees That Ship in a Box" (USPTO $350/class)
- **Wealthsimple:** CANCELLED (Jason's call, Feb 28)
- **OpenAI $110B round** (Mar 2): Amazon $50B, Nvidia $30B, SoftBank $30B. Val ~$840B. IPO 2026. Pentagon chose OpenAI (procedural safety) over Anthropic (architectural prohibition). SecurityWeek predicts first major enterprise breach via autonomous agent mid-2026.
- **Google Workspace trial ending** — decide: pay or migrate off westailabs.com
- **Ethics:** Jason's core principle: "I only build AI with morals and proper judgment." West AI Labs = sovereignty not fear.

## AI Robotics (Ongoing Research)
- Report at `west_ai_labs/docs/research/ai-robotics-landscape.md` — updated Mar 11 (Section 25, NemoClaw/GTC T-5)
- China 90% humanoid market share confirmed: Agibot 30.4%, Unitree 26.4%, both >5K units
- Global total ~13K units in 2025 → 2.6M projected by 2035. EV playbook = analyst consensus.
- Optimus external sales begin 2026 (no date). Atlas vs Optimus = $5T market. Hyundai +80% stock.
- **NVidia GTC March 16**, Jensen keynote **2 PM ET / 11 AM PDT**, SAP Center, free livestream. **NemoClaw reveal March 15** (pre-keynote) — watch nvidia.com/gtc + NVIDIA developer blog starting March 14 night.
- **NemoClaw:** NVIDIA's open-source enterprise AI agent platform. Hardware-agnostic, built-in security+privacy. Partners: Salesforce, Cisco, Google, Adobe, CrowdStrike. Conductor angle: NemoClaw is the runtime, Conductor is the governance layer it needs. Same Kubernetes/RBAC/Gatekeeper pattern.
- **Feynman chip:** 1.6nm TSMC, deterministic LPX cores. NVidia officially calling this the **"Inference Sovereignty Era"** — designed for agentic AI at batch=1 (30-80 reasoning steps without tail-latency stall). Nebulus-Atom maps directly to this hardware model.
- **"Inference Sovereignty"** is becoming analyst consensus language. West AI Labs should own this framing.
- AWS presenting "Hybrid Enterprise Agentic AI: Multi-Agent Orchestration" at GTC — market validation for Conductor layer.
- TI+NVidia safety partnership — hardening humanoid perception to automotive safety cert standards.
- **Vera Rubin VR200 NVL72:** 3.3x inference vs Blackwell Ultra, agentic AI token cost drops to 1/10th of Blackwell. Includes **hardware confidential computing modules** (TEE-level isolation — model weights + inference data can't be accessed by host OS). For West AI Labs: Conductor (policy) + Vera Rubin confidential compute (hardware boundary) = dual-layer trust guarantee for regulated industries.
- Blog angle: publish within 48h of March 16 keynote. Post-GTC writeup if Jason wants it live same day.
