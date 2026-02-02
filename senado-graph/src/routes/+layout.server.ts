import { getAllParties, getAllCommittees } from "$lib/database/queries";
import type { Party, Committee } from "$lib/types";
import type { LayoutServerLoad } from "./$types";

export const load: LayoutServerLoad = async () => {
  try {
    const [parties, committees] = await Promise.all([
      getAllParties(),
      getAllCommittees(),
    ]);

    return {
      parties,
      committees,
    };
  } catch (err) {
    console.error("Error loading layout data:", err);
    return {
      parties: [] as Party[],
      committees: [] as Committee[],
    };
  }
};
