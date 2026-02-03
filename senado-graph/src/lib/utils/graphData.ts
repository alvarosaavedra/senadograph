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
    // Determine which entity types to show (default to all if not specified)
    const entityTypes = filters.entityTypes || [
      "senator",
      "law",
      "party",
      "committee",
      "lobbyist",
    ];

    const params: Record<string, unknown> = {};

    // Only fetch senators if entity type is enabled
    let senatorsResult: { records: Neo4jRecord[] } = { records: [] };
    if (entityTypes.includes("senator")) {
      // Build senator query with filters
      let senatorQuery = `
        MATCH (s:Senator)
        WHERE s.active = true
      `;

      // Filter by party shortName (not ID)
      if (filters.parties && filters.parties.length > 0) {
        senatorQuery += ` AND s.party IN $parties`;
        params.parties = filters.parties;
      }

      senatorQuery += `
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

      senatorsResult = await session.run(senatorQuery, params);
    }

    // Only fetch laws if entity type is enabled
    let lawsResult: { records: Neo4jRecord[] } = { records: [] };
    if (entityTypes.includes("law")) {
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
        LIMIT 50
      `;

      lawsResult = await session.run(lawQuery, params);
    }

    // Only fetch parties if entity type is enabled
    let partiesResult: { records: Neo4jRecord[] } = { records: [] };
    if (entityTypes.includes("party")) {
      // Get Party nodes with member counts
      let partyQuery = `
        MATCH (p:Party)
      `;

      // Filter by party shortName to match senator.party field
      if (filters.parties && filters.parties.length > 0) {
        partyQuery += ` WHERE p.shortName IN $parties`;
      }

      partyQuery += `
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
      `;

      partiesResult = await session.run(partyQuery, params);
    }

    // Only fetch committees if entity type is enabled
    let committeesResult: { records: Neo4jRecord[] } = { records: [] };
    if (entityTypes.includes("committee")) {
      // Get Committee nodes
      let committeeQuery = `
        MATCH (c:Committee)
      `;

      if (filters.committees && filters.committees.length > 0) {
        committeeQuery += ` WHERE c.id IN $committees`;
        params.committees = filters.committees;
      }

      committeeQuery += `
        RETURN c {
          .id,
          .name,
          .nameEn
        } AS committee
      `;

      committeesResult = await session.run(committeeQuery, params);
    }

    // Only fetch lobbyists if entity type is enabled
    let lobbyistsResult: { records: Neo4jRecord[] } = { records: [] };
    if (entityTypes.includes("lobbyist")) {
      // Get Lobbyist nodes (limit 30)
      let lobbyistQuery = `
        MATCH (l:Lobbyist)
      `;

      if (filters.lobbyistTypes && filters.lobbyistTypes.length > 0) {
        lobbyistQuery += ` WHERE l.type IN $lobbyistTypes`;
        params.lobbyistTypes = filters.lobbyistTypes;
      }

      lobbyistQuery += `
        RETURN l {
          .id,
          .name,
          .type,
          .industry,
          .industryEn
        } AS lobbyist
        LIMIT 30
      `;

      lobbyistsResult = await session.run(lobbyistQuery, params);
    }

    // Get active relationship types from filters
    const activeEdgeTypes = filters.relationshipTypes || [
      "authored",
      "belongs_to",
      "member_of",
      "lobby",
      "voted_same",
    ];

    let edgeIndex = 0;
    const edges: GraphData["edges"] = [];

    // Get AUTHORED edges (senator → law) - only if both entity types are enabled
    if (
      activeEdgeTypes.includes("authored") &&
      entityTypes.includes("senator") &&
      entityTypes.includes("law")
    ) {
      let authoredQuery = `
        MATCH (s:Senator)-[:AUTHORED]->(l:Law)
        WHERE s.active = true
      `;

      // Use party shortName for filtering
      if (filters.parties && filters.parties.length > 0) {
        authoredQuery += ` AND s.party IN $parties`;
      }

      if (filters.lawStatuses && filters.lawStatuses.length > 0) {
        authoredQuery += ` AND l.status IN $lawStatuses`;
      }

      authoredQuery += ` RETURN s.id AS source, l.id AS target`;

      const authoredResult = await session.run(authoredQuery, params);
      authoredResult.records.forEach((record: Neo4jRecord) => {
        edges.push({
          data: {
            id: `edge_${edgeIndex++}`,
            source: record.get("source"),
            target: record.get("target"),
            type: "authored" as EdgeType,
          },
        });
      });
    }

    // Get BELONGS_TO edges (senator → party) - only if both entity types are enabled
    if (
      activeEdgeTypes.includes("belongs_to") &&
      entityTypes.includes("senator") &&
      entityTypes.includes("party")
    ) {
      let belongsToQuery = `
        MATCH (s:Senator)-[:BELONGS_TO]->(p:Party)
        WHERE s.active = true
      `;

      // Use party shortName for filtering senators
      if (filters.parties && filters.parties.length > 0) {
        belongsToQuery += ` AND s.party IN $parties AND p.shortName IN $parties`;
      }

      belongsToQuery += ` RETURN s.id AS source, p.id AS target`;

      const belongsToResult = await session.run(belongsToQuery, params);
      belongsToResult.records.forEach((record: Neo4jRecord) => {
        edges.push({
          data: {
            id: `edge_${edgeIndex++}`,
            source: record.get("source"),
            target: record.get("target"),
            type: "belongs_to" as EdgeType,
          },
        });
      });
    }

    // Get MEMBER_OF edges (senator → committee) - only if both entity types are enabled
    if (
      activeEdgeTypes.includes("member_of") &&
      entityTypes.includes("senator") &&
      entityTypes.includes("committee")
    ) {
      let memberOfQuery = `
        MATCH (s:Senator)-[:MEMBER_OF]->(c:Committee)
        WHERE s.active = true
      `;

      // Use party shortName for filtering
      if (filters.parties && filters.parties.length > 0) {
        memberOfQuery += ` AND s.party IN $parties`;
      }

      if (filters.committees && filters.committees.length > 0) {
        memberOfQuery += ` AND c.id IN $committees`;
      }

      memberOfQuery += ` RETURN s.id AS source, c.id AS target`;

      const memberOfResult = await session.run(memberOfQuery, params);
      memberOfResult.records.forEach((record: Neo4jRecord) => {
        edges.push({
          data: {
            id: `edge_${edgeIndex++}`,
            source: record.get("source"),
            target: record.get("target"),
            type: "member_of" as EdgeType,
          },
        });
      });
    }

    // Get LOBBY edges (lobbyist → senator) - only if both entity types are enabled
    if (
      activeEdgeTypes.includes("lobby") &&
      entityTypes.includes("lobbyist") &&
      entityTypes.includes("senator")
    ) {
      let lobbyQuery = `
        MATCH (l:Lobbyist)-[:LOBBY]->(s:Senator)
        WHERE s.active = true
      `;

      // Use party shortName for filtering
      if (filters.parties && filters.parties.length > 0) {
        lobbyQuery += ` AND s.party IN $parties`;
      }

      if (filters.lobbyistTypes && filters.lobbyistTypes.length > 0) {
        lobbyQuery += ` AND l.type IN $lobbyistTypes`;
      }

      lobbyQuery += ` RETURN l.id AS source, s.id AS target LIMIT 50`;

      const lobbyResult = await session.run(lobbyQuery, params);
      lobbyResult.records.forEach((record: Neo4jRecord) => {
        edges.push({
          data: {
            id: `edge_${edgeIndex++}`,
            source: record.get("source"),
            target: record.get("target"),
            type: "lobby" as EdgeType,
          },
        });
      });
    }

    // Get VOTED_SAME edges between senators (voting patterns) - only if senators enabled
    if (
      activeEdgeTypes.includes("voted_same") &&
      entityTypes.includes("senator")
    ) {
      let votedSameQuery = `
        MATCH (s1:Senator)-[v:VOTED_SAME]->(s2:Senator)
        WHERE s1.id < s2.id AND v.agreement > 0.7
      `;

      // Use party shortName for filtering
      if (filters.parties && filters.parties.length > 0) {
        votedSameQuery += ` AND s1.party IN $parties AND s2.party IN $parties`;
      }

      if (filters.agreementRange) {
        votedSameQuery += ` AND v.agreement >= $minAgreement AND v.agreement <= $maxAgreement`;
        params.minAgreement = filters.agreementRange.min;
        params.maxAgreement = filters.agreementRange.max;
      }

      votedSameQuery += `
        RETURN s1.id AS source, s2.id AS target, v.agreement AS agreement
        LIMIT 50
      `;

      const votedSameResult = await session.run(votedSameQuery, params);
      votedSameResult.records.forEach((record: Neo4jRecord) => {
        edges.push({
          data: {
            id: `edge_${edgeIndex++}`,
            source: record.get("source"),
            target: record.get("target"),
            type: "voted_same" as EdgeType,
            agreement: record.get("agreement"),
          },
        });
      });
    }

    // Get VOTED_ON edges (senator → law) - only if both entity types are enabled
    if (
      activeEdgeTypes.includes("voted_on") &&
      entityTypes.includes("senator") &&
      entityTypes.includes("law")
    ) {
      let votedOnQuery = `
        MATCH (s:Senator)-[v:VOTED_ON]->(l:Law)
        WHERE s.active = true
      `;

      // Use party shortName for filtering
      if (filters.parties && filters.parties.length > 0) {
        votedOnQuery += ` AND s.party IN $parties`;
      }

      if (filters.lawStatuses && filters.lawStatuses.length > 0) {
        votedOnQuery += ` AND l.status IN $lawStatuses`;
      }

      votedOnQuery += `
        RETURN s.id AS source, l.id AS target, v.vote AS vote
        LIMIT 100
      `;

      const votedOnResult = await session.run(votedOnQuery, params);
      votedOnResult.records.forEach((record: Neo4jRecord) => {
        edges.push({
          data: {
            id: `edge_${edgeIndex++}`,
            source: record.get("source"),
            target: record.get("target"),
            type: "voted_on" as EdgeType,
            vote: record.get("vote"),
          },
        });
      });
    }

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

    const partyNodes = partiesResult.records.map((record: Neo4jRecord) => ({
      data: {
        id: record.get("party").id,
        label: record.get("party").shortName,
        type: "party" as const,
        color: record.get("party").color,
        ideology: record.get("party").ideology,
        memberCount: record.get("memberCount").toNumber(),
      },
    }));

    const committeeNodes = committeesResult.records.map(
      (record: Neo4jRecord) => ({
        data: {
          id: record.get("committee").id,
          label: record.get("committee").name,
          type: "committee" as const,
        },
      }),
    );

    const lobbyistNodes = lobbyistsResult.records.map(
      (record: Neo4jRecord) => ({
        data: {
          id: record.get("lobbyist").id,
          label: record.get("lobbyist").name,
          type: "lobbyist" as const,
          lobbyistType: record.get("lobbyist").type,
        },
      }),
    );

    const nodes = [
      ...senatorNodes,
      ...lawNodes,
      ...partyNodes,
      ...committeeNodes,
      ...lobbyistNodes,
    ];

    // Create a set of all node IDs for filtering edges
    const nodeIds = new Set(nodes.map((n) => n.data.id));

    // Filter edges to only include those where both source and target exist
    const validEdges = edges.filter(
      (edge) => nodeIds.has(edge.data.source) && nodeIds.has(edge.data.target),
    );

    console.log(
      `Graph: Filtered ${edges.length} edges to ${validEdges.length} valid edges (removed ${edges.length - validEdges.length} orphaned edges)`,
    );

    return { nodes, edges: validEdges };
  } finally {
    await session.close();
  }
}
