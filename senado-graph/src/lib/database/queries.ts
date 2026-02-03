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
import type {
  Senator,
  Party,
  Law,
  Committee,
  GraphData,
  EdgeType,
} from "$lib/types";

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

    const senators = result.records.map((record) => record.get("senator"));

    if (senators.length === 0) {
      console.warn("Database returned no senators, falling back to mock data");
      return getMockSenators();
    }

    return senators;
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

    const parties = result.records.map((record) => record.get("party"));

    if (parties.length === 0) {
      console.warn("Database returned no parties, falling back to mock data");
      return getMockParties();
    }

    return parties;
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

    const committees = result.records.map((record) => record.get("committee"));

    if (committees.length === 0) {
      console.warn("Database returned no committees, falling back to mock data");
      return getMockCommittees();
    }

    return committees;
  } finally {
    await session.close();
  }
}

export async function getInitialGraphData(
  lawStatuses?: string[],
): Promise<GraphData> {
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

    // Get law nodes with optional status filter
    let lawQuery = `
      MATCH (l:Law)
    `;

    const lawParams: Record<string, unknown> = {};

    if (lawStatuses && lawStatuses.length > 0) {
      lawQuery += ` WHERE l.status IN $lawStatuses`;
      lawParams.lawStatuses = lawStatuses;
    }

    lawQuery += `
      RETURN l {
        .id,
        .boletin,
        .title,
        .titleEn,
        .status,
        .topic
      } AS law
      LIMIT 50
    `;

    const lawsResult = await session.run(lawQuery, lawParams);

    // Get Party nodes with member counts
    const partiesResult = await session.run(`
      MATCH (p:Party)
      OPTIONAL MATCH (s:Senator)-[:BELONGS_TO]->(p)
      WHERE s.active = true
      RETURN p {
        .id,
        .name,
        .nameEn,
        .shortName,
        .color,
        .ideology
      } AS party, count(s) AS memberCount
    `);

    // Get Committee nodes
    const committeesResult = await session.run(`
      MATCH (c:Committee)
      RETURN c {
        .id,
        .name,
        .nameEn
      } AS committee
    `);

    // Get Lobbyist nodes (limit 30)
    const lobbyistsResult = await session.run(`
      MATCH (l:Lobbyist)
      RETURN l {
        .id,
        .name,
        .type,
        .industry,
        .industryEn
      } AS lobbyist
      LIMIT 30
    `);

    // Get AUTHORED edges (senator → law)
    const authoredResult = await session.run(`
      MATCH (s:Senator)-[:AUTHORED]->(l:Law)
      WHERE s.active = true
      RETURN s.id AS source, l.id AS target
    `);

    // Get BELONGS_TO edges (senator → party)
    const belongsToResult = await session.run(`
      MATCH (s:Senator)-[:BELONGS_TO]->(p:Party)
      WHERE s.active = true
      RETURN s.id AS source, p.id AS target
    `);

    // Get MEMBER_OF edges (senator → committee)
    const memberOfResult = await session.run(`
      MATCH (s:Senator)-[:MEMBER_OF]->(c:Committee)
      WHERE s.active = true
      RETURN s.id AS source, c.id AS target
    `);

    // Get LOBBY edges (lobbyist → senator)
    const lobbyResult = await session.run(`
      MATCH (l:Lobbyist)-[:LOBBY]->(s:Senator)
      WHERE s.active = true
      RETURN l.id AS source, s.id AS target
      LIMIT 50
    `);

    // Get VOTED_SAME edges between senators (voting patterns) - reduced to 50
    const votedSameResult = await session.run(`
      MATCH (s1:Senator)-[v:VOTED_SAME]->(s2:Senator)
      WHERE s1.id < s2.id AND v.agreement > 0.7
      RETURN s1.id AS source, s2.id AS target, v.agreement AS agreement
      LIMIT 50
    `);

    // Get VOTED_ON edges (senator → law)
    const votedOnResult = await session.run(`
      MATCH (s:Senator)-[v:VOTED_ON]->(l:Law)
      WHERE s.active = true
      RETURN s.id AS source, l.id AS target, v.vote AS vote
      LIMIT 100
    `);

    const senatorNodes = senatorsResult.records.map((record) => ({
      data: {
        id: record.get("senator").id,
        label: record.get("senator").name,
        type: "senator" as const,
        color: record.get("color"),
        party: record.get("senator").party,
        region: record.get("senator").region,
      },
    }));

    const lawNodes = lawsResult.records.map((record) => ({
      data: {
        id: record.get("law").id,
        label: record.get("law").boletin,
        type: "law" as const,
        status: record.get("law").status,
        topic: record.get("law").topic,
      },
    }));

    const partyNodes = partiesResult.records.map((record) => ({
      data: {
        id: record.get("party").id,
        label: record.get("party").shortName,
        type: "party" as const,
        color: record.get("party").color,
        ideology: record.get("party").ideology,
        memberCount: record.get("memberCount").toNumber(),
      },
    }));

    const committeeNodes = committeesResult.records.map((record) => ({
      data: {
        id: record.get("committee").id,
        label: record.get("committee").name,
        type: "committee" as const,
      },
    }));

    const lobbyistNodes = lobbyistsResult.records.map((record) => ({
      data: {
        id: record.get("lobbyist").id,
        label: record.get("lobbyist").name,
        type: "lobbyist" as const,
        lobbyistType: record.get("lobbyist").type,
      },
    }));

    const nodes = [
      ...senatorNodes,
      ...lawNodes,
      ...partyNodes,
      ...committeeNodes,
      ...lobbyistNodes,
    ];

    // If database is empty (no nodes), fall back to mock data
    if (nodes.length === 0) {
      console.warn("Graph: Database returned no data, falling back to mock data");
      return getMockGraphData();
    }

    let edgeIndex = 0;

    const authoredEdges = authoredResult.records.map((record) => ({
      data: {
        id: `edge_${edgeIndex++}`,
        source: record.get("source"),
        target: record.get("target"),
        type: "authored" as EdgeType,
      },
    }));

    const belongsToEdges = belongsToResult.records.map((record) => ({
      data: {
        id: `edge_${edgeIndex++}`,
        source: record.get("source"),
        target: record.get("target"),
        type: "belongs_to" as EdgeType,
      },
    }));

    const memberOfEdges = memberOfResult.records.map((record) => ({
      data: {
        id: `edge_${edgeIndex++}`,
        source: record.get("source"),
        target: record.get("target"),
        type: "member_of" as EdgeType,
      },
    }));

    const lobbyEdges = lobbyResult.records.map((record) => ({
      data: {
        id: `edge_${edgeIndex++}`,
        source: record.get("source"),
        target: record.get("target"),
        type: "lobby" as EdgeType,
      },
    }));

    const votedSameEdges = votedSameResult.records.map((record) => ({
      data: {
        id: `edge_${edgeIndex++}`,
        source: record.get("source"),
        target: record.get("target"),
        type: "voted_same" as EdgeType,
        agreement: record.get("agreement"),
      },
    }));

    const votedOnEdges = votedOnResult.records.map((record) => ({
      data: {
        id: `edge_${edgeIndex++}`,
        source: record.get("source"),
        target: record.get("target"),
        type: "voted_on" as EdgeType,
        vote: record.get("vote"),
      },
    }));

    const edges = [
      ...authoredEdges,
      ...belongsToEdges,
      ...memberOfEdges,
      ...lobbyEdges,
      ...votedSameEdges,
      ...votedOnEdges,
    ];

    // Create a set of all node IDs for filtering edges
    const nodeIds = new Set(nodes.map((n) => n.data.id));

    // Filter edges to only include those where both source and target exist
    const validEdges = edges.filter(
      (edge) =>
        nodeIds.has(edge.data.source) && nodeIds.has(edge.data.target),
    );

    console.log(
      `Graph: Filtered ${edges.length} edges to ${validEdges.length} valid edges (removed ${edges.length - validEdges.length} orphaned edges)`,
    );

    return { nodes, edges: validEdges };
  } catch (err) {
    console.error("Graph: Error fetching from database:", err);
    return getMockGraphData();
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
