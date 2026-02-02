"""Update Neo4j database with incremental changes."""

import json
import os
from datetime import datetime
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


class Neo4jUpdater:
    """Updates Neo4j with incremental changes from scraping."""

    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def update_senators(self, senators: list):
        """Update or insert senators."""
        print(f"Updating {len(senators)} senators...")

        query = """
        UNWIND $senators AS senator
        MERGE (s:Senator {id: senator.id})
        SET s.name = senator.name,
            s.nameEn = senator.nameEn,
            s.party = senator.party,
            s.region = senator.region,
            s.regionEn = senator.regionEn,
            s.email = senator.email,
            s.photoUrl = senator.photoUrl,
            s.biography = senator.biography,
            s.biographyEn = senator.biographyEn,
            s.startDate = senator.startDate,
            s.active = senator.active,
            s.lastUpdated = datetime()
        WITH s, senator
        MATCH (p:Party {shortName: senator.party})
        MERGE (s)-[:BELONGS_TO]->(p)
        """

        with self.driver.session() as session:
            session.run(query, senators=senators)

        print("Senators updated")

    def update_laws(self, laws: list):
        """Update or insert laws."""
        print(f"Updating {len(laws)} laws...")

        query = """
        UNWIND $laws AS law
        MERGE (l:Law {id: law.id})
        SET l.boletin = law.boletin,
            l.title = law.title,
            l.titleEn = law.titleEn,
            l.description = law.description,
            l.descriptionEn = law.descriptionEn,
            l.dateProposed = law.dateProposed,
            l.status = law.status,
            l.topic = law.topic,
            l.lastUpdated = datetime()
        """

        with self.driver.session() as session:
            session.run(query, laws=laws)

        print("Laws updated")

    def mark_inactive_senators(self, active_ids: list):
        """Mark senators as inactive if not in active list."""
        query = """
        MATCH (s:Senator)
        WHERE NOT s.id IN $active_ids
        SET s.active = false, s.endDate = date()
        RETURN count(s) AS count
        """

        with self.driver.session() as session:
            result = session.run(query, active_ids=active_ids)
            count = result.single()["count"]
            print(f"Marked {count} senators as inactive")

    def log_update(self, update_type: str, count: int):
        """Log update activity."""
        query = """
        CREATE (u:Update {
            id: randomUUID(),
            type: $type,
            count: $count,
            timestamp: datetime()
        })
        """

        with self.driver.session() as session:
            session.run(query, type=update_type, count=count)


def main():
    """Main update function."""
    print("Starting Neo4j updater...")

    updater = Neo4jUpdater()

    try:
        data_dir = os.path.join(os.path.dirname(__file__), "data")

        # Load and update senators
        try:
            with open(f"{data_dir}/senators.json", "r", encoding="utf-8") as f:
                senators = json.load(f)
            updater.update_senators(senators)
            active_ids = [s["id"] for s in senators]
            updater.mark_inactive_senators(active_ids)
            updater.log_update("senators", len(senators))
        except FileNotFoundError:
            print("No senator data found to update")

        # Load and update laws
        try:
            with open(f"{data_dir}/laws.json", "r", encoding="utf-8") as f:
                laws = json.load(f)
            updater.update_laws(laws)
            updater.log_update("laws", len(laws))
        except FileNotFoundError:
            print("No law data found to update")

        print("Update complete!")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        updater.close()


if __name__ == "__main__":
    main()
