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
            "CREATE CONSTRAINT donation_id IF NOT EXISTS FOR (d:Donation) REQUIRE d.id IS UNIQUE",
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

    def seed_votes(self, votes: list):
        """Seed voting records into Neo4j."""
        print(f"Seeding {len(votes)} voting records...")

        # Pre-process senator names for better matching
        query = """
        UNWIND $votes AS vote
        MATCH (l:Law {boletin: vote.law_boletin})
        MATCH (s:Senator)
        WHERE 
            // Try exact match first
            s.name = vote.senator_name
            OR
            // Match where senator name is "LastNames, FirstName" 
            // and vote name is "LastInitials., FirstName"
            // Extract first name from vote name (after the last space)
            vote.senator_name = split(s.name, ', ')[1] + 
                CASE 
                    WHEN split(vote.senator_name, ' ')[-1] = split(s.name, ', ')[1] THEN split(vote.senator_name, ' ')[0]
                    ELSE ''
                END
            OR
            // Try matching just the first name
            split(vote.senator_name, ' ')[-1] = split(s.name, ', ')[1]
        MERGE (s)-[v:VOTED_ON]->(l)
        SET v.session = vote.session,
            v.date = vote.date,
            v.vote = vote.vote,
            v.topic = vote.topic
        """

        with self.driver.session() as session:
            result = session.run(query, votes=votes)
            summary = result.consume()
            print(
                f"Created {summary.counters.relationships_created} VOTED_ON relationships"
            )

        print("Votes seeded")

    def calculate_voting_similarity(self, min_common_votes: int = 5):
        """Calculate VOTED_SAME relationships based on actual voting patterns."""
        print("Calculating voting similarity between senators...")

        query = """
        // Get all senators who voted on the same laws
        MATCH (s1:Senator)-[v1:VOTED_ON]->(l:Law)<-[v2:VOTED_ON]-(s2:Senator)
        WHERE s1 <> s2 AND v1.vote = v2.vote

        // Group by senator pairs and count common votes
        WITH s1, s2, count(*) AS common_votes
        WHERE common_votes >= $min_common_votes

        // Calculate agreement percentage
        MATCH (s1)-[v1:VOTED_ON]->(l:Law)
        WITH s1, s2, common_votes, count(v1) AS total_s1
        MATCH (s2)-[v2:VOTED_ON]->(l)
        WITH s1, s2, common_votes, total_s1, count(v2) AS total_s2

        // Calculate Jaccard similarity: intersection / union
        WITH s1, s2, common_votes, total_s1, total_s2,
             (toFloat(common_votes) / (total_s1 + total_s2 - common_votes)) AS agreement

        // Create relationship with agreement score
        CREATE (s1)-[r:VOTED_SAME]->(s2)
        SET r.agreement = agreement

        RETURN count(r) AS relationships_created
        """

        with self.driver.session() as session:
            result = session.run(query, min_common_votes=min_common_votes)
            record = result.single()
            if record:
                count = record[0]
                print(
                    f"Created {count} VOTED_SAME relationships based on {min_common_votes}+ common votes"
                )
            else:
                print("No VOTED_SAME relationships created")

        print("Voting similarity calculated")

    def seed_lobbyists(self, lobbyists: list):
        """Seed lobbyists into Neo4j."""
        print(f"Seeding {len(lobbyists)} lobbyists...")

        query = """
        UNWIND $lobbyists AS lobbyist
        MERGE (l:Lobbyist {id: lobbyist.id})
        SET l.name = lobbyist.name,
            l.type = lobbyist.type,
            l.industry = lobbyist.industry,
            l.registrationDate = lobbyist.registration_date,
            l.origin = lobbyist.origin
        """

        with self.driver.session() as session:
            session.run(query, lobbyists=lobbyists)

        print("Lobbyists seeded")

    def seed_lobby_meetings(self, meetings: list):
        """Seed lobby meeting relationships."""
        print(f"Seeding {len(meetings)} lobby meeting relationships...")

        query = """
        UNWIND $meetings AS meeting
        MERGE (s:Senator {id: meeting.senator_id})
        SET s.name = meeting.senator_name
        WITH s, meeting
        MERGE (l:Lobbyist {id: meeting.lobbyist_id})
        MERGE (s)-[m:MET_WITH_LOBBYIST]->(l)
        SET m.date = meeting.date,
            m.topic = meeting.topic,
            m.senatorName = meeting.senator_name,
            m.lobbyistName = meeting.lobbyist_name
        """

        with self.driver.session() as session:
            session.run(query, meetings=meetings)

        print("Lobby meeting relationships seeded")

    def seed_lobby_trips(self, trips: list):
        """Seed lobbyist-funded trip relationships."""
        print(f"Seeding {len(trips)} lobby trip relationships...")

        query = """
        UNWIND $trips AS trip
        MERGE (s:Senator {id: trip.senator_id})
        SET s.name = trip.senator_name
        WITH s, trip
        MERGE (l:Lobbyist {id: trip.lobbyist_id})
        MERGE (s)-[t:TRIP_FUNDED_BY]->(l)
        SET t.destination = trip.destination,
            t.purpose = trip.purpose,
            t.cost = trip.cost,
            t.fundedBy = trip.funded_by,
            t.invitedBy = trip.invited_by,
            t.senatorName = trip.senator_name,
            t.lobbyistName = trip.lobbyist_name
        """

        with self.driver.session() as session:
            session.run(query, trips=trips)

        print("Lobby trip relationships seeded")

    def seed_lobby_donations(self, donations: list):
        """Seed donation relationships."""
        print(f"Seeding {len(donations)} donation relationships...")

        query = """
        UNWIND $donations AS donation
        MERGE (s:Senator {id: donation.senator_id})
        SET s.name = donation.senator_name
        WITH s, donation
        MERGE (l:Lobbyist {id: donation.lobbyist_id})
        MERGE (s)-[d:RECEIVED_DONATION]->(l)
        SET d.date = donation.date,
            d.occasion = donation.occasion,
            d.item = donation.item,
            d.donor = donation.donor,
            d.senatorName = donation.senator_name,
            d.lobbyistName = donation.lobbyist_name
        """

        with self.driver.session() as session:
            session.run(query, donations=donations)

        print("Donation relationships seeded")


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

        # Load voting data if available
        try:
            with open(f"{data_dir}/votes.json", "r", encoding="utf-8") as f:
                votes = json.load(f)
        except FileNotFoundError:
            print("No voting data found, skipping...")
            votes = []

        # Load lobby data if available
        try:
            with open(f"{data_dir}/lobbyists.json", "r", encoding="utf-8") as f:
                lobbyists = json.load(f)
        except FileNotFoundError:
            print("No lobbyist data found, skipping...")
            lobbyists = []

        try:
            with open(f"{data_dir}/lobby_meetings.json", "r", encoding="utf-8") as f:
                meetings = json.load(f)
        except FileNotFoundError:
            print("No lobby meeting data found, skipping...")
            meetings = []

        try:
            with open(f"{data_dir}/lobby_trips.json", "r", encoding="utf-8") as f:
                trips = json.load(f)
        except FileNotFoundError:
            print("No lobby trip data found, skipping...")
            trips = []

        try:
            with open(f"{data_dir}/lobby_donations.json", "r", encoding="utf-8") as f:
                donations = json.load(f)
        except FileNotFoundError:
            print("No donation data found, skipping...")
            donations = []

        # Seed data
        seeder.seed_parties(parties)
        seeder.seed_senators(senators)
        seeder.seed_laws(laws)
        seeder.seed_law_authorships(authorships)

        # Seed voting data if available
        if votes:
            seeder.seed_votes(votes)
            # Calculate real voting similarity instead of using mock data
            seeder.calculate_voting_similarity(min_common_votes=3)
        else:
            # Create sample relationships
            seeder.create_sample_relationships()

        # Seed lobby data if available
        if lobbyists:
            seeder.seed_lobbyists(lobbyists)

        if meetings:
            seeder.seed_lobby_meetings(meetings)

        if trips:
            seeder.seed_lobby_trips(trips)

        if donations:
            seeder.seed_lobby_donations(donations)

        print("Seeding complete!")

    except Exception as e:
        print(f"Error: {e}")
        raise
    finally:
        seeder.close()


if __name__ == "__main__":
    main()
