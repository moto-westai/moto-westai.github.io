#!/usr/bin/env bash
# Mac Mini — Sibling AI Setup Script (Gemini 3.1 OAuth edition)
# Run FROM shurtugal-lnx as jlwestsr
# Wipes Mac Mini workspace and installs seed files for a fresh AI identity
# Primary model: google-gemini-cli/gemini-3.1-pro (OAuth — no API key needed)
# Date: 2026-02-21
#
# BEFORE RUNNING:
#   SSH to Mac Mini and run: openclaw configure
#   Choose: Google → "Google Gemini CLI OAuth"
#   Sign in with Google account that has Ultra access
#   Then run this script.

set -e

MAC_MINI="moto@nebulus"
SSH_KEY="$HOME/.ssh/id_ed25519_moto"
SEED_DIR="$HOME/.openclaw/workspace/west_ai_labs/docs/plans/new-ai-seed"
REMOTE_WORKSPACE="/Users/moto/.openclaw/workspace"
REMOTE_CONFIG="/Users/moto/.openclaw/openclaw.json"

echo "=== Mac Mini Sibling AI Setup (Gemini 3.1) ==="
echo ""

# Step 1: Verify Mac Mini is reachable
echo "[1/7] Checking Mac Mini connectivity..."
ssh -i "$SSH_KEY" "$MAC_MINI" "echo connected && hostname && date" || {
    echo "ERROR: Cannot reach Mac Mini. Check SSH."
    exit 1
}

# Step 2: Backup current workspace
echo ""
echo "[2/7] Backing up current Mac Mini workspace..."
BACKUP_NAME="workspace-backup-$(date +%Y%m%d-%H%M%S)"
ssh -i "$SSH_KEY" "$MAC_MINI" "
    cd /Users/moto/.openclaw
    tar czf ~/${BACKUP_NAME}.tar.gz workspace/ 2>/dev/null && echo 'Backup: ~/${BACKUP_NAME}.tar.gz' || echo 'Nothing to backup (ok)'
"

# Step 3: Wipe workspace
echo ""
echo "[3/7] Wiping Mac Mini workspace..."
ssh -i "$SSH_KEY" "$MAC_MINI" "
    rm -rf '$REMOTE_WORKSPACE'
    mkdir -p '$REMOTE_WORKSPACE/memory'
    echo 'Workspace wiped and recreated.'
"

# Step 4: Copy seed files
echo ""
echo "[4/7] Installing seed files..."
scp -i "$SSH_KEY" "$SEED_DIR/SOUL.md"   "$MAC_MINI:$REMOTE_WORKSPACE/SOUL.md"
scp -i "$SSH_KEY" "$SEED_DIR/USER.md"   "$MAC_MINI:$REMOTE_WORKSPACE/USER.md"
scp -i "$SSH_KEY" "$SEED_DIR/AGENTS.md" "$MAC_MINI:$REMOTE_WORKSPACE/AGENTS.md"
echo "Seed files installed: SOUL.md, USER.md, AGENTS.md"

# Step 5: Update openclaw.json for Gemini 3.1 OAuth
echo ""
echo "[5/6] Configuring Mac Mini for Gemini 3.1 (OAuth)..."
ssh -i "$SSH_KEY" "$MAC_MINI" "python3 << 'PYEOF'
import json

with open('/Users/moto/.openclaw/openclaw.json', 'r') as f:
    cfg = json.load(f)

# Set primary model to Gemini 3.1
cfg.setdefault('agents', {}).setdefault('defaults', {})['model'] = {
    'primary': 'google-gemini-cli/gemini-3.1-pro'
}
cfg['agents']['defaults']['models'] = {
    'google-gemini-cli/gemini-3.1-pro': {},
    'google-gemini-cli/gemini-3-pro': {}
}
cfg['agents']['defaults']['workspace'] = '/Users/moto/.openclaw/workspace'

# Set OAuth auth profile for Google Gemini CLI
cfg.setdefault('auth', {}).setdefault('profiles', {})['google-gemini-cli:default'] = {
    'provider': 'google-gemini-cli',
    'mode': 'oauth'
}
# Remove Anthropic as default if present
cfg['auth']['profiles'].pop('anthropic:default', None)

with open('/Users/moto/.openclaw/openclaw.json', 'w') as f:
    json.dump(cfg, f, indent=2)

print('openclaw.json updated for Gemini 3.1 OAuth')
PYEOF
"

# Step 6: Restart Mac Mini gateway
echo ""
echo "[6/6] Restarting Mac Mini gateway..."
ssh -i "$SSH_KEY" "$MAC_MINI" "
    sudo launchctl unload /Library/LaunchDaemons/com.westailabs.openclaw.plist 2>/dev/null || true
    sleep 3
    sudo launchctl load /Library/LaunchDaemons/com.westailabs.openclaw.plist 2>/dev/null && echo 'Gateway restarted via launchd' || {
        cd /Users/moto/.openclaw
        pkill -f openclaw-gateway 2>/dev/null || true
        sleep 2
        nohup openclaw-gateway > logs/gateway.log 2>&1 &
        echo 'Gateway started manually'
    }
    sleep 5
    echo 'Done.'
"

echo ""
echo "=== SETUP COMPLETE ==="
echo ""
echo "Model: google-gemini-cli/gemini-3.1-pro (OAuth)"
echo "Backup: ~/${BACKUP_NAME}.tar.gz on Mac Mini"
echo ""
echo "Next steps:"
echo "1. Add Telegram config to Mac Mini (see cutover runbook)"
echo "2. Open Telegram on your phone"
echo "3. Say hello — new AI starts fresh, no identity yet"
echo ""
echo "Rollback: ssh -i $SSH_KEY $MAC_MINI 'tar xzf ~/${BACKUP_NAME}.tar.gz -C /Users/moto/.openclaw/'"
