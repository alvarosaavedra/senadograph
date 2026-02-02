import { getDriver } from "./neo4j";
import {
  getMockSenators,
  getMockSenatorById,
  getMockParties,
  getMockCommittees,
  getMockGraphData,
  getMockLawById,
  getMockLawsForSenator,
  getMockCommitteesForSenator,
  getMockAuthorsForLaw,
} from "./mockData";
import type { Senator, Party, Law, Committee, GraphData, EdgeType } from "$lib/types";

// Helper to check if we should use mock data
function useMockData(): boolean {
  return getDriver() === null;
}

export async function getAllSenators(): Promise<Senator[]> {
  if (useMockData()) {
    return getMockSenators();
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(`
      MATCH (s:Senator)
      RETURN s {
        .id,
        .name,
        .nameEn,
        .party,
        .region,
        .regionEn,
        .email,
        .photoUrl,
        .biography,
        .biographyEn,
        .startDate,
        .active
      } AS senator
    `);

    return result.records.map((record) => record.get("senator"));
  } finally {
    await session.close();
  }
}

export async function getSenatorById(id: string): Promise<Senator | null> {
  if (useMockData()) {
    return getMockSenatorById(id);
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(
      `
      MATCH (s:Senator {id: $id})
      RETURN s {
        .id,
        .name,
        .nameEn,
        .party,
        .region,
        .regionEn,
        .email,
        .photoUrl,
        .biography,
        .biographyEn,
        .startDate,
        .active
      } AS senator
    `,
      { id },
    );

    if (result.records.length === 0) {
      return null;
    }

    return result.records[0].get("senator");
  } finally {
    await session.close();
  }
}

export async function getAllParties(): Promise<Party[]> {
  if (useMockData()) {
    return getMockParties();
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(`
      MATCH (p:Party)
      RETURN p {
        .id,
        .name,
        .nameEn,
        .shortName,
        .color,
        .ideology
      } AS party
    `);

    return result.records.map((record) => record.get("party"));
  } finally {
    await session.close();
  }
}

export async function getAllCommittees(): Promise<Committee[]> {
  if (useMockData()) {
    return getMockCommittees();
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(`
      MATCH (c:Committee)
      RETURN c {
        .id,
        .name,
        .nameEn
      } AS committee
    `);

    return result.records.map((record) => record.get("committee"));
  } finally {
    await session.close();
  }
}

export async function getInitialGraphData(): Promise<GraphData> {
  if (useMockData()) {
    return getMockGraphData();
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    // Get all senators with their parties
    const senatorsResult = await session.run(`
      MATCH (s:Senator)-[:BELONGS_TO]->(p:Party)
      WHERE s.active = true
      RETURN s {
        .id,
        .name,
        .nameEn,
        .party,
        .region,
        .active
      } AS senator, p.color AS color
    `);

    // Get relationships between senators (voting patterns)
    const relationshipsResult = await session.run(`
      MATCH (s1:Senator)-[v:VOTED_SAME]->(s2:Senator)
      WHERE s1.id < s2.id AND v.agreement > 0.7
      RETURN s1.id AS source, s2.id AS target, v.agreement AS agreement
      LIMIT 100
    `);

    const nodes = senatorsResult.records.map((record) => ({
      data: {
        id: record.get("senator").id,
        label: record.get("senator").name,
        type: "senator" as const,
        color: record.get("color"),
        party: record.get("senator").party,
        region: record.get("senator").region,
      },
    }));

    const edges = relationshipsResult.records.map((record, index) => ({
      data: {
        id: `edge_${index}`,
        source: record.get("source"),
        target: record.get("target"),
        type: "voted_same" as EdgeType,
        agreement: record.get("agreement"),
      },
    }));

    return { nodes, edges };
  } finally {
    await session.close();
  }
}

export async function getLawById(id: string): Promise<Law | null> {
  if (useMockData()) {
    return getMockLawById(id);
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(
      `
      MATCH (l:Law {id: $id})
      RETURN l {
        .id,
        .boletin,
        .title,
        .titleEn,
        .description,
        .descriptionEn,
        .dateProposed,
        .status,
        .topic
      } AS law
    `,
      { id },
    );

    if (result.records.length === 0) {
      return null;
    }

    return result.records[0].get("law");
  } finally {
    await session.close();
  }
}

export async function getLawsForSenator(senatorId: string): Promise<Law[]> {
  if (useMockData()) {
    return getMockLawsForSenator(senatorId);
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(
      `
      MATCH (s:Senator {id: $senatorId})-[:AUTHORED]->(l:Law)
      RETURN l {
        .id,
        .boletin,
        .title,
        .titleEn,
        .dateProposed,
        .status,
        .topic
      } AS law
      ORDER BY l.dateProposed DESC
    `,
      { senatorId },
    );

    return result.records.map((record) => record.get("law"));
  } finally {
    await session.close();
  }
}

export async function getCommitteesForSenator(
  senatorId: string,
): Promise<Committee[]> {
  if (useMockData()) {
    return getMockCommitteesForSenator(senatorId);
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(
      `
      MATCH (s:Senator {id: $senatorId})-[:MEMBER_OF]->(c:Committee)
      RETURN c {
        .id,
        .name,
        .nameEn
      } AS committee
    `,
      { senatorId },
    );

    return result.records.map((record) => record.get("committee"));
  } finally {
    await session.close();
  }
}

export async function getAuthorsForLaw(lawId: string): Promise<Senator[]> {
  if (useMockData()) {
    return getMockAuthorsForLaw(lawId);
  }

  const driver = getDriver()!;
  const session = driver.session();

  try {
    const result = await session.run(
      `
      MATCH (s:Senator)-[:AUTHORED]->(l:Law {id: $lawId})
      RETURN s {
        .id,
        .name,
        .nameEn,
        .party,
        .region
      } AS senator
    `,
      { lawId },
    );

    return result.records.map((record) => record.get("senator"));
  } finally {
    await session.close();
  }
}
