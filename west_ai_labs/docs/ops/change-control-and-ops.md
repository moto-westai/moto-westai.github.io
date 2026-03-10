# Moto Operations & Change Control

> Established: 2026-02-20  
> Owner: Jason West / Moto  
> Status: DRAFT — awaiting Jason's review

---

## Infrastructure

| Role | Host | IP | OS | Notes |
|------|------|----|----|-------|
| **Production** | shurtugal-lnx | localhost | Ubuntu 24.04 | Gateway port 18789. DO NOT modify without approval. |
| **Staging/DR** | Mac Mini M4 Pro | 192.168.4.30 | macOS | Resettable. Staging gateway + DR failover. |

---

## Change Control Pipeline

### 1. Dev
- All code changes happen in the fork: `~/.openclaw/workspace/openclaw-fork/`
- Branch convention: `moto/<feature-name>`
- Conventional commits: `feat:`, `fix:`, `chore:`
- No direct commits to main without review

### 2. Staging
- **Staging gateway** on Mac Mini, port 18790
- Deploy changes to staging FIRST
- Validate basic functionality:
  - [ ] Gateway starts without errors
  - [ ] WebSocket connections work
  - [ ] Telegram channel responds
  - [ ] Memory/session persistence intact
  - [ ] Cron scheduler fires

### 3. QA
- Run QA checklist before promoting to production:
  - [ ] All channels functional (Telegram, Discord)
  - [ ] Sub-agent spawning works
  - [ ] Compaction completes without loops
  - [ ] Memory flush writes correctly
  - [ ] No error spam in logs
  - [ ] Config changes apply cleanly
  - [ ] Rollback tested (can revert in <60 seconds)

### 4. Load Test
- Concurrent session test:
  - [ ] Telegram DM + Discord server messages simultaneously
  - [ ] Cron jobs firing during active conversation
  - [ ] Sub-agent spawn during main session activity
  - [ ] Compaction under load (does it block responses?)
- Token burn check:
  - [ ] Workspace file injection size vs maxHistoryShare headroom
  - [ ] Compaction doesn't loop (verify <3 compactions per hour)

### 5. Production Promotion
- **REQUIRES Jason's explicit approval**
- Pre-promotion:
  1. Document current production state (PID, version, uptime)
  2. Create backup: `tar czf ~/openclaw-backup-$(date +%Y%m%d-%H%M%S).tar.gz ~/.openclaw/`
  3. Send Jason the rollback command BEFORE proceeding
  4. Get explicit "go" from Jason
- Promotion:
  1. Stop staging gateway on Mini
  2. Apply changes to production (rebuild + restart)
  3. Validate with QA checklist (abbreviated)
  4. Confirm to Jason: "Production updated, all checks pass"
- **Rollback:** If anything fails, execute the pre-documented rollback command immediately

---

## Disaster Recovery

### Backup Strategy
| What | Where | Frequency | Retention |
|------|-------|-----------|-----------|
| OpenClaw config | `~/.openclaw/` | Daily | 7 days |
| Workspace (memory, SOUL, AGENTS, etc.) | `~/.openclaw/workspace/` | Daily + pre-change | 7 days |
| Session state | `memory/session-state.json` | Every 15 min (autosave) | Current |
| Daily logs | `memory/YYYY-MM-DD.md` | Continuous | 30 days |
| MEMORY.md | Workspace root | On change | Git versioned |
| Secrets | `~/.openclaw/secrets/` | Pre-change only | Manual |

### Backup Locations
- **Primary:** shurtugal-lnx local (tar.gz snapshots)
- **Secondary:** Mac Mini (rsync mirror)
- **Tertiary:** GitHub (workspace files via git push)

### Recovery Targets
- **RTO (Recovery Time Objective):** < 15 minutes to restore service
- **RPO (Recovery Point Objective):** < 1 hour of data loss (autosave cadence)

### Recovery Procedures
See Runbooks below.

---

## Runbooks

### RB-001: Gateway Restart (Production)
**When:** Gateway is unresponsive or needs update  
**Risk:** HIGH — Moto goes offline  
**Requires:** Jason's approval  

1. Verify current state:
   ```bash
   pgrep -af openclaw
   ss -tlnp | grep 18789
   ```
2. Document PID and rollback:
   ```bash
   echo "Rollback: kill <new_pid> && <start_old_command>"
   ```
3. Send rollback to Jason. Wait for "go."
4. Create backup:
   ```bash
   tar czf ~/openclaw-backup-$(date +%Y%m%d-%H%M%S).tar.gz ~/.openclaw/
   ```
5. Stop gateway:
   ```bash
   kill <pid>
   ```
6. Start new gateway:
   ```bash
   cd ~/.openclaw/workspace/openclaw-fork
   nohup node dist/index.js gateway --port 18789 > /tmp/openclaw-gateway.log 2>&1 &
   ```
7. Validate:
   ```bash
   sleep 5
   curl -s http://127.0.0.1:18789/ | head -1  # Should return HTML
   ```
8. Confirm to Jason: "Gateway restarted, PID <new>, all channels up."

### RB-002: Fork Sync & Rebuild
**When:** Upstream OpenClaw has new commits  
**Risk:** MEDIUM — build could fail, conflicts possible  

1. Create backup branch:
   ```bash
   cd ~/.openclaw/workspace/openclaw-fork
   git branch backup/pre-sync-$(date +%Y%m%d)
   ```
2. Fetch upstream:
   ```bash
   git fetch upstream
   ```
3. Check what's new:
   ```bash
   git log --oneline HEAD..upstream/main | head -20
   ```
4. Rebase:
   ```bash
   git rebase upstream/main
   ```
5. If conflicts: resolve, `git add`, `GIT_EDITOR=true git rebase --continue`
6. Build:
   ```bash
   export PATH="$HOME/.local/bin:$PATH"
   export COREPACK_HOME=~/.corepack
   pnpm build
   ```
7. If build fails: `git rebase --abort` and restore backup branch
8. Push: `git push origin main --force-with-lease`
9. Deploy to staging first (see RB-004)

### RB-003: Full Restore from Backup
**When:** Catastrophic failure, need to rebuild from scratch  
**Risk:** Service outage during restore  

1. Identify latest backup:
   ```bash
   ls -lt ~/openclaw-backup-*.tar.gz | head -5
   ```
2. Stop any running gateway
3. Extract backup:
   ```bash
   tar xzf ~/openclaw-backup-<timestamp>.tar.gz -C /
   ```
4. Verify config:
   ```bash
   cat ~/.openclaw/openclaw.json | python3 -m json.tool
   ```
5. Start gateway (see RB-001 step 6-7)
6. Validate all channels

### RB-004: Deploy to Staging (Mac Mini)
**When:** Testing changes before production  
**Risk:** LOW — staging only  

1. SSH to Mac Mini (or prompt Jason to run):
   ```bash
   ssh jlwestsr@192.168.4.30
   ```
2. Sync workspace:
   ```bash
   rsync -avz ~/.openclaw/workspace/openclaw-fork/ mini:~/openclaw-staging/
   ```
3. Start staging gateway:
   ```bash
   cd ~/openclaw-staging
   node dist/index.js gateway --port 18790
   ```
4. Test from shurtugal-lnx:
   ```bash
   curl -s http://192.168.4.30:18790/ | head -1
   ```
5. Run QA checklist

### RB-005: Compaction Troubleshooting
**When:** Compaction loops, excessive token burn, stale context  
**Risk:** LOW-MEDIUM  

1. Check compaction count in last hour:
   ```bash
   grep -c "compaction" /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log
   ```
2. If >3 compactions/hour: likely maxHistoryShare too low
   - Current safe floor: 0.75
   - Check workspace file sizes: `du -sh ~/.openclaw/workspace/*.md`
3. If workspace files growing: trim HEARTBEAT.md, TOOLS.md, or raise maxHistoryShare
4. Compaction model: claude-sonnet-4-6 (NOT Opus — too slow/expensive)

### RB-006: Incident Response — Moto Down
**When:** Jason can't reach Moto on any channel  
**For:** Jason (human-executable)  

1. SSH to shurtugal-lnx
2. Check gateway:
   ```bash
   pgrep -af openclaw
   ss -tlnp | grep 18789
   ```
3. If not running, start it:
   ```bash
   cd ~/.openclaw/workspace/openclaw-fork
   nohup node dist/index.js gateway --port 18789 > /tmp/openclaw-gateway.log 2>&1 &
   ```
4. If won't start, check logs:
   ```bash
   tail -50 /tmp/openclaw-gateway.log
   cat /tmp/openclaw/openclaw-$(date +%Y-%m-%d).log | tail -50
   ```
5. If all else fails, restore from backup (RB-003)

---

## Self-Modification Protocol

**MANDATORY for all changes that could affect Moto's availability:**

1. Document current working state + exact rollback command
2. Send Jason the rollback instructions BEFORE making the change
3. Get explicit go-ahead before killing any running service
4. Test on staging (Mac Mini) first when possible
5. Never touch production during Jason's quiet hours unless emergency

**This exists because Jason depends on Moto being available.**  
**Going down = Jason loses his copilot.**  
**Treat uptime as a production SLA.**

---

---

## Monitoring & Alerting

### Health Checks
| Check | Frequency | Alert Threshold | AI-Automated? |
|-------|-----------|----------------|---------------|
| Gateway process alive | Heartbeat (30 min) | Process not running | ✅ Yes — heartbeat check |
| Telegram channel responsive | Heartbeat | No response to test | ✅ Yes |
| Discord bot connected | Heartbeat | Bot offline | ✅ Yes |
| Disk space | Daily | < 10GB free | ✅ Yes |
| Token burn rate | Per-session | > $5/hr sustained | ✅ Yes — log analysis |
| Compaction frequency | Continuous | > 3/hour | ✅ Yes — pattern detection |
| Memory file freshness | Daily | session-state.json > 1hr stale | ✅ Yes |
| Upstream commits | Daily (9 AM) | Security-tagged commits | ✅ Yes — cron |
| API key expiration | Weekly | < 30 days to expiry | ✅ Yes — cron |

### Alert Delivery
- **Primary:** Telegram DM to Jason
- **Secondary:** Discord #motos-office
- **Quiet hours (23:00-08:00 CST):** Suppress non-critical alerts

---

## Security & Access Control

### Secret Inventory
| Secret | Location | Expires | Rotation |
|--------|----------|---------|----------|
| Anthropic API key | openclaw.json | N/A | On compromise |
| GitHub PAT (Moto) | ~/.openclaw/secrets/github-moto.env | May 20, 2026 | Reminder cron May 13 |
| Discord bot token | ~/.openclaw/secrets/discord.env | N/A | On compromise |
| X/Twitter keys | ~/.openclaw/secrets/x-westailabs.env | N/A | On compromise |
| Mac Mini sudo | ~/.openclaw/secrets/mac-mini-sudo.env | N/A | Quarterly |
| Mac Mini jlwestsr | ~/.openclaw/secrets/mac-mini-jlwestsr.env | N/A | Quarterly |

### Access Control
- **Production gateway:** Token auth (auth.mode: "token")
- **Staging gateway:** Open auth for testing (switch to token before any external exposure)
- **SSH keys:** Ed25519 only. No password auth.
- **Audit trail:** Daily logs in `memory/YYYY-MM-DD.md`, session-state.json

---

## Versioning & Release Tags

- Fork tracks upstream OpenClaw via `git rebase upstream/main`
- Our commits sit on top of upstream HEAD
- Tag convention: `moto/v{date}` for production deployments
- Backup branches: `backup/pre-sync-YYYYMMDD` before each rebase
- Production binary tracked by PID + build timestamp in daily log

---

## CI/CD (Future)

### Current (Manual)
1. Fork sync → rebuild → test on staging → promote

### Target (GitHub Actions)
- On push to `main`: build + basic smoke test
- On PR: run full test suite
- On tag `moto/v*`: deploy to staging automatically
- Production promotion: manual trigger with approval gate

---

## Change Advisory Board (CAB)

For a two-person team, CAB = a structured conversation:

1. **Moto proposes** change (what, why, risk, rollback)
2. **Jason approves** or requests modification
3. **Moto executes** and reports result
4. **Post-change review** in daily scrum

For autonomous non-destructive changes (staging, research, writing):
- Moto proceeds and reports in next scrum
- Jason reviews async

---

## Rollback Testing

### Monthly DR Drill
- [ ] Stop staging gateway
- [ ] Simulate data loss (rename workspace)
- [ ] Restore from latest backup
- [ ] Verify: config loads, channels connect, memory intact
- [ ] Document results + time-to-recovery
- [ ] Compare against RTO target (< 15 min)

---

## Dependency Management

| Dependency | Current | Track | Update Strategy |
|-----------|---------|-------|----------------|
| OpenClaw (upstream) | Synced Feb 20 | Daily cron | Rebase + rebuild |
| Node.js | v24.12.0 (shurtugal) / v25.4.0 (Mini) | LTS | Quarterly |
| pnpm | v10.23.0 | Latest | With builds |
| Ubuntu (shurtugal) | 24.04 | LTS | `apt upgrade` monthly |
| macOS (Mini) | 26.2 | Latest | Apple auto-update |

---

## AI Automation Opportunities

| Stage | Current State | AI Automation | Human Role |
|-------|--------------|---------------|------------|
| **Monitoring** | Heartbeat checks | ✅ Automated via heartbeat + cron | Set thresholds |
| **Alerting** | Telegram ping | ✅ Automated delivery | Acknowledge + act |
| **Fork sync** | Manual trigger | 🔜 Cron-triggered, auto-rebase | Approve conflicts |
| **Build** | Manual | 🔜 CI/CD pipeline | Review failures |
| **Staging deploy** | Manual SSH | 🔜 Automated post-build | Validate results |
| **QA** | Manual checklist | 🔜 Automated smoke tests | Review edge cases |
| **Load testing** | Not yet | 🔜 Scripted concurrent sessions | Set thresholds |
| **Prod promotion** | Manual + approval | ❌ Always human-approved | **APPROVE** |
| **Backup** | Manual tar.gz | 🔜 Cron daily backup | Verify monthly |
| **Scrum report** | Manual | ✅ Automated daily delivery | Read + respond |
| **Secret rotation** | Manual | 🔜 Expiry alerts automated | Execute rotation |
| **Runbook execution** | Manual | 🔜 Scripted + approval gates | Authorize |

**Key insight:** AI handles 80% of execution. Humans hold 100% of approval gates for production changes. This is the Moto Workforce value proposition.

---

## Daily Scrum Template

```
🔄 Daily Ops Scrum — {date}
━━━━━━━━━━━━━━━━━━━━━━━━
DEV:      {commits ahead of upstream}
STAGING:  {status, last deploy}
QA:       {last run, pass/fail}
LOAD:     {last test, results}
PROD:     {gateway PID, uptime}
DR:       {last backup date, age}
BLOCKERS: {current blockers}
━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Revision History

| Date | Change | Author |
|------|--------|--------|
| 2026-02-20 | Initial draft — full ops pipeline | Moto |
| 2026-02-20 | Added monitoring, security, versioning, CI/CD, CAB, rollback testing, deps, AI automation | Moto |
