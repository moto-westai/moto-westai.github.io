# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## TTS / Voice

- **Engine:** ElevenLabs (Creator/Pro tier, 110K chars/month)
- **CLI:** `sag` (brew: steipete/tap/sag)
- **Moto's voice:** Charlie — Deep, Confident, Energetic (ID: `IKne3meq5aSn9XLyUdCD`)
- **Key env:** `ELEVENLABS_API_KEY` in `~/.openclaw/openclaw.env`
- **Usage:** `sag speak -v "Charlie" -o /tmp/output.mp3 "text"`

## Neo4j Knowledge Graph

- **Browser UI:** http://192.168.4.208:7474 (also localhost:7474)
- **Bolt:** bolt://localhost:7687
- **Credentials:** neo4j / WestAILabs2026! (also in `/home/jlwestsr/.openclaw/secrets/neo4j.env`)
- **Docker:** `cd /home/jlwestsr/neo4j && docker compose up -d`
- **Ingest/rebuild:** `python3 scripts/ingest-memory-graph.py`
- **Query mid-session:**
  ```bash
  python3 scripts/query-graph.py topic <keyword>
  python3 scripts/query-graph.py category <cat>
  python3 scripts/query-graph.py high-salience
  python3 scripts/query-graph.py related <rec-id>
  python3 scripts/query-graph.py stats
  python3 scripts/query-graph.py cypher "MATCH (m:MemoryRecord) RETURN m LIMIT 5"
  ```
- **Nodes:** MemoryRecord (35), Concept (152), Infrastructure (7), Agent (1)
- **Edges:** HAS_MEMORY, LINKS_TO, RELATED, RUNS_ON

## Gitea Git Server

- **Web UI:** http://192.168.4.208:3001
- **Org:** westailabs
- **Repos:** westailabs/moto-workspace, westailabs/cael-workspace
- **Credentials:** moto / WestAILabs2026! (token in `/home/jlwestsr/.openclaw/secrets/gitea.env`)
- **Docker:** `cd /home/jlwestsr/gitea && docker compose up -d`
- **Moto remote:** `git remote add gitea http://moto:<token>@localhost:3001/westailabs/moto-workspace.git`

## Examples

```markdown
### Cameras

- (none configured yet)

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: Charlie (deep, confident, energetic)
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
