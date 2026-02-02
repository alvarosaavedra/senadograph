// Neo4j Schema - Constraints and Indexes

// Constraints
CREATE CONSTRAINT senator_id IF NOT EXISTS
FOR (s:Senator) REQUIRE s.id IS UNIQUE;

CREATE CONSTRAINT party_id IF NOT EXISTS
FOR (p:Party) REQUIRE p.id IS UNIQUE;

CREATE CONSTRAINT law_id IF NOT EXISTS
FOR (l:Law) REQUIRE l.id IS UNIQUE;

CREATE CONSTRAINT vote_id IF NOT EXISTS
FOR (v:Vote) REQUIRE v.id IS UNIQUE;

CREATE CONSTRAINT committee_id IF NOT EXISTS
FOR (c:Committee) REQUIRE c.id IS UNIQUE;

CREATE CONSTRAINT lobbyist_id IF NOT EXISTS
FOR (l:Lobbyist) REQUIRE l.id IS UNIQUE;

// Indexes for performance
CREATE INDEX senator_name_idx IF NOT EXISTS
FOR (s:Senator) ON (s.name);

CREATE INDEX senator_party_idx IF NOT EXISTS
FOR (s:Senator) ON (s.party);

CREATE INDEX law_boletin_idx IF NOT EXISTS
FOR (l:Law) ON (l.boletin);

CREATE INDEX law_status_idx IF NOT EXISTS
FOR (l:Law) ON (l.status);

CREATE INDEX vote_date_idx IF NOT EXISTS
FOR (v:Vote) ON (v.date);
