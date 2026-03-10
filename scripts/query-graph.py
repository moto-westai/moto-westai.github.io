#!/usr/bin/env python3
"""
query-graph.py — Query Moto's Neo4j knowledge graph mid-session.

Usage:
  python3 query-graph.py topic <keyword>        # Find records related to a topic
  python3 query-graph.py related <record_id>    # Find records related to a given record
  python3 query-graph.py category <cat>         # All records in a category
  python3 query-graph.py high-salience [N]      # Top N records by salience (default 10)
  python3 query-graph.py path <id1> <id2>       # Shortest path between two records
  python3 query-graph.py cypher "<query>"       # Raw Cypher query (returns JSON)
  python3 query-graph.py stats                  # Graph statistics
"""

import sys
import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "WestAILabs2026!")

def driver():
    return GraphDatabase.driver(URI, auth=AUTH)

def fmt_record(r):
    sal = r.get("salience", 0)
    bar = "█" * int(sal * 10) + "░" * (10 - int(sal * 10))
    cat = r.get("category", "?")
    hint = r.get("compaction_hint", "?")
    content_preview = (r.get("content", "") or "")[:120].replace("\n", " ").strip()
    return (
        f"  [{r.get('id','?')}] {r.get('title','?')}\n"
        f"  {bar} {sal:.1f} | {cat} | {hint}\n"
        f"  {content_preview}...\n"
    )

def cmd_topic(keyword):
    """Find memory records related to a keyword (concept or title match)"""
    kw = keyword.lower().replace(" ", "_")
    with driver().session() as s:
        # Match by concept
        result = s.run("""
            MATCH (m:MemoryRecord)-[:LINKS_TO]->(c:Concept)
            WHERE toLower(c.id) CONTAINS $kw OR toLower(c.name) CONTAINS $kw
               OR toLower(m.title) CONTAINS $kw OR toLower(m.content) CONTAINS $kw
            RETURN DISTINCT m
            ORDER BY m.salience DESC
            LIMIT 10
        """, kw=keyword.lower())
        rows = list(result)
        if not rows:
            print(f"No records found for topic: {keyword}")
            return
        print(f"Records related to '{keyword}' ({len(rows)} found):\n")
        for row in rows:
            print(fmt_record(dict(row["m"])))

def cmd_related(record_id):
    """Find records related to a given record via shared concepts"""
    with driver().session() as s:
        result = s.run("""
            MATCH (m:MemoryRecord {id: $id})-[:RELATED]-(r:MemoryRecord)
            RETURN r, [(m)-[:RELATED {via: v}]-(r) | v] AS via_concepts
            ORDER BY r.salience DESC
            LIMIT 10
        """, id=record_id)
        rows = list(result)
        if not rows:
            print(f"No related records found for: {record_id}")
            return
        print(f"Records related to {record_id}:\n")
        for row in rows:
            r = dict(row["r"])
            via = row["via_concepts"]
            print(fmt_record(r))
            if via:
                print(f"  → via: {', '.join(str(v) for v in via[:3])}\n")

def cmd_category(cat):
    """All records in a category"""
    with driver().session() as s:
        result = s.run("""
            MATCH (m:MemoryRecord) WHERE m.category = $cat
            RETURN m ORDER BY m.salience DESC
        """, cat=cat)
        rows = list(result)
        if not rows:
            cats = s.run("MATCH (m:MemoryRecord) RETURN DISTINCT m.category AS c ORDER BY c")
            available = [r["c"] for r in cats]
            print(f"No records in category '{cat}'. Available: {', '.join(available)}")
            return
        print(f"Category '{cat}' ({len(rows)} records):\n")
        for row in rows:
            print(fmt_record(dict(row["m"])))

def cmd_high_salience(n=10):
    """Top N records by salience"""
    with driver().session() as s:
        result = s.run("""
            MATCH (m:MemoryRecord)
            RETURN m ORDER BY m.salience DESC
            LIMIT $n
        """, n=int(n))
        rows = list(result)
        print(f"Top {n} records by salience:\n")
        for row in rows:
            print(fmt_record(dict(row["m"])))

def cmd_path(id1, id2):
    """Shortest path between two memory records"""
    with driver().session() as s:
        result = s.run("""
            MATCH p = shortestPath(
                (a:MemoryRecord {id: $id1})-[*]-(b:MemoryRecord {id: $id2})
            )
            RETURN p, length(p) AS hops
        """, id1=id1, id2=id2)
        row = result.single()
        if not row:
            print(f"No path found between {id1} and {id2}")
            return
        print(f"Path: {id1} → {id2} ({row['hops']} hops)")
        for node in row["p"].nodes:
            labels = list(node.labels)
            props = dict(node)
            name = props.get("title") or props.get("name") or props.get("id", "?")
            print(f"  [{'/'.join(labels)}] {name}")

def cmd_cypher(query):
    """Raw Cypher query — returns JSON"""
    with driver().session() as s:
        result = s.run(query)
        rows = [dict(r) for r in result]
        # Convert Neo4j types to plain dicts
        def serialize(obj):
            if hasattr(obj, "_properties"):
                return dict(obj)
            if hasattr(obj, "__iter__") and not isinstance(obj, (str, dict)):
                return list(obj)
            return str(obj)
        print(json.dumps(rows, default=serialize, indent=2))

def cmd_stats():
    """Graph statistics"""
    with driver().session() as s:
        stats = {}
        for label in ["MemoryRecord", "Concept", "Infrastructure", "Agent"]:
            r = s.run(f"MATCH (n:{label}) RETURN count(n) AS c").single()
            stats[label] = r["c"]
        for rel in ["HAS_MEMORY", "LINKS_TO", "RELATED", "RUNS_ON"]:
            r = s.run(f"MATCH ()-[r:{rel}]->() RETURN count(r) AS c").single()
            stats[f"rel:{rel}"] = r["c"]
        cats = s.run("MATCH (m:MemoryRecord) RETURN m.category AS cat, count(m) AS n ORDER BY n DESC")
        print("=== Neo4j Graph Stats ===\n")
        print("Nodes:")
        for k in ["MemoryRecord", "Concept", "Infrastructure", "Agent"]:
            print(f"  {k}: {stats[k]}")
        print("\nRelationships:")
        for k, v in stats.items():
            if k.startswith("rel:"):
                print(f"  {k[4:]}: {v}")
        print("\nRecords by category:")
        for r in cats:
            print(f"  {r['cat']}: {r['n']}")
        print(f"\nBrowser: http://localhost:7474")
        print(f"LAN:     http://192.168.4.208:7474")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(0)

    cmd = args[0]
    try:
        if cmd == "topic":
            cmd_topic(args[1] if len(args) > 1 else "")
        elif cmd == "related":
            cmd_related(args[1])
        elif cmd == "category":
            cmd_category(args[1] if len(args) > 1 else "")
        elif cmd == "high-salience":
            cmd_high_salience(int(args[1]) if len(args) > 1 else 10)
        elif cmd == "path":
            cmd_path(args[1], args[2])
        elif cmd == "cypher":
            cmd_cypher(" ".join(args[1:]))
        elif cmd == "stats":
            cmd_stats()
        else:
            print(f"Unknown command: {cmd}\n")
            print(__doc__)
            sys.exit(1)
    except IndexError:
        print("Missing argument. Usage:\n")
        print(__doc__)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
