import type {
  Senator,
  Party,
  Law,
  Committee,
  GraphData,
  Lobbyist,
} from "$lib/types";

// Mock data for development without Neo4j
const mockParties: Party[] = [
  {
    id: "party_rn",
    name: "Renovación Nacional",
    nameEn: "National Renewal",
    shortName: "RN",
    color: "#0054a6",
    ideology: "center-right",
  },
  {
    id: "party_ps",
    name: "Partido Socialista",
    nameEn: "Socialist Party",
    shortName: "PS",
    color: "#e4002b",
    ideology: "center-left",
  },
  {
    id: "party_udi",
    name: "Unión Demócrata Independiente",
    nameEn: "Independent Democratic Union",
    shortName: "UDI",
    color: "#1a237e",
    ideology: "right",
  },
  {
    id: "party_pdc",
    name: "Partido Demócrata Cristiano",
    nameEn: "Christian Democratic Party",
    shortName: "PDC",
    color: "#0066cc",
    ideology: "center",
  },
];

const mockSenators: Senator[] = [
  {
    id: "senator_001",
    name: "Juan Pérez González",
    nameEn: "Juan Perez Gonzalez",
    party: "RN",
    region: "Metropolitana",
    regionEn: "Metropolitan",
    email: "juan.perez@senado.cl",
    photoUrl: "/images/senators/senator_001.jpg",
    biography: "Senador desde 2022, abogado de profesión",
    biographyEn: "Senator since 2022, lawyer by profession",
    startDate: "2022-03-11",
    active: true,
  },
  {
    id: "senator_002",
    name: "María González Silva",
    nameEn: "Maria Gonzalez Silva",
    party: "PS",
    region: "Valparaíso",
    regionEn: "Valparaiso",
    email: "maria.gonzalez@senado.cl",
    photoUrl: "/images/senators/senator_002.jpg",
    biography: "Primera senadora de la región de Valparaíso",
    biographyEn: "First senator from Valparaiso region",
    startDate: "2022-03-11",
    active: true,
  },
  {
    id: "senator_003",
    name: "Carlos Rodríguez Martínez",
    nameEn: "Carlos Rodriguez Martinez",
    party: "UDI",
    region: "Biobío",
    regionEn: "Biobio",
    email: "carlos.rodriguez@senado.cl",
    photoUrl: "/images/senators/senator_003.jpg",
    biography: "Veterano del senado con 8 años de servicio",
    biographyEn: "Senate veteran with 8 years of service",
    startDate: "2018-03-11",
    active: true,
  },
  {
    id: "senator_004",
    name: "Ana María López",
    nameEn: "Ana Maria Lopez",
    party: "PDC",
    region: "Maule",
    regionEn: "Maule",
    email: "ana.lopez@senado.cl",
    photoUrl: "/images/senators/senator_004.jpg",
    biography: "Especialista en educación y derechos sociales",
    biographyEn: "Specialist in education and social rights",
    startDate: "2022-03-11",
    active: true,
  },
  {
    id: "senator_005",
    name: "Pedro Hernández Castro",
    nameEn: "Pedro Hernandez Castro",
    party: "RN",
    region: "Araucanía",
    regionEn: "Araucania",
    email: "pedro.hernandez@senado.cl",
    photoUrl: "/images/senators/senator_005.jpg",
    biography: "Empresario y político con enfoque económico",
    biographyEn: "Businessman and politician with economic focus",
    startDate: "2022-03-11",
    active: true,
  },
];

const mockCommittees: Committee[] = [
  { id: "committee_education", name: "Educación", nameEn: "Education" },
  { id: "committee_finance", name: "Hacienda", nameEn: "Finance" },
  { id: "committee_health", name: "Salud", nameEn: "Health" },
];

const mockLaws: Law[] = [
  {
    id: "law_12345",
    boletin: "12345-06",
    title: "Proyecto de Ley de Educación Superior",
    titleEn: "Higher Education Law Project",
    description: "Reforma integral al sistema de educación superior",
    descriptionEn: "Comprehensive reform of the higher education system",
    dateProposed: "2023-01-15",
    status: "in_discussion",
    topic: "education",
  },
  {
    id: "law_12346",
    boletin: "12346-07",
    title: "Proyecto de Ley de Protección Ambiental",
    titleEn: "Environmental Protection Law Project",
    description: "Fortalecimiento de la protección del medio ambiente",
    descriptionEn: "Strengthening environmental protection",
    dateProposed: "2023-02-20",
    status: "in_discussion",
    topic: "environment",
  },
  {
    id: "law_12347",
    boletin: "12347-08",
    title: "Proyecto de Ley de Seguridad Ciudadana",
    titleEn: "Citizen Security Law Project",
    description: "Medidas para mejorar la seguridad pública",
    descriptionEn: "Measures to improve public security",
    dateProposed: "2023-03-10",
    status: "approved",
    topic: "security",
  },
];

const mockLobbyists: Lobbyist[] = [
  {
    id: "lobbyist_001",
    name: "Mining Association",
    type: "company",
    industry: "Mining",
    industryEn: "Mining",
  },
  {
    id: "lobbyist_002",
    name: "Workers Union",
    type: "union",
    industry: "Labor",
    industryEn: "Labor",
  },
  {
    id: "lobbyist_003",
    name: "Environmental NGO",
    type: "ngo",
    industry: "Environment",
    industryEn: "Environment",
  },
];

export function getMockParties(): Party[] {
  return mockParties;
}

export function getMockSenators(): Senator[] {
  return mockSenators;
}

export function getMockCommittees(): Committee[] {
  return mockCommittees;
}

export function getMockLaws(): Law[] {
  return mockLaws;
}

export function getMockLobbyists(): Lobbyist[] {
  return mockLobbyists;
}

export function getMockSenatorById(id: string): Senator | null {
  return mockSenators.find((s) => s.id === id) || null;
}

export function getMockLawById(id: string): Law | null {
  return mockLaws.find((l) => l.id === id) || null;
}

export function getMockLawsForSenator(senatorId: string): Law[] {
  if (senatorId === "senator_001") return [mockLaws[0], mockLaws[1]];
  if (senatorId === "senator_002") return [mockLaws[0], mockLaws[2]];
  if (senatorId === "senator_003") return [mockLaws[1]];
  return [mockLaws[2]];
}

export function getMockCommitteesForSenator(senatorId: string): Committee[] {
  if (senatorId === "senator_001")
    return [mockCommittees[0], mockCommittees[1]];
  if (senatorId === "senator_002") return [mockCommittees[1]];
  if (senatorId === "senator_003")
    return [mockCommittees[0], mockCommittees[2]];
  return [mockCommittees[2]];
}

export function getMockAuthorsForLaw(lawId: string): Senator[] {
  if (lawId === "law_12345") return [mockSenators[0], mockSenators[1]];
  if (lawId === "law_12346") return [mockSenators[0], mockSenators[2]];
  if (lawId === "law_12347") return [mockSenators[1], mockSenators[3]];
  return [mockSenators[4]];
}

export function getMockGraphData(): GraphData {
  const nodes = [
    ...mockSenators.map((senator) => {
      const party = mockParties.find((p) => p.shortName === senator.party);
      return {
        data: {
          id: senator.id,
          label: senator.name,
          type: "senator" as const,
          color: party?.color || "#cccccc",
          party: senator.party,
          region: senator.region,
        },
      };
    }),
    ...mockLaws.map((law) => ({
      data: {
        id: law.id,
        label: law.boletin,
        type: "law" as const,
        status: law.status,
        topic: law.topic,
      },
    })),
    ...mockParties.map((party) => ({
      data: {
        id: party.id,
        label: party.shortName,
        type: "party" as const,
        color: party.color,
        ideology: party.ideology,
        memberCount: mockSenators.filter((s) => s.party === party.shortName)
          .length,
      },
    })),
    ...mockCommittees.map((committee) => ({
      data: {
        id: committee.id,
        label: committee.name,
        type: "committee" as const,
      },
    })),
    ...mockLobbyists.map((lobbyist) => ({
      data: {
        id: lobbyist.id,
        label: lobbyist.name,
        type: "lobbyist" as const,
        lobbyistType: lobbyist.type,
        industry: lobbyist.industry,
      },
    })),
  ];

  const edges = [
    {
      data: {
        id: "edge_1",
        source: "senator_001",
        target: "senator_002",
        type: "voted_same" as const,
        agreement: 0.85,
      },
    },
    {
      data: {
        id: "edge_2",
        source: "senator_001",
        target: "senator_003",
        type: "voted_same" as const,
        agreement: 0.72,
      },
    },
    {
      data: {
        id: "edge_3",
        source: "senator_002",
        target: "senator_003",
        type: "voted_same" as const,
        agreement: 0.45,
      },
    },
    {
      data: {
        id: "edge_4",
        source: "senator_001",
        target: "senator_005",
        type: "voted_same" as const,
        agreement: 0.9,
      },
    },
    {
      data: {
        id: "edge_5",
        source: "senator_002",
        target: "senator_004",
        type: "voted_same" as const,
        agreement: 0.68,
      },
    },
    {
      data: {
        id: "edge_6",
        source: "senator_001",
        target: "law_12345",
        type: "authored" as const,
      },
    },
    {
      data: {
        id: "edge_7",
        source: "senator_002",
        target: "law_12345",
        type: "authored" as const,
      },
    },
    {
      data: {
        id: "edge_8",
        source: "senator_001",
        target: "law_12346",
        type: "authored" as const,
      },
    },
    {
      data: {
        id: "edge_9",
        source: "senator_002",
        target: "law_12347",
        type: "authored" as const,
      },
    },
    {
      data: {
        id: "edge_10",
        source: "senator_001",
        target: "party_rn",
        type: "belongs_to" as const,
      },
    },
    {
      data: {
        id: "edge_11",
        source: "senator_005",
        target: "party_rn",
        type: "belongs_to" as const,
      },
    },
    {
      data: {
        id: "edge_12",
        source: "senator_002",
        target: "party_ps",
        type: "belongs_to" as const,
      },
    },
    {
      data: {
        id: "edge_13",
        source: "senator_003",
        target: "party_udi",
        type: "belongs_to" as const,
      },
    },
    {
      data: {
        id: "edge_14",
        source: "senator_004",
        target: "party_pdc",
        type: "belongs_to" as const,
      },
    },
    {
      data: {
        id: "edge_15",
        source: "senator_001",
        target: "committee_education",
        type: "member_of" as const,
      },
    },
    {
      data: {
        id: "edge_16",
        source: "senator_001",
        target: "committee_finance",
        type: "member_of" as const,
      },
    },
    {
      data: {
        id: "edge_17",
        source: "senator_002",
        target: "committee_finance",
        type: "member_of" as const,
      },
    },
    {
      data: {
        id: "edge_18",
        source: "senator_003",
        target: "committee_education",
        type: "member_of" as const,
      },
    },
    {
      data: {
        id: "edge_19",
        source: "senator_003",
        target: "committee_health",
        type: "member_of" as const,
      },
    },
    {
      data: {
        id: "edge_20",
        source: "lobbyist_001",
        target: "senator_001",
        type: "lobby" as const,
      },
    },
    {
      data: {
        id: "edge_21",
        source: "lobbyist_002",
        target: "senator_002",
        type: "lobby" as const,
      },
    },
    {
      data: {
        id: "edge_22",
        source: "lobbyist_003",
        target: "senator_004",
        type: "lobby" as const,
      },
    },
  ];

  return { nodes, edges };
}
