#!/usr/bin/env python3
"""
Ingest Moto's typed YAML memory records into Neo4j as a knowledge graph.
Nodes: MemoryRecord, Concept
Edges: LINKS_TO (record→concept), RELATED (concept→concept via shared records)
"""
import os
import yaml
import glob
from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "WestAILabs2026!"
RECORDS_DIR = "/home/jlwestsr/.openclaw/workspace/memory/long-term"

def load_records():
    records = []
    for path in sorted(glob.glob(f"{RECORDS_DIR}/rec-*.yaml")):
        with open(path) as f:
            try:
                r = yaml.safe_load(f)
                r["_file"] = os.path.basename(path)
                records.append(r)
            except Exception as e:
                print(f"  SKIP {path}: {e}")
    return records

def ingest(driver, records):
    with driver.session() as session:
        # Clear existing memory graph
        session.run("MATCH (n:MemoryRecord) DETACH DELETE n")
        session.run("MATCH (n:Concept) DETACH DELETE n")
        print(f"Cleared existing nodes.")

        # Create agent node
        session.run("""
            MERGE (a:Agent {id: 'moto'})
            SET a.name = 'Moto West',
                a.host = 'shurtugal-lnx',
                a.version = 'moto-v1',
                a.updated_at = datetime()
        """)

        # Ingest each record
        for r in records:
            rec_id = r.get("id", r["_file"])
            title = r.get("title", "")
            category = r.get("category", "fact")
            subcategory = r.get("subcategory", "")
            content = str(r.get("content", ""))[:2000]  # truncate for graph
            salience = float(r.get("salience", 0.5))
            decay_class = r.get("decay_class", "normal")
            compaction_hint = r.get("compaction_hint", "summarize")
            concepts = r.get("linked_concepts", []) or []
            source = r.get("source", "MEMORY.md migration 2026-03-10")

            # Create MemoryRecord node
            session.run("""
                MERGE (m:MemoryRecord {id: $id})
                SET m.title = $title,
                    m.category = $category,
                    m.subcategory = $subcategory,
                    m.content = $content,
                    m.salience = $salience,
                    m.decay_class = $decay_class,
                    m.compaction_hint = $compaction_hint,
                    m.source = $source,
                    m.file = $file
                WITH m
                MATCH (a:Agent {id: 'moto'})
                MERGE (a)-[:HAS_MEMORY]->(m)
            """, id=rec_id, title=title, category=category,
                subcategory=subcategory, content=content,
                salience=salience, decay_class=decay_class,
                compaction_hint=compaction_hint, source=source,
                file=r["_file"])

            # Create Concept nodes and link
            for concept in concepts:
                concept_clean = concept.strip().lower().replace(" ", "_")
                session.run("""
                    MERGE (c:Concept {id: $cid})
                    SET c.name = $name
                    WITH c
                    MATCH (m:MemoryRecord {id: $mid})
                    MERGE (m)-[:LINKS_TO]->(c)
                """, cid=concept_clean, name=concept.strip(), mid=rec_id)

            print(f"  ✓ {rec_id}: {title[:50]} (salience={salience}, concepts={len(concepts)})")

        # Create cross-concept edges (shared concept = related records)
        session.run("""
            MATCH (m1:MemoryRecord)-[:LINKS_TO]->(c:Concept)<-[:LINKS_TO]-(m2:MemoryRecord)
            WHERE m1.id < m2.id
            MERGE (m1)-[:RELATED {via: c.name}]->(m2)
        """)

        # Add agent infrastructure nodes
        infra = [
            {"id": "shurtugal-lnx", "type": "host", "role": "primary OpenClaw host", "ip": "192.168.4.208"},
            {"id": "nebulus", "type": "host", "role": "Mac Mini M4 Pro, Cael agent", "ip": "192.168.4.30"},
            {"id": "hohenheim", "type": "host", "role": "Jr workstation, Ollama", "ip": "192.168.4.221"},
            {"id": "gitea", "type": "service", "role": "git server", "port": "3001"},
            {"id": "neo4j", "type": "service", "role": "graph database", "port": "7687"},
            {"id": "ollama", "type": "service", "role": "local LLM", "port": "11434"},
            {"id": "chromadb", "type": "service", "role": "vector store", "port": "8001"},
        ]
        for node in infra:
            session.run("""
                MERGE (n:Infrastructure {id: $id})
                SET n += $props
            """, id=node["id"], props=node)

        # Link agent to its host
        session.run("""
            MATCH (a:Agent {id: 'moto'}), (h:Infrastructure {id: 'shurtugal-lnx'})
            MERGE (a)-[:RUNS_ON]->(h)
        """)

        # Get stats
        result = session.run("MATCH (m:MemoryRecord) RETURN count(m) as records")
        rec_count = result.single()["records"]
        result = session.run("MATCH (c:Concept) RETURN count(c) as concepts")
        concept_count = result.single()["concepts"]
        result = session.run("MATCH ()-[r:RELATED]->() RETURN count(r) as rels")
        rel_count = result.single()["rels"]

        print(f"\nGraph summary:")
        print(f"  MemoryRecord nodes: {rec_count}")
        print(f"  Concept nodes:      {concept_count}")
        print(f"  RELATED edges:      {rel_count}")
        print(f"  Neo4j browser:      http://localhost:7474")
        print(f"  LAN access:         http://192.168.4.208:7474")

def main():
    print("Loading memory records...")
    records = load_records()
    print(f"Found {len(records)} records.")

    print("\nConnecting to Neo4j...")
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    driver.verify_connectivity()
    print("Connected.")

    print("\nIngesting...")
    ingest(driver, records)
    driver.close()
    print("\nDone.")

if __name__ == "__main__":
    main()
