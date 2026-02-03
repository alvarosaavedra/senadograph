#!/usr/bin/env python3
"""
Clear all data from Neo4j database.
This will delete all nodes and relationships.
"""

import os
import sys

# Add parent directory to path to import neo4j module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from neo4j import GraphDatabase
except ImportError:
    print("Error: neo4j package not installed")
    print("Install with: pip install neo4j")
    sys.exit(1)


def clear_database():
    """Delete all nodes and relationships from Neo4j."""
    # Load connection details from environment or use defaults
    uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "password")

    if not password:
        print("Error: NEO4J_PASSWORD environment variable not set")
        print("Set it with: export NEO4J_PASSWORD=your_password")
        sys.exit(1)

    print(f"Connecting to Neo4j at {uri}...")

    try:
        driver = GraphDatabase.driver(uri, auth=(user, password))

        with driver.session() as session:
            # Count existing data
            result = session.run("MATCH (n) RETURN count(n) AS node_count")
            node_count = result.single()["node_count"]

            result = session.run("MATCH ()-[r]->() RETURN count(r) AS rel_count")
            rel_count = result.single()["rel_count"]

            print(f"\nCurrent database state:")
            print(f"  Nodes: {node_count}")
            print(f"  Relationships: {rel_count}")

            if node_count == 0 and rel_count == 0:
                print("\nDatabase is already empty!")
                return

            # Confirm deletion
            confirm = input(
                f"\n⚠️  WARNING: This will DELETE ALL {node_count} nodes and {rel_count} relationships!\n"
            )
            print("Type 'yes' to confirm: ")

            if confirm.lower().strip() != "yes":
                print("Operation cancelled.")
                return

            # Delete all relationships first (faster than DETACH DELETE for large datasets)
            print("\nDeleting relationships...")
            result = session.run("MATCH ()-[r]->() DELETE r")
            summary = result.consume()
            print(f"  Deleted {summary.counters.relationships_deleted} relationships")

            # Delete all nodes
            print("Deleting nodes...")
            result = session.run("MATCH (n) DELETE n")
            summary = result.consume()
            print(f"  Deleted {summary.counters.nodes_deleted} nodes")

            print("\n✅ Database cleared successfully!")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        if "driver" in locals():
            driver.close()


if __name__ == "__main__":
    clear_database()
