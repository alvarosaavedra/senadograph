import {
  getAllSenators,
  getInitialGraphData,
  getAllParties,
  getAllCommittees,
} from "$lib/database/queries";
import type { Senator, GraphData } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  try {
    const [senators, graphData, parties, committees] = await Promise.all([
      getAllSenators(),
      getInitialGraphData(["approved", "rejected", "withdrawn"]),
      getAllParties(),
      getAllCommittees(),
    ]);

    return {
      senators,
      graphData,
      parties,
      committees,
    };
  } catch (err) {
    console.error("Error loading home page data:", err);
    return {
      senators: [] as Senator[],
      graphData: { nodes: [], edges: [] } as GraphData,
      parties: [],
      committees: [],
    };
  }
};
