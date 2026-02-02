"""Seed Neo4j database with initial data."""

import json
import os
from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD


class Neo4jSeeder:
    """Seeds Neo4j with initial data from scraped files or mock data."""

    def __init__(self):
        self.driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

    def close(self):
        self.driver.close()

    def create_constraints(self):
        """Create database constraints and indexes."""
        print("Creating constraints...")

        constraints = [
            "CREATE CONSTRAINT senator_id IF NOT EXISTS FOR (s:Senator) REQUIRE s.id IS UNIQUE",
            "CREATE CONSTRAINT party_id IF NOT EXISTS FOR (p:Party) REQUIRE p.id IS UNIQUE",
            "CREATE CONSTRAINT law_id IF NOT EXISTS FOR (l:Law) REQUIRE l.id IS UNIQUE",
            "CREATE CONSTRAINT committee_id IF NOT EXISTS FOR (c:Committee) REQUIRE c.id IS UNIQUE",
            "CREATE CONSTRAINT vote_id IF NOT EXISTS FOR (v:Vote) REQUIRE v.id IS UNIQUE",
            "CREATE CONSTRAINT lobbyist_id IF NOT EXISTS FOR (l:Lobbyist) REQUIRE l.id IS UNIQUE",
        ]

        with self.driver.session() as session:
            for constraint in constraints:
                try:
                    session.run(constraint)
                except Exception as e:
                    print(f"Warning: {e}")

        print("Constraints created")

    def seed_parties(self, parties: list):
        """Seed parties into Neo4j."""
        print(f"Seeding {len(parties)} parties...")

        query = """
        UNWIND $parties AS party
        MERGE (p:Party {id: party.id})
        SET p.name = party.name,
            p.nameEn = party.nameEn,
            p.shortName = party.shortName,
            p.color = party.color,
            p.ideology = party.ideology
        """

        with self.driver.session() as session:
            session.run(query, parties=parties)

        print("Parties seeded")

    def seed_senators(self, senators: list):
        """Seed senators into Neo4j."""
        print(f"Seeding {len(senators)} senators...")

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
            s.active = senator.active
        WITH s, senator
        MATCH (p:Party {shortName: senator.party})
        MERGE (s)-[:BELONGS_TO]->(p)
        """

        with self.driver.session() as session:
            session.run(query, senators=senators)

        print("Senators seeded")

    def seed_laws(self, laws: list):
        """Seed laws into Neo4j."""
        print(f"Seeding {len(laws)} laws...")

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
            l.topic = law.topic
        """

        with self.driver.session() as session:
            session.run(query, laws=laws)

        print("Laws seeded")

    def create_sample_relationships(self):
        """Create sample relationships for testing."""
        print("Creating sample relationships...")

        query = """
        // Create voting similarities
        MATCH (s1:Senator), (s2:Senator)
        WHERE s1.id < s2.id AND s1.party = s2.party
        WITH s1, s2, rand() AS r
        WHERE r > 0.3
        CREATE (s1)-[:VOTED_SAME {agreement: 0.7 + r * 0.3}]->(s2)
        """

        with self.driver.session() as session:
            session.run(query)

        print("Sample relationships created")

    def seed_law_authorships(self, authorships: list):
        """Seed law authorship relationships."""
        print(f"Seeding {len(authorships)} authorship relationships...")

        query = """
        UNWIND $authorships AS auth
        MATCH (s:Senator {id: auth.senator_id})
        MATCH (l:Law {id: auth.law_id})
        MERGE (s)-[:AUTHORED {role: auth.role, date: auth.date}]->(l)
        """

        with self.driver.session() as session:
            session.run(query, authorships=authorships)

        print("Authorship relationships seeded")


def load_mock_data():
    """Load mock data for testing when scraping fails."""
    parties = [
        {
            "id": "party_rn",
            "name": "Renovación Nacional",
            "nameEn": "National Renewal",
            "shortName": "RN",
            "color": "#0054a6",
            "ideology": "center-right",
        },
        {
            "id": "party_ps",
            "name": "Partido Socialista",
            "nameEn": "Socialist Party",
            "shortName": "PS",
            "color": "#e4002b",
            "ideology": "center-left",
        },
        {
            "id": "party_udi",
            "name": "Unión Demócrata Independiente",
            "nameEn": "Independent Democratic Union",
            "shortName": "UDI",
            "color": "#1a237e",
            "ideology": "right",
        },
        {
            "id": "party_pdc",
            "name": "Partido Demócrata Cristiano",
            "nameEn": "Christian Democratic Party",
            "shortName": "PDC",
            "color": "#0066cc",
            "ideology": "center",
        },
    ]

    senators = [
        {
            "id": "senator_001",
            "name": "Juan Pérez González",
            "nameEn": "Juan Perez Gonzalez",
            "party": "RN",
            "region": "Metropolitana",
            "regionEn": "Metropolitan",
            "email": "juan.perez@senado.cl",
            "photoUrl": "/images/senators/senator_001.jpg",
            "biography": "Senador desde 2022, abogado de profesión",
            "biographyEn": "Senator since 2022, lawyer by profession",
            "startDate": "2022-03-11",
            "active": True,
        },
        {
            "id": "senator_002",
            "name": "María González Silva",
            "nameEn": "Maria Gonzalez Silva",
            "party": "PS",
            "region": "Valparaíso",
            "regionEn": "Valparaiso",
            "email": "maria.gonzalez@senado.cl",
            "photoUrl": "/images/senators/senator_002.jpg",
            "biography": "Primera senadora de la región de Valparaíso",
            "biographyEn": "First senator from Valparaiso region",
            "startDate": "2022-03-11",
            "active": True,
        },
        {
            "id": "senator_003",
            "name": "Carlos Rodríguez Martínez",
            "nameEn": "Carlos Rodriguez Martinez",
            "party": "UDI",
            "region": "Biobío",
            "regionEn": "Biobio",
            "email": "carlos.rodriguez@senado.cl",
            "photoUrl": "/images/senators/senator_003.jpg",
            "biography": "Veterano del senado con 8 años de servicio",
            "biographyEn": "Senate veteran with 8 years of service",
            "startDate": "2018-03-11",
            "active": True,
        },
        {
            "id": "senator_004",
            "name": "Ana María López",
            "nameEn": "Ana Maria Lopez",
            "party": "PDC",
            "region": "Maule",
            "regionEn": "Maule",
            "email": "ana.lopez@senado.cl",
            "photoUrl": "/images/senators/senator_004.jpg",
            "biography": "Especialista en educación y derechos sociales",
            "biographyEn": "Specialist in education and social rights",
            "startDate": "2022-03-11",
            "active": True,
        },
        {
            "id": "senator_005",
            "name": "Pedro Hernández Castro",
            "nameEn": "Pedro Hernandez Castro",
            "party": "RN",
            "region": "Araucanía",
            "regionEn": "Araucania",
            "email": "pedro.hernandez@senado.cl",
            "photoUrl": "/images/senators/senator_005.jpg",
            "biography": "Empresario y político con enfoque económico",
            "biographyEn": "Businessman and politician with economic focus",
            "startDate": "2022-03-11",
            "active": True,
        },
    ]

    laws = [
        {
            "id": "law_12345",
            "boletin": "12345-06",
            "title": "Proyecto de Ley de Educación Superior",
            "titleEn": "Higher Education Law Project",
            "description": "Reforma integral al sistema de educación superior",
            "descriptionEn": "Comprehensive reform of the higher education system",
            "dateProposed": "2023-01-15",
            "status": "in_discussion",
            "topic": "education",
        },
        {
            "id": "law_12346",
            "boletin": "12346-07",
            "title": "Proyecto de Ley de Protección Ambiental",
            "titleEn": "Environmental Protection Law Project",
            "description": "Fortalecimiento de la protección del medio ambiente",
            "descriptionEn": "Strengthening environmental protection",
            "dateProposed": "2023-02-20",
            "status": "in_discussion",
            "topic": "environment",
        },
        {
            "id": "law_12347",
            "boletin": "12347-08",
            "title": "Proyecto de Ley de Seguridad Ciudadana",
            "titleEn": "Citizen Security Law Project",
            "description": "Medidas para mejorar la seguridad pública",
            "descriptionEn": "Measures to improve public security",
            "dateProposed": "2023-03-10",
            "status": "approved",
            "topic": "security",
        },
    ]

    return parties, senators, laws


def main():
    """Main seeding function."""
    print("Starting Neo4j seeder...")

    seeder = Neo4jSeeder()

    try:
        # Create constraints
        seeder.create_constraints()

        # Load data
        data_dir = os.path.join(os.path.dirname(__file__), "data")

        # Try to load from scraped data, fallback to mock data
        try:
            with open(f"{data_dir}/parties.json", "r", encoding="utf-8") as f:
                parties = json.load(f)
        except FileNotFoundError:
            print("Using mock party data...")
            parties, _, _ = load_mock_data()

        try:
            with open(f"{data_dir}/senators.json", "r", encoding="utf-8") as f:
                senators = json.load(f)
        except FileNotFoundError:
            print("Using mock senator data...")
            _, senators, _ = load_mock_data()

        try:
            with open(f"{data_dir}/laws.json", "r", encoding="utf-8") as f:
                laws = json.load(f)
        except FileNotFoundError:
            print("Using mock law data...")
            _, _, laws = load_mock_data()

        try:
            with open(f"{data_dir}/authorships.json", "r", encoding="utf-8") as f:
                authorships = json.load(f)
        except FileNotFoundError:
            print("Using mock authorship data...")
            authorships = []
            if senators and laws:
                import random

                for senator in senators:
                    for _ in range(random.randint(1, 3)):
                        law = random.choice(laws)
                        authorships.append(
                            {
                                "senator_id": senator["id"],
                                "law_id": law["id"],
                                "role": "principal"
                                if random.random() > 0.5
                                else "co_sponsor",
                                "date": law["dateProposed"],
                            }
                        )

        # Seed data
        seeder.seed_parties(parties)
        seeder.seed_senators(senators)
        seeder.seed_laws(laws)
        seeder.seed_law_authorships(authorships)

        # Create sample relationships
        seeder.create_sample_relationships()

        print("Seeding complete!")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        seeder.close()


if __name__ == "__main__":
    main()
