import type { GraphData, GraphFilters, EdgeType } from "$lib/types";
import { getDriver } from "$lib/database/neo4j";
import { getMockGraphData } from "$lib/database/mockData";
import type { Record as Neo4jRecord } from "neo4j-driver";

export async function getFilteredGraphData(
  filters: GraphFilters,
): Promise<GraphData> {
  const driver = getDriver();

  if (!driver) {
    // Return mock data if no database connection
    return getMockGraphData();
  }

  const session = driver.session();

  try {
    let query = `
      MATCH (s:Senator)
      WHERE s.active = true
    `;

    const params: Record<string, unknown> = {};

    if (filters.parties && filters.parties.length > 0) {
      query += ` AND s.party IN $parties`;
      params.parties = filters.parties;
    }

    query += `
      MATCH (s)-[:BELONGS_TO]->(p:Party)
      RETURN s {
        .id,
        .name,
        .nameEn,
        .party,
        .region,
        .active
      } AS senator, p.color AS color
    `;

    const senatorsResult = await session.run(query, params);

    // Get law nodes with optional status filter
    let lawQuery = `
      MATCH (l:Law)
    `;

    if (filters.lawStatuses && filters.lawStatuses.length > 0) {
      lawQuery += ` WHERE l.status IN $lawStatuses`;
      params.lawStatuses = filters.lawStatuses;
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
      LIMIT 200
    `;

    const lawsResult = await session.run(lawQuery, params);

    // Get relationships
    let relQuery = `
      MATCH (s1:Senator)-[v:VOTED_SAME]->(s2:Senator)
      WHERE s1.id < s2.id AND v.agreement > 0.7
    `;

    if (filters.parties && filters.parties.length > 0) {
      relQuery += ` AND s1.party IN $parties AND s2.party IN $parties`;
    }

    relQuery += `
      RETURN s1.id AS source, s2.id AS target, v.agreement AS agreement
      LIMIT 100
    `;

    const relationshipsResult = await session.run(relQuery, params);

    const senatorNodes = senatorsResult.records.map((record: Neo4jRecord) => ({
      data: {
        id: record.get("senator").id,
        label: record.get("senator").name,
        type: "senator" as const,
        color: record.get("color"),
        party: record.get("senator").party,
        region: record.get("senator").region,
      },
    }));

    const lawNodes = lawsResult.records.map((record: Neo4jRecord) => ({
      data: {
        id: record.get("law").id,
        label: record.get("law").boletin,
        type: "law" as const,
        status: record.get("law").status,
        topic: record.get("law").topic,
      },
    }));

    const nodes = [...senatorNodes, ...lawNodes];

    const edges = relationshipsResult.records.map(
      (record: Neo4jRecord, index: number) => ({
        data: {
          id: `edge_${index}`,
          source: record.get("source"),
          target: record.get("target"),
          type: "voted_same" as EdgeType,
          agreement: record.get("agreement"),
        },
      }),
    );

    return { nodes, edges };
  } finally {
    await session.close();
  }
}
