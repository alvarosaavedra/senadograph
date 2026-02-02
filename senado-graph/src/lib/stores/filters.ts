import { writable } from 'svelte/store';
import type { GraphFilters } from '$lib/types';

export const filterStore = writable<GraphFilters>({
  parties: [],
  committees: [],
  dateRange: undefined,
  topics: [],
  relationshipTypes: [],
  activeOnly: true
});

export const searchQuery = writable<string>('');
export const searchResults = writable<Array<{id: string; name: string; type: string}>>([]);

export function updateFilters(filters: GraphFilters) {
  filterStore.set(filters);
}

export function clearFilters() {
  filterStore.set({
    parties: [],
    committees: [],
    dateRange: undefined,
    topics: [],
    relationshipTypes: [],
    activeOnly: true
  });
}
