// Seed data for testing

// Parties
CREATE (p1:Party {
  id: 'party_rn',
  name: 'Renovación Nacional',
  nameEn: 'National Renewal',
  shortName: 'RN',
  color: '#0054a6',
  ideology: 'center-right'
});

CREATE (p2:Party {
  id: 'party_ps',
  name: 'Partido Socialista',
  nameEn: 'Socialist Party',
  shortName: 'PS',
  color: '#e4002b',
  ideology: 'center-left'
});

CREATE (p3:Party {
  id: 'party_udI',
  name: 'Unión Demócrata Independiente',
  nameEn: 'Independent Democratic Union',
  shortName: 'UDI',
  color: '#1a237e',
  ideology: 'right'
});

// Senators
CREATE (s1:Senator {
  id: 'senator_001',
  name: 'Juan Pérez',
  nameEn: 'Juan Perez',
  party: 'RN',
  region: 'Metropolitana',
  regionEn: 'Metropolitan',
  email: 'juan.perez@senado.cl',
  photoUrl: '/images/senators/001.jpg',
  biography: 'Senador desde 2022',
  biographyEn: 'Senator since 2022',
  startDate: '2022-03-11',
  active: true
});

CREATE (s2:Senator {
  id: 'senator_002',
  name: 'María González',
  nameEn: 'Maria Gonzalez',
  party: 'PS',
  region: 'Valparaíso',
  regionEn: 'Valparaiso',
  email: 'maria.gonzalez@senado.cl',
  photoUrl: '/images/senators/002.jpg',
  biography: 'Primera senadora de la región',
  biographyEn: 'First senator from the region',
  startDate: '2022-03-11',
  active: true
});

CREATE (s3:Senator {
  id: 'senator_003',
  name: 'Carlos Rodríguez',
  nameEn: 'Carlos Rodriguez',
  party: 'UDI',
  region: 'Biobío',
  regionEn: 'Biobio',
  email: 'carlos.rodriguez@senado.cl',
  photoUrl: '/images/senators/003.jpg',
  biography: 'Veterano del senado',
  biographyEn: 'Senate veteran',
  startDate: '2018-03-11',
  active: true
});

// Relationships
MATCH (s:Senator), (p:Party)
WHERE s.party = p.shortName
CREATE (s)-[:BELONGS_TO]->(p);

// Voting similarity (sample data)
MATCH (s1:Senator {id: 'senator_001'}), (s2:Senator {id: 'senator_002'})
CREATE (s1)-[:VOTED_SAME {agreement: 0.85}]->(s2);

MATCH (s1:Senator {id: 'senator_001'}), (s2:Senator {id: 'senator_003'})
CREATE (s1)-[:VOTED_SAME {agreement: 0.72}]->(s2);

MATCH (s1:Senator {id: 'senator_002'}), (s2:Senator {id: 'senator_003'})
CREATE (s1)-[:VOTED_SAME {agreement: 0.45}]->(s2);

// Committees
CREATE (c1:Committee {
  id: 'committee_education',
  name: 'Educación',
  nameEn: 'Education'
});

CREATE (c2:Committee {
  id: 'committee_finance',
  name: 'Hacienda',
  nameEn: 'Finance'
});

// Committee memberships
MATCH (s:Senator {id: 'senator_001'}), (c:Committee {id: 'committee_education'})
CREATE (s)-[:MEMBER_OF {role: 'member'}]->(c);

MATCH (s:Senator {id: 'senator_002'}), (c:Committee {id: 'committee_finance'})
CREATE (s)-[:MEMBER_OF {role: 'president'}]->(c);

// Laws (sample)
CREATE (l1:Law {
  id: 'law_12345',
  boletin: '12345-06',
  title: 'Proyecto de Ley de Educación',
  titleEn: 'Education Law Project',
  description: 'Reforma educacional integral',
  descriptionEn: 'Comprehensive education reform',
  dateProposed: '2023-01-15',
  status: 'in_discussion',
  topic: 'education'
});

// Authorship
MATCH (s:Senator {id: 'senator_001'}), (l:Law {id: 'law_12345'})
CREATE (s)-[:AUTHORED {role: 'principal', date: '2023-01-15'}]->(l);

MATCH (s:Senator {id: 'senator_002'}), (l:Law {id: 'law_12345'})
CREATE (s)-[:CO_SPONSORED]->(l);
