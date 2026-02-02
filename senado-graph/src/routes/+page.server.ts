import { getAllSenators, getInitialGraphData } from "$lib/database/queries";
import type { Senator, GraphData } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  try {
    const [senators, graphData] = await Promise.all([
      getAllSenators(),
      getInitialGraphData(),
    ]);

    return {
      senators,
      graphData,
    };
  } catch (err) {
    console.error("Error loading home page data:", err);
    return {
      senators: [] as Senator[],
      graphData: { nodes: [], edges: [] } as GraphData,
    };
  }
};
