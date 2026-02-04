import type { GraphData, GraphNode, ClusterInfo } from "$lib/types";

interface LouvainNode {
  id: string;
  community: number;
  neighbors: Map<string, number>;
}

interface LouvainGraph {
  nodes: Map<string, LouvainNode>;
  totalWeight: number;
}

const CLUSTER_COLORS = [
  "#ef4444", // red-500
  "#3b82f6", // blue-500
  "#10b981", // emerald-500
  "#f59e0b", // amber-500
  "#8b5cf6", // violet-500
  "#ec4899", // pink-500
  "#06b6d4", // cyan-500
  "#84cc16", // lime-500
  "#f97316", // orange-500
  "#6366f1", // indigo-500
];

/**
 * Build a weighted graph from VOTED_SAME edges
 */
function buildWeightedGraph(graphData: GraphData): LouvainGraph {
  const nodes = new Map<string, LouvainNode>();
  let totalWeight = 0;

  // Initialize nodes for all senators
  graphData.nodes
    .filter((node) => node.data.type === "senator")
    .forEach((node) => {
      nodes.set(node.data.id, {
        id: node.data.id,
        community: nodes.size,
        neighbors: new Map(),
      });
    });

  // Add weighted edges from VOTED_SAME relationships
  graphData.edges
    .filter((edge) => edge.data.type === "voted_same")
    .forEach((edge) => {
      const source = nodes.get(edge.data.source);
      const target = nodes.get(edge.data.target);
      const weight = (edge.data.agreement as number) || 0.5;

      if (source && target) {
        source.neighbors.set(target.id, weight);
        target.neighbors.set(source.id, weight);
        totalWeight += weight;
      }
    });

  return { nodes, totalWeight };
}

/**
 * Calculate modularity gain for moving node to target community
 */
function calculateModularityGain(
  node: LouvainNode,
  targetCommunity: number,
  graph: LouvainGraph,
  nodeDegrees: Map<string, number>,
  communityWeights: Map<number, number>,
): number {
  const ki = nodeDegrees.get(node.id) || 0;
  const ki_in =
    Array.from(node.neighbors.entries())
      .filter(([neighborId]) => {
        const neighbor = graph.nodes.get(neighborId);
        return neighbor && neighbor.community === targetCommunity;
      })
      .reduce((sum, [, weight]) => sum + weight, 0) * 2;

  const sigma_tot = communityWeights.get(targetCommunity) || 0;
  const m = graph.totalWeight;

  return ki_in / (2 * m) - (sigma_tot * ki) / (2 * m * m);
}

/**
 * Calculate degree of each node (sum of edge weights)
 */
function calculateNodeDegrees(graph: LouvainGraph): Map<string, number> {
  const degrees = new Map<string, number>();

  graph.nodes.forEach((node, id) => {
    const degree = Array.from(node.neighbors.values()).reduce(
      (sum, weight) => sum + weight,
      0,
    );
    degrees.set(id, degree);
  });

  return degrees;
}

/**
 * Calculate total weight of each community
 */
function calculateCommunityWeights(
  graph: LouvainGraph,
  nodeDegrees: Map<string, number>,
): Map<number, number> {
  const weights = new Map<number, number>();

  graph.nodes.forEach((node) => {
    const currentWeight = weights.get(node.community) || 0;
    weights.set(
      node.community,
      currentWeight + (nodeDegrees.get(node.id) || 0),
    );
  });

  return weights;
}

/**
 * Perform one phase of Louvain algorithm (local moving)
 */
function louvainPhase(graph: LouvainGraph): boolean {
  let improved = false;
  const nodeDegrees = calculateNodeDegrees(graph);
  let communityWeights = calculateCommunityWeights(graph, nodeDegrees);

  const nodeIds = Array.from(graph.nodes.keys());
  let changed = true;
  let iterations = 0;
  const maxIterations = 100;

  while (changed && iterations < maxIterations) {
    changed = false;
    iterations++;

    // Shuffle node order for better convergence
    const shuffledIds = [...nodeIds].sort(() => Math.random() - 0.5);

    for (const nodeId of shuffledIds) {
      const node = graph.nodes.get(nodeId);
      if (!node) continue;

      const currentCommunity = node.community;
      let bestCommunity = currentCommunity;
      let bestGain = 0;

      // Collect communities of neighbors
      const neighborCommunities = new Set<number>();
      node.neighbors.forEach((_, neighborId) => {
        const neighbor = graph.nodes.get(neighborId);
        if (neighbor) {
          neighborCommunities.add(neighbor.community);
        }
      });

      // Try moving to each neighbor's community
      for (const community of neighborCommunities) {
        if (community === currentCommunity) continue;

        const gain = calculateModularityGain(
          node,
          community,
          graph,
          nodeDegrees,
          communityWeights,
        );

        if (gain > bestGain) {
          bestGain = gain;
          bestCommunity = community;
        }
      }

      // Move to best community if improvement found
      if (bestCommunity !== currentCommunity) {
        // Update community weights
        const nodeDegree = nodeDegrees.get(node.id) || 0;
        communityWeights.set(
          currentCommunity,
          (communityWeights.get(currentCommunity) || 0) - nodeDegree,
        );
        communityWeights.set(
          bestCommunity,
          (communityWeights.get(bestCommunity) || 0) + nodeDegree,
        );

        node.community = bestCommunity;
        changed = true;
        improved = true;
      }
    }
  }

  return improved;
}

/**
 * Rebuild graph with communities as nodes (aggregation phase)
 */
function aggregateGraph(graph: LouvainGraph): LouvainGraph {
  const newNodes = new Map<string, LouvainNode>();

  // Create new nodes for each community
  graph.nodes.forEach((node) => {
    if (!newNodes.has(String(node.community))) {
      newNodes.set(String(node.community), {
        id: String(node.community),
        community: node.community,
        neighbors: new Map(),
      });
    }
  });

  // Aggregate edges between communities
  let totalWeight = 0;
  graph.nodes.forEach((node) => {
    const communityNode = newNodes.get(String(node.community));
    if (!communityNode) return;

    node.neighbors.forEach((weight, neighborId) => {
      const neighbor = graph.nodes.get(neighborId);
      if (!neighbor) return;

      const neighborCommunity = String(neighbor.community);
      const currentWeight = communityNode.neighbors.get(neighborCommunity) || 0;
      communityNode.neighbors.set(neighborCommunity, currentWeight + weight);
      totalWeight += weight;
    });
  });

  return { nodes: newNodes, totalWeight };
}

/**
 * Run complete Louvain algorithm
 */
function runLouvain(graphData: GraphData): Map<string, number> {
  const graph = buildWeightedGraph(graphData);

  if (graph.nodes.size === 0) {
    return new Map();
  }

  let changed = true;
  let phase = 0;
  const maxPhases = 10;

  // Track original node IDs to their communities
  const originalCommunities = new Map<string, number>();

  while (changed && phase < maxPhases) {
    changed = louvainPhase(graph);

    if (changed) {
      // Store community assignments before aggregation
      if (phase === 0) {
        graph.nodes.forEach((node, id) => {
          originalCommunities.set(id, node.community);
        });
      }

      // Aggregate for next phase
      // This is simplified - in full implementation would track hierarchical communities
      phase++;
    }
  }

  // If no aggregation happened, use final communities
  if (originalCommunities.size === 0) {
    graph.nodes.forEach((node, id) => {
      originalCommunities.set(id, node.community);
    });
  }

  return originalCommunities;
}

/**
 * Calculate cluster statistics
 */
function calculateClusterStats(
  graphData: GraphData,
  nodeCommunities: Map<string, number>,
): ClusterInfo[] {
  const clusters = new Map<number, ClusterInfo>();
  const senatorNodes = graphData.nodes.filter((n) => n.data.type === "senator");

  // Initialize clusters
  nodeCommunities.forEach((communityId) => {
    if (!clusters.has(communityId)) {
      clusters.set(communityId, {
        id: communityId,
        name: `Cluster ${communityId + 1}`,
        color: CLUSTER_COLORS[communityId % CLUSTER_COLORS.length],
        size: 0,
        cohesion: 0,
        partyBreakdown: {},
        avgAgreement: 0,
      });
    }
  });

  // Count cluster sizes and party breakdown
  senatorNodes.forEach((node) => {
    const communityId = nodeCommunities.get(node.data.id);
    if (communityId === undefined) return;

    const cluster = clusters.get(communityId);
    if (!cluster) return;

    cluster.size++;

    const party = node.data.party || "Unknown";
    cluster.partyBreakdown[party] = (cluster.partyBreakdown[party] || 0) + 1;
  });

  // Calculate internal edge weights for cohesion
  graphData.edges
    .filter((edge) => edge.data.type === "voted_same")
    .forEach((edge) => {
      const sourceCommunity = nodeCommunities.get(edge.data.source);
      const targetCommunity = nodeCommunities.get(edge.data.target);

      if (
        sourceCommunity !== undefined &&
        sourceCommunity === targetCommunity
      ) {
        const cluster = clusters.get(sourceCommunity);
        if (cluster) {
          cluster.avgAgreement += (edge.data.agreement as number) || 0;
        }
      }
    });

  // Calculate average agreements
  clusters.forEach((cluster) => {
    const internalEdges = Object.values(cluster.partyBreakdown).reduce(
      (sum, count) => sum + (count * (count - 1)) / 2,
      0,
    );
    if (internalEdges > 0) {
      cluster.avgAgreement /= internalEdges;
    }
    cluster.cohesion = cluster.avgAgreement;
  });

  return Array.from(clusters.values()).sort((a, b) => b.size - a.size);
}

/**
 * Detect voting pattern clusters using Louvain algorithm
 */
export function detectVotingClusters(graphData: GraphData): {
  nodes: GraphNode[];
  clusters: ClusterInfo[];
} {
  // Run Louvain algorithm
  const nodeCommunities = runLouvain(graphData);

  // Assign cluster IDs and colors to nodes
  const clusteredNodes = graphData.nodes.map((node) => {
    if (node.data.type !== "senator") {
      return node;
    }

    const clusterId = nodeCommunities.get(node.data.id);
    if (clusterId === undefined) {
      return node;
    }

    return {
      ...node,
      data: {
        ...node.data,
        clusterId,
        clusterColor: CLUSTER_COLORS[clusterId % CLUSTER_COLORS.length],
      },
    };
  });

  // Calculate cluster statistics
  const clusters = calculateClusterStats(graphData, nodeCommunities);

  return { nodes: clusteredNodes, clusters };
}

/**
 * Get color for a cluster
 */
export function getClusterColor(clusterId: number): string {
  return CLUSTER_COLORS[clusterId % CLUSTER_COLORS.length];
}

/**
 * Calculate voting similarity between two senators
 */
export function calculateVotingSimilarity(
  graphData: GraphData,
  senatorId1: string,
  senatorId2: string,
): number {
  const edge = graphData.edges.find(
    (e) =>
      e.data.type === "voted_same" &&
      ((e.data.source === senatorId1 && e.data.target === senatorId2) ||
        (e.data.source === senatorId2 && e.data.target === senatorId1)),
  );

  return (edge?.data.agreement as number) || 0;
}
