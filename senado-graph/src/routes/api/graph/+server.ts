import { error } from '@sveltejs/kit';
import { getFilteredGraphData } from '$lib/utils/graphData';
import type { RequestHandler } from './$types';
import type { GraphFilters } from '$lib/types';

export const POST: RequestHandler = async ({ request }) => {
  try {
    const filters: GraphFilters = await request.json();
    const graphData = await getFilteredGraphData(filters);
    
    return new Response(JSON.stringify(graphData), {
      headers: {
        'Content-Type': 'application/json'
      }
    });
  } catch (err) {
    console.error('Error fetching graph data:', err);
    throw error(500, 'Failed to fetch graph data');
  }
};
