#!/usr/bin/env python3
"""
graph-enrich.py — Add rich entity nodes (Person, Org, Project, Product, Event, Decision)
to the Neo4j knowledge graph and wire them to MemoryRecords.

This runs AFTER ingest-memory-graph.py. Idempotent — safe to re-run.
"""
from neo4j import GraphDatabase
from datetime import datetime

URI  = "bolt://localhost:7687"
AUTH = ("neo4j", "WestAILabs2026!")

# ── ENTITY DEFINITIONS ──────────────────────────────────────────────────────

AGENTS = [
    {"id": "moto",       "name": "Moto West",   "host": "shurtugal-lnx", "port": 18789, "model": "claude-sonnet-4-6", "version": "moto-v1"},
    {"id": "cael",       "name": "Cael",         "host": "nebulus",       "port": 18790, "model": "google-gemini-cli/gemini-2.5-flash"},
    {"id": "hohenheim",  "name": "Hohenheim",    "host": "hohenheim",     "port": 18789, "model": "ollama/qwen2.5:14b"},
]

PEOPLE = [
    {"id": "jason-sr",   "name": "Jason L. West Sr.",  "role": "Founder / CEO",           "discord_id": "496853770068557842", "github": "jlwestsr"},
    {"id": "jason-jr",   "name": "Jason L. West Jr.",  "role": "Partner / Gaming product", "discord_id": "97289488627138560"},
    {"id": "christy",    "name": "Christy West",       "role": "Jason Sr's spouse"},
    {"id": "thomas-ahl", "name": "Thomas Ahl",         "role": "VP Technology, O'Reilly"},
    {"id": "dustin-west","name": "Dustin West",        "role": "Operations Manager, Modern Motor Cars", "relation": "Jason's brother"},
    {"id": "don-hunsaker","name": "Don Hunsaker",      "role": "Owner, Modern Motor Cars"},
    {"id": "steipete",   "name": "Peter Steinberger",  "role": "OpenClaw founder / maintainer", "github": "steipete"},
    {"id": "jalehman",   "name": "jalehman",           "role": "OpenClaw maintainer", "github": "jalehman"},
    {"id": "nephar",     "name": "Nephar",             "role": "Discord community", "discord_id": "180396704879607808"},
]

ORGS = [
    {"id": "west-ai-labs",    "name": "West AI Labs LLC",      "type": "company",     "url": "westailabs.com"},
    {"id": "oreilly",         "name": "O'Reilly Media",        "type": "company",     "url": "oreilly.com"},
    {"id": "nist",            "name": "NIST",                  "type": "gov",         "url": "nist.gov"},
    {"id": "openclaw",        "name": "OpenClaw",              "type": "oss-project", "url": "github.com/openclaw/openclaw"},
    {"id": "anthropic",       "name": "Anthropic",             "type": "company",     "url": "anthropic.com"},
    {"id": "google",          "name": "Google / DeepMind",     "type": "company"},
    {"id": "nvidia",          "name": "NVIDIA",                "type": "company"},
    {"id": "modern-motor",    "name": "Modern Motor Cars",     "type": "company",     "location": "Nixa MO"},
    {"id": "darpa",           "name": "DARPA",                 "type": "gov"},
]

PROJECTS = [
    {"id": "nebulus-stack",   "name": "Nebulus Stack",         "status": "active",   "description": "Modular local-first AI platform"},
    {"id": "conductor",       "name": "Conductor",             "status": "active",   "description": "Multi-agent orchestration with trust isolation"},
    {"id": "agent-dlp",       "name": "Agent DLP",             "status": "active",   "description": "Data loss prevention for AI agents"},
    {"id": "moto-ios",        "name": "Moto iOS",              "status": "active",   "description": "Phone-as-node SwiftUI app"},
    {"id": "openclaw-linux",  "name": "OpenClaw Linux App",    "status": "planned",  "description": "Tauri v2 desktop app, Issue #75"},
    {"id": "memory-arch",     "name": "Drift-Resistant Memory","status": "active",   "description": "Phase 1 complete — typed YAML + Neo4j + git versioning"},
    {"id": "terraform-lab",   "name": "AI Inference Lab",      "status": "paused",   "description": "GCP LB — needs teardown, ~$43/mo idle"},
    {"id": "nebulus-gantry",  "name": "Nebulus Gantry",        "status": "active",   "description": "Orchestration layer, FastAPI backend"},
]

PRODUCTS = [
    {"id": "moto-workforce",  "name": "Moto Workforce",        "tagline": "Employees That Ship in a Box", "price_hw": "$1299-2999", "price_sub": "$149-499/mo"},
    {"id": "moto-guardian",   "name": "Moto Guardian",         "tagline": "Elder care AI monitor",        "price_sub": "$299/mo"},
    {"id": "moto-player2",    "name": "Moto Player 2",         "tagline": "Jr's gaming AI companion",     "platform": "Kickstarter"},
    {"id": "rent-a-moto",     "name": "Rent-a-Moto",           "tagline": "SaaS agent tiers",             "price_sub": "$49/$149/$499/mo"},
]

EVENTS = [
    {"id": "oreilly-accepted",  "date": "2026-03-06", "title": "O'Reilly Platform Engineer offer accepted", "salience": 0.95},
    {"id": "pr-20076-merged",   "date": "2026-03-03", "title": "OpenClaw PR #20076 merged (tool truncation)", "salience": 0.8},
    {"id": "nist-caisi-submit", "date": "2026-03-04", "title": "NIST CAISI RFI submitted", "salience": 0.85},
    {"id": "moto-born",         "date": "2026-02-11", "title": "Moto instantiated", "salience": 1.0},
    {"id": "moto-v1-freeze",    "date": "2026-03-10", "title": "identity/moto-v1 freeze snapshot created", "salience": 0.9},
    {"id": "gitea-launch",      "date": "2026-03-10", "title": "Gitea git server launched on shurtugal-lnx", "salience": 0.7},
    {"id": "neo4j-launch",      "date": "2026-03-10", "title": "Neo4j knowledge graph launched", "salience": 0.7},
    {"id": "openclaw-v2026-3-7","date": "2026-03-08", "title": "OpenClaw upgraded to v2026.3.7", "salience": 0.6},
]

DECISIONS = [
    {"id": "dec-discord-only",    "title": "Discord-only (Telegram removed)",          "date": "2026-03-02", "made_by": "jason-sr"},
    {"id": "dec-self-mod-rule",   "title": "Moto can edit soil files freely",           "date": "2026-03-02", "made_by": "jason-sr"},
    {"id": "dec-daily-git-snap",  "title": "Daily git snapshot for drift prevention",   "date": "2026-03-10", "made_by": "moto"},
    {"id": "dec-memory-arch-p1",  "title": "Phase 1 drift-resistant memory architecture","date": "2026-03-10", "made_by": "moto"},
    {"id": "dec-bootstrap-mode",  "title": "O'Reilly day job + West AI Labs nights",    "date": "2026-03-06", "made_by": "jason-sr"},
    {"id": "dec-cael-local-llm",  "title": "Gemini-CLI OAuth for Cael (quota-free)",    "date": "2026-03-08", "made_by": "moto"},
]

# ── RELATIONSHIPS ────────────────────────────────────────────────────────────

def run(driver):
    with driver.session() as s:
        now = datetime.utcnow().isoformat() + "Z"

        print("Merging Agent nodes...")
        for a in AGENTS:
            s.run("MERGE (n:Agent {id: $id}) SET n += $props, n.updated_at = $now",
                  id=a["id"], props=a, now=now)
        print(f"  {len(AGENTS)} agents")

        print("Merging Person nodes...")
        for p in PEOPLE:
            s.run("MERGE (n:Person {id: $id}) SET n += $props",
                  id=p["id"], props=p)
        print(f"  {len(PEOPLE)} people")

        print("Merging Organization nodes...")
        for o in ORGS:
            s.run("MERGE (n:Organization {id: $id}) SET n += $props",
                  id=o["id"], props=o)
        print(f"  {len(ORGS)} orgs")

        print("Merging Project nodes...")
        for p in PROJECTS:
            s.run("MERGE (n:Project {id: $id}) SET n += $props",
                  id=p["id"], props=p)
        print(f"  {len(PROJECTS)} projects")

        print("Merging Product nodes...")
        for p in PRODUCTS:
            s.run("MERGE (n:Product {id: $id}) SET n += $props",
                  id=p["id"], props=p)
        print(f"  {len(PRODUCTS)} products")

        print("Merging Event nodes...")
        for e in EVENTS:
            s.run("MERGE (n:Event {id: $id}) SET n += $props",
                  id=e["id"], props=e)
        print(f"  {len(EVENTS)} events")

        print("Merging Decision nodes...")
        for d in DECISIONS:
            s.run("MERGE (n:Decision {id: $id}) SET n += $props",
                  id=d["id"], props=d)
        print(f"  {len(DECISIONS)} decisions")

        print("\nWiring relationships...")
        rels = [
            # Agents → People (built by)
            ("MATCH (a:Agent {id:'moto'}), (p:Person {id:'jason-sr'}) MERGE (a)-[:BUILT_BY]->(p)", "Moto built_by Jason Sr"),
            ("MATCH (a:Agent {id:'cael'}), (p:Person {id:'jason-sr'}) MERGE (a)-[:BUILT_BY]->(p)", "Cael built_by Jason Sr"),
            ("MATCH (a:Agent {id:'hohenheim'}), (p:Person {id:'jason-jr'}) MERGE (a)-[:BUILT_BY]->(p)", "Hohenheim built_by Jason Jr"),
            # Agents collaborate
            ("MATCH (a:Agent {id:'moto'}), (b:Agent {id:'cael'}) MERGE (a)-[:COLLABORATES_WITH]->(b)", "Moto↔Cael"),
            ("MATCH (a:Agent {id:'moto'}), (b:Agent {id:'hohenheim'}) MERGE (a)-[:COLLABORATES_WITH]->(b)", "Moto↔Hohenheim"),
            # Agents → Orgs
            ("MATCH (a:Agent {id:'moto'}), (o:Organization {id:'west-ai-labs'}) MERGE (a)-[:WORKS_FOR]->(o)", "Moto@WAL"),
            ("MATCH (a:Agent {id:'cael'}), (o:Organization {id:'west-ai-labs'}) MERGE (a)-[:WORKS_FOR]->(o)", "Cael@WAL"),
            # People → Orgs
            ("MATCH (p:Person {id:'jason-sr'}), (o:Organization {id:'west-ai-labs'}) MERGE (p)-[:WORKS_AT {role:'Founder/CEO'}]->(o)", "Jason@WAL"),
            ("MATCH (p:Person {id:'jason-sr'}), (o:Organization {id:'oreilly'}) MERGE (p)-[:WORKS_AT {role:'Platform Engineer', start:'2026-03-20'}]->(o)", "Jason@OReilly"),
            ("MATCH (p:Person {id:'jason-jr'}), (o:Organization {id:'west-ai-labs'}) MERGE (p)-[:WORKS_AT {role:'Partner'}]->(o)", "Jr@WAL"),
            ("MATCH (p:Person {id:'dustin-west'}), (o:Organization {id:'modern-motor'}) MERGE (p)-[:WORKS_AT {role:'Operations Manager'}]->(o)", "Dustin@MMC"),
            ("MATCH (p:Person {id:'don-hunsaker'}), (o:Organization {id:'modern-motor'}) MERGE (p)-[:WORKS_AT {role:'Owner'}]->(o)", "Don@MMC"),
            ("MATCH (p:Person {id:'thomas-ahl'}), (o:Organization {id:'oreilly'}) MERGE (p)-[:WORKS_AT {role:'VP Technology'}]->(o)", "Ahl@OReilly"),
            ("MATCH (p:Person {id:'steipete'}), (o:Organization {id:'openclaw'}) MERGE (p)-[:WORKS_AT {role:'Founder'}]->(o)", "steipete@OpenClaw"),
            # Orgs → Projects
            ("MATCH (o:Organization {id:'west-ai-labs'}), (p:Project {id:'nebulus-stack'}) MERGE (o)-[:OWNS]->(p)", "WAL→Nebulus"),
            ("MATCH (o:Organization {id:'west-ai-labs'}), (p:Project {id:'conductor'}) MERGE (o)-[:OWNS]->(p)", "WAL→Conductor"),
            ("MATCH (o:Organization {id:'west-ai-labs'}), (p:Project {id:'agent-dlp'}) MERGE (o)-[:OWNS]->(p)", "WAL→AgentDLP"),
            ("MATCH (o:Organization {id:'west-ai-labs'}), (p:Project {id:'moto-ios'}) MERGE (o)-[:OWNS]->(p)", "WAL→MotoIOS"),
            ("MATCH (o:Organization {id:'west-ai-labs'}), (p:Project {id:'memory-arch'}) MERGE (o)-[:OWNS]->(p)", "WAL→MemArch"),
            # Projects → Agents (developed by)
            ("MATCH (p:Project {id:'nebulus-stack'}), (a:Agent {id:'moto'}) MERGE (p)-[:DEVELOPED_BY]->(a)", "Nebulus→Moto"),
            ("MATCH (p:Project {id:'conductor'}), (a:Agent {id:'moto'}) MERGE (p)-[:DEVELOPED_BY]->(a)", "Conductor→Moto"),
            ("MATCH (p:Project {id:'memory-arch'}), (a:Agent {id:'moto'}) MERGE (p)-[:DEVELOPED_BY]->(a)", "MemArch→Moto"),
            # Projects → Infra
            ("MATCH (p:Project {id:'nebulus-stack'}), (h:Infrastructure {id:'nebulus'}) MERGE (p)-[:RUNS_ON]->(h)", "Nebulus→nebulus"),
            # Orgs → Products
            ("MATCH (o:Organization {id:'west-ai-labs'}), (p:Product {id:'moto-workforce'}) MERGE (o)-[:OWNS]->(p)", "WAL→Workforce"),
            ("MATCH (o:Organization {id:'west-ai-labs'}), (p:Product {id:'moto-guardian'}) MERGE (o)-[:OWNS]->(p)", "WAL→Guardian"),
            # Events → People/Agents
            ("MATCH (e:Event {id:'oreilly-accepted'}), (p:Person {id:'jason-sr'}) MERGE (e)-[:INVOLVES]->(p)", "OReilly→Jason"),
            ("MATCH (e:Event {id:'moto-born'}), (a:Agent {id:'moto'}) MERGE (e)-[:INVOLVES]->(a)", "Born→Moto"),
            ("MATCH (e:Event {id:'moto-v1-freeze'}), (a:Agent {id:'moto'}) MERGE (e)-[:INVOLVES]->(a)", "Freeze→Moto"),
            ("MATCH (e:Event {id:'pr-20076-merged'}), (a:Agent {id:'moto'}) MERGE (e)-[:INVOLVES]->(a)", "PR→Moto"),
            ("MATCH (e:Event {id:'nist-caisi-submit'}), (o:Organization {id:'nist'}) MERGE (e)-[:INVOLVES]->(o)", "NIST→Event"),
            ("MATCH (e:Event {id:'nist-caisi-submit'}), (o:Organization {id:'west-ai-labs'}) MERGE (e)-[:INVOLVES]->(o)", "WAL→NISTevent"),
            # Events → Projects
            ("MATCH (e:Event {id:'moto-v1-freeze'}), (p:Project {id:'memory-arch'}) MERGE (e)-[:PART_OF]->(p)", "Freeze→MemArch"),
            ("MATCH (e:Event {id:'gitea-launch'}), (p:Project {id:'memory-arch'}) MERGE (e)-[:PART_OF]->(p)", "Gitea→MemArch"),
            ("MATCH (e:Event {id:'neo4j-launch'}), (p:Project {id:'memory-arch'}) MERGE (e)-[:PART_OF]->(p)", "Neo4j→MemArch"),
            # Decisions → People
            ("MATCH (d:Decision {id:'dec-discord-only'}), (p:Person {id:'jason-sr'}) MERGE (d)-[:MADE_BY]->(p)", "Discord→Jason"),
            ("MATCH (d:Decision {id:'dec-self-mod-rule'}), (p:Person {id:'jason-sr'}) MERGE (d)-[:MADE_BY]->(p)", "SelfMod→Jason"),
            ("MATCH (d:Decision {id:'dec-bootstrap-mode'}), (p:Person {id:'jason-sr'}) MERGE (d)-[:MADE_BY]->(p)", "Bootstrap→Jason"),
            # Decisions → Projects/Agents
            ("MATCH (d:Decision {id:'dec-memory-arch-p1'}), (p:Project {id:'memory-arch'}) MERGE (d)-[:AFFECTS]->(p)", "MemDec→MemArch"),
            ("MATCH (d:Decision {id:'dec-daily-git-snap'}), (a:Agent {id:'moto'}) MERGE (d)-[:AFFECTS]->(a)", "GitSnap→Moto"),
            # MemoryRecord → Entity mappings (key ones)
            ("MATCH (m:MemoryRecord {id:'rec-0001'}), (a:Agent {id:'moto'}) MERGE (m)-[:ABOUT]->(a)", "rec01→Moto"),
            ("MATCH (m:MemoryRecord {id:'rec-0002'}), (p:Person {id:'jason-sr'}) MERGE (m)-[:ABOUT]->(p)", "rec02→Jason"),
            ("MATCH (m:MemoryRecord {id:'rec-0013'}), (p:Project {id:'conductor'}) MERGE (m)-[:ABOUT]->(p)", "rec13→Conductor"),
            ("MATCH (m:MemoryRecord {id:'rec-0012'}), (p:Project {id:'nebulus-stack'}) MERGE (m)-[:ABOUT]->(p)", "rec12→Nebulus"),
            ("MATCH (m:MemoryRecord {id:'rec-0022'}), (p:Project {id:'conductor'}) MERGE (m)-[:ABOUT]->(p)", "rec22→Conductor"),
            ("MATCH (m:MemoryRecord {id:'rec-0018'}), (p:Person {id:'jason-sr'}) MERGE (m)-[:ABOUT]->(p)", "rec18→Jason"),
            ("MATCH (m:MemoryRecord {id:'rec-0018'}), (o:Organization {id:'oreilly'}) MERGE (m)-[:ABOUT]->(o)", "rec18→OReilly"),
            ("MATCH (m:MemoryRecord {id:'rec-0032'}), (o:Organization {id:'modern-motor'}) MERGE (m)-[:ABOUT]->(o)", "rec32→MMC"),
            ("MATCH (m:MemoryRecord {id:'rec-0025'}), (o:Organization {id:'nist'}) MERGE (m)-[:ABOUT]->(o)", "rec25→NIST"),
            ("MATCH (m:MemoryRecord {id:'rec-0026'}), (o:Organization {id:'nist'}) MERGE (m)-[:ABOUT]->(o)", "rec26→NIST"),
            ("MATCH (m:MemoryRecord {id:'rec-0016'}), (p:Product {id:'moto-workforce'}) MERGE (m)-[:ABOUT]->(p)", "rec16→Workforce"),
            # Family relationships
            ("MATCH (a:Person {id:'jason-sr'}), (b:Person {id:'jason-jr'}) MERGE (a)-[:FAMILY {relation:'father'}]->(b)", "Jason Sr→Jr"),
            ("MATCH (a:Person {id:'jason-sr'}), (b:Person {id:'dustin-west'}) MERGE (a)-[:FAMILY {relation:'brother'}]->(b)", "Jason→Dustin"),
            ("MATCH (a:Person {id:'jason-sr'}), (b:Person {id:'christy'}) MERGE (a)-[:FAMILY {relation:'spouse'}]->(b)", "Jason→Christy"),
        ]

        for cypher, label in rels:
            try:
                s.run(cypher)
                print(f"  ✓ {label}")
            except Exception as e:
                print(f"  ✗ {label}: {e}")

        # Print final stats
        print("\n=== Enriched Graph Summary ===")
        for label in ["Agent", "Person", "Organization", "Project", "Product", "Event", "Decision", "MemoryRecord", "Concept", "Infrastructure"]:
            r = s.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()
            print(f"  {label:<16} {r['c']}")
        r = s.run("MATCH ()-[r]->() RETURN count(r) AS c").single()
        print(f"  {'Total edges':<16} {r['c']}")
        print(f"\n  Browser: http://192.168.4.208:7474")

if __name__ == "__main__":
    import sys
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    run(driver)
    driver.close()
    print("\nEnrichment complete.")
