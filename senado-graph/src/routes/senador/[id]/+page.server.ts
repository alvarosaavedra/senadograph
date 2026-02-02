import { error } from "@sveltejs/kit";
import {
  getSenatorById,
  getLawsForSenator,
  getCommitteesForSenator,
} from "$lib/database/queries";
import type { PageServerLoad } from "./$types";

export const prerender = true;

export const load: PageServerLoad = async ({ params }) => {
  try {
    const [senator, laws, committees] = await Promise.all([
      getSenatorById(params.id),
      getLawsForSenator(params.id),
      getCommitteesForSenator(params.id),
    ]);

    if (!senator) {
      throw error(404, "Senator not found");
    }

    return {
      senator,
      laws,
      committees,
    };
  } catch (err) {
    console.error("Error loading senator data:", err);
    throw error(500, "Failed to load senator data");
  }
};
