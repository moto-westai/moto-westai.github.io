#!/usr/bin/env python3
"""
graph-schema.py — Set up Neo4j constraints, indexes, and the full entity schema.

Run this once (or after a DB wipe) to prepare the graph for enrichment.

Schema:
  Nodes:     Agent, Person, Organization, Project, Product, Infrastructure,
             Service, MemoryRecord, Concept, Decision, Event
  Key rels:  WORKS_FOR, BUILT_BY, COLLABORATES_WITH, WORKS_AT, OWNS,
             DEVELOPED_BY, RUNS_ON, HAS_MEMORY, LINKS_TO, RELATED,
             ABOUT, MADE_BY, AFFECTS, PARTICIPATED_IN, SUCCEEDED
"""
from neo4j import GraphDatabase

URI  = "bolt://localhost:7687"
AUTH = ("neo4j", "WestAILabs2026!")

CONSTRAINTS = [
    ("Agent",          "id"),
    ("Person",         "id"),
    ("Organization",   "id"),
    ("Project",        "id"),
    ("Product",        "id"),
    ("Infrastructure", "id"),
    ("MemoryRecord",   "id"),
    ("Concept",        "id"),
    ("Decision",       "id"),
    ("Event",          "id"),
]

INDEXES = [
    ("MemoryRecord", "salience"),
    ("MemoryRecord", "category"),
    ("MemoryRecord", "compaction_hint"),
    ("Person",       "name"),
    ("Project",      "name"),
    ("Organization", "name"),
    ("Event",        "date"),
]

def run(driver):
    with driver.session() as s:
        print("Creating constraints...")
        for label, prop in CONSTRAINTS:
            try:
                s.run(f"""
                    CREATE CONSTRAINT {label.lower()}_{prop}_unique IF NOT EXISTS
                    FOR (n:{label}) REQUIRE n.{prop} IS UNIQUE
                """)
                print(f"  ✓ {label}.{prop}")
            except Exception as e:
                print(f"  ~ {label}.{prop}: {e}")

        print("\nCreating indexes...")
        for label, prop in INDEXES:
            try:
                s.run(f"""
                    CREATE INDEX {label.lower()}_{prop}_idx IF NOT EXISTS
                    FOR (n:{label}) ON (n.{prop})
                """)
                print(f"  ✓ {label}.{prop}")
            except Exception as e:
                print(f"  ~ {label}.{prop}: {e}")

        print("\nSchema ready.")

if __name__ == "__main__":
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    run(driver)
    driver.close()
