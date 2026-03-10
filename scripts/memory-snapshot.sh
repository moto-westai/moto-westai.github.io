#!/bin/bash
# memory-snapshot.sh — Daily identity git snapshot for Moto
# Versions identity/memory files to detect and prevent drift over time.
# Called by cron (5 AM CST daily) and manually for freeze snapshots.

set -euo pipefail

WORKSPACE="/home/jlwestsr/.openclaw/workspace"
DATE=$(date +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
MODE="${1:-daily}"  # daily | weekly | freeze

cd "$WORKSPACE"

# Stage identity + memory files
git add \
  SOUL.md \
  AGENTS.md \
  MEMORY.md \
  HEARTBEAT.md \
  IDENTITY.md \
  TOOLS.md \
  USER.md \
  memory/ \
  skills/ \
  2>/dev/null || true

# Check if anything changed
CHANGES=$(git diff --cached --stat 2>/dev/null | tail -1)

if [ -z "$CHANGES" ]; then
  echo "[${TIMESTAMP}] Identity stable — no drift detected since last checkpoint."
  exit 0
fi

case "$MODE" in
  daily)
    MSG="snapshot: daily identity checkpoint ${DATE}"
    ;;
  weekly)
    MSG="snapshot: weekly identity review ${DATE}"
    ;;
  freeze)
    FREEZE_NAME="${2:-unnamed}"
    MSG="freeze(moto-${FREEZE_NAME}): identity snapshot approved by Jason L. West Sr."
    ;;
  *)
    MSG="snapshot: manual checkpoint ${DATE}"
    ;;
esac

git commit -m "$MSG"

if [ "$MODE" = "freeze" ]; then
  TAG="identity/moto-${2:-$(date +%Y%m%d)}"
  git tag "$TAG"
  echo "[${TIMESTAMP}] FREEZE SNAPSHOT created: ${TAG}"
  echo "Commit: $(git rev-parse HEAD)"
else
  echo "[${TIMESTAMP}] Snapshot committed: ${CHANGES}"
fi

# Push to Gitea (off-machine backup)
if source /home/jlwestsr/.openclaw/secrets/gitea.env 2>/dev/null; then
  git push gitea master --tags --quiet 2>/dev/null && echo "[${TIMESTAMP}] Pushed to Gitea." || echo "[${TIMESTAMP}] Gitea push failed (non-fatal)."
fi
