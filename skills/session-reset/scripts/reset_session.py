#!/usr/bin/env python3
"""
reset_session.py - Reset an OpenClaw agent session by channel key.

Usage:
  python3 reset_session.py <sessions_json> <session_key>
  python3 reset_session.py <sessions_json> --list

Examples:
  python3 reset_session.py ~/.openclaw/agents/main/sessions/sessions.json --list
  python3 reset_session.py ~/.openclaw/agents/main/sessions/sessions.json "agent:main:discord:channel:1475994576668852254"
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime, timezone


def load_sessions(sessions_json: Path) -> dict:
    with open(sessions_json) as f:
        return json.load(f)


def list_sessions(sessions: dict):
    print("Active sessions:")
    for key, data in sessions.items():
        session_id = data.get("sessionId", "unknown")
        session_file = data.get("sessionFile", "")
        exists = "✓" if session_file and Path(session_file).exists() else "✗"
        print(f"  [{exists}] {key}")
        print(f"        session: {session_id}")


def reset_session(sessions_json: Path, session_key: str):
    sessions = load_sessions(sessions_json)

    if session_key not in sessions:
        print(f"ERROR: Session key not found: {session_key}")
        print("Run with --list to see available sessions.")
        sys.exit(1)

    session_data = sessions[session_key]
    session_file = session_data.get("sessionFile", "")

    if not session_file:
        print(f"ERROR: No sessionFile found for key: {session_key}")
        sys.exit(1)

    session_path = Path(session_file)

    # Delete the session file (mark as deleted with timestamp, same as OpenClaw's pattern)
    if session_path.exists():
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%S.000Z")
        deleted_path = session_path.with_suffix(f".jsonl.deleted.{ts}")
        session_path.rename(deleted_path)
        print(f"Session file archived: {deleted_path.name}")
    else:
        print(f"Session file already missing: {session_path.name}")

    # Remove the entry from sessions.json so next prompt creates a fresh session
    del sessions[session_key]
    with open(sessions_json, "w") as f:
        json.dump(sessions, f, indent=4)

    print(f"Session reset complete: {session_key}")
    print("Next prompt on this channel will start a fresh session.")


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    sessions_json = Path(sys.argv[1])
    if not sessions_json.exists():
        print(f"ERROR: sessions.json not found at: {sessions_json}")
        sys.exit(1)

    arg = sys.argv[2]

    if arg == "--list":
        sessions = load_sessions(sessions_json)
        list_sessions(sessions)
    else:
        reset_session(sessions_json, arg)


if __name__ == "__main__":
    main()
