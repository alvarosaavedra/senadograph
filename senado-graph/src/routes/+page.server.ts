import {
  getAllSenators,
  getAllParties,
  getAllCommittees,
  getSenatorCount,
  getPartyCount,
  getLawCount,
  getCommitteeCount,
  getPartyBreakdown,
  getLawStatusBreakdown,
} from "$lib/database/queries";
import type { Senator, GraphData } from "$lib/types";
import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async () => {
  try {
    // Fetch senators list and basic data
    const [senators, parties, committees] = await Promise.all([
      getAllSenators(),
      getAllParties(),
      getAllCommittees(),
    ]);

    // Fetch individual stats for StatsCards
    const [
      senatorCount,
      partyCount,
      lawCount,
      committeeCount,
      partyBreakdown,
      lawStatusBreakdown,
    ] = await Promise.all([
      getSenatorCount(),
      getPartyCount(),
      getLawCount(),
      getCommitteeCount(),
      getPartyBreakdown(),
      getLawStatusBreakdown(),
    ]);

    return {
      senators,
      parties,
      committees,
      stats: {
        senatorCount,
        partyCount,
        lawCount,
        committeeCount,
        partyBreakdown,
        lawStatusBreakdown,
      },
    };
  } catch (err) {
    console.error("Error loading home page data:", err);
    return {
      senators: [] as Senator[],
      parties: [],
      committees: [],
      stats: {
        senatorCount: 0,
        partyCount: 0,
        lawCount: 0,
        committeeCount: 0,
        partyBreakdown: [],
        lawStatusBreakdown: [],
      },
    };
  }
};
