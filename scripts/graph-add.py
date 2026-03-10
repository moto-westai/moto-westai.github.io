#!/usr/bin/env python3
"""
graph-add.py — Add a new memory record to YAML + Neo4j in one shot.

Usage:
  python3 graph-add.py \
    --title "Short descriptive title" \
    --category fact|decision|relationship|infrastructure|project|job|security|business \
    --content "The memory content" \
    --concepts "tag1,tag2,tag3" \
    --salience 0.7 \
    [--decay normal|slow|permanent|fast] \
    [--hint preserve|summarize|ephemeral] \
    [--subcategory "optional"]

Salience guide:
  1.0 identity-critical  0.8 active decisions  0.6 historical
  0.9 critical infra     0.7 career/business   0.4 nice-to-know
"""
import argparse
import os
import sys
import glob
import yaml
from datetime import datetime, timezone
from neo4j import GraphDatabase

RECORDS_DIR = "/home/jlwestsr/.openclaw/workspace/memory/long-term"
INDEX_FILE  = f"{RECORDS_DIR}/INDEX.yaml"
NEO4J_URI   = "bolt://localhost:7687"
NEO4J_AUTH  = ("neo4j", "WestAILabs2026!")

def next_id():
    existing = sorted(glob.glob(f"{RECORDS_DIR}/rec-*.yaml"))
    if not existing:
        return "rec-0001"
    last = os.path.basename(existing[-1])
    num = int(last.split("-")[1]) + 1
    return f"rec-{num:04d}"

def next_filename(rec_id, title):
    slug = title.lower()
    for ch in " /\\:()[]{}|<>":
        slug = slug.replace(ch, "-")
    slug = "-".join(p for p in slug.split("-") if p)[:40]
    return f"{rec_id}-{slug}.yaml"

def write_yaml(rec):
    fname = next_filename(rec["id"], rec["title"])
    path  = f"{RECORDS_DIR}/{fname}"
    with open(path, "w") as f:
        yaml.dump(rec, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    return path, fname

def update_index(rec, fname):
    if os.path.exists(INDEX_FILE):
        with open(INDEX_FILE) as f:
            index = yaml.safe_load(f)
    else:
        index = {"generated_at": "", "total_records": 0, "agent_id": "moto", "records": []}

    index["records"].append({
        "id":              rec["id"],
        "file":            fname,
        "title":           rec["title"],
        "category":        rec["category"],
        "salience":        rec["salience"],
        "compaction_hint": rec["compaction_hint"],
    })
    index["total_records"] = len(index["records"])
    index["generated_at"]  = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    with open(INDEX_FILE, "w") as f:
        yaml.dump(index, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def write_neo4j(rec):
    driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
    with driver.session() as s:
        content = str(rec.get("content", ""))[:2000]
        concepts = rec.get("linked_concepts", []) or []

        s.run("""
            MERGE (m:MemoryRecord {id: $id})
            SET m.title           = $title,
                m.category        = $category,
                m.subcategory     = $subcategory,
                m.content         = $content,
                m.salience        = $salience,
                m.decay_class     = $decay_class,
                m.compaction_hint = $compaction_hint,
                m.source          = $source,
                m.created_at      = $created_at
            WITH m
            MATCH (a:Agent {id: 'moto'})
            MERGE (a)-[:HAS_MEMORY]->(m)
        """, id=rec["id"], title=rec["title"], category=rec["category"],
             subcategory=rec.get("subcategory",""), content=content,
             salience=rec["salience"], decay_class=rec["decay_class"],
             compaction_hint=rec["compaction_hint"],
             source=rec.get("source",""), created_at=rec["created_at"])

        for concept in concepts:
            cid = concept.strip().lower().replace(" ", "_")
            s.run("""
                MERGE (c:Concept {id: $cid}) SET c.name = $name
                WITH c MATCH (m:MemoryRecord {id: $mid})
                MERGE (m)-[:LINKS_TO]->(c)
            """, cid=cid, name=concept.strip(), mid=rec["id"])

        # Rebuild RELATED edges for this record
        s.run("""
            MATCH (m:MemoryRecord {id: $id})-[:LINKS_TO]->(c:Concept)<-[:LINKS_TO]-(r:MemoryRecord)
            WHERE m.id <> r.id
            MERGE (m)-[:RELATED {via: c.name}]->(r)
        """, id=rec["id"])

    driver.close()

def main():
    p = argparse.ArgumentParser(description="Add a memory record to YAML + Neo4j")
    p.add_argument("--title",      required=True)
    p.add_argument("--category",   required=True,
                   choices=["fact","decision","relationship","infrastructure",
                            "project","job","security","business"])
    p.add_argument("--content",    required=True)
    p.add_argument("--concepts",   default="",
                   help="Comma-separated concept tags")
    p.add_argument("--salience",   type=float, default=0.7)
    p.add_argument("--decay",      default="normal",
                   choices=["permanent","slow","normal","fast"])
    p.add_argument("--hint",       default="summarize",
                   choices=["preserve","summarize","ephemeral"])
    p.add_argument("--subcategory",default="")
    args = p.parse_args()

    now     = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    rec_id  = next_id()
    concepts = [c.strip() for c in args.concepts.split(",") if c.strip()]

    rec = {
        "id":               rec_id,
        "created_at":       now,
        "category":         args.category,
        "subcategory":      args.subcategory,
        "title":            args.title,
        "content":          args.content,
        "linked_concepts":  concepts,
        "salience":         args.salience,
        "decay_class":      args.decay,
        "compaction_hint":  args.hint,
        "last_reinforced":  now,
        "source":           f"graph-add {now}",
    }

    print(f"Creating {rec_id}: {args.title}")

    path, fname = write_yaml(rec)
    print(f"  ✓ YAML: {path}")

    update_index(rec, fname)
    print(f"  ✓ INDEX updated")

    try:
        write_neo4j(rec)
        print(f"  ✓ Neo4j node created + RELATED edges rebuilt")
    except Exception as e:
        print(f"  ⚠ Neo4j: {e} (YAML still saved)")

    print(f"\nDone. Salience: {args.salience} | Hint: {args.hint} | Concepts: {concepts}")

if __name__ == "__main__":
    main()
