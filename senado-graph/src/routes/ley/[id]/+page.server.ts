import { error } from "@sveltejs/kit";
import { getLawById, getAuthorsForLaw } from "$lib/database/queries";
import type { PageServerLoad } from "./$types";

export const prerender = true;

export const load: PageServerLoad = async ({ params }) => {
  try {
    const [law, authors] = await Promise.all([
      getLawById(params.id),
      getAuthorsForLaw(params.id),
    ]);

    if (!law) {
      throw error(404, "Law not found");
    }

    return {
      law,
      authors,
    };
  } catch (err) {
    console.error("Error loading law data:", err);
    throw error(500, "Failed to load law data");
  }
};
