import {
  getAllSenators,
  getAllParties,
  getAllCommittees,
  getInitialGraphData,
  getVotingSimilarityGraph,
} from "$lib/database/queries";
import type { GraphData, Senator, Party, Committee } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  try {
    // Fetch base data
    const [senators, parties, committees] = await Promise.all([
      getAllSenators(),
      getAllParties(),
      getAllCommittees(),
    ]);

    // Fetch initial graph data (for display)
    const initialGraphData = await getInitialGraphData();

    // Fetch voting similarity graph (for clustering analysis)
    const votingGraphData = await getVotingSimilarityGraph();

    return {
      senators,
      parties,
      committees,
      initialGraphData,
      votingGraphData,
    };
  } catch (err) {
    console.error("Error loading graph page data:", err);
    return {
      senators: [] as Senator[],
      parties: [] as Party[],
      committees: [] as Committee[],
      initialGraphData: { nodes: [], edges: [] } as GraphData,
      votingGraphData: { nodes: [], edges: [] } as GraphData,
    };
  }
};
