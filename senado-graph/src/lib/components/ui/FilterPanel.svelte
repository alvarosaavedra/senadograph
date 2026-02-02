<script lang="ts">
  import type { GraphFilters } from '$lib/types';

  export let parties: { id: string; name: string; color?: string }[] = [];
  export let committees: { id: string; name: string }[] = [];
  export let onApplyFilters: (filters: GraphFilters) => void;

  let selectedParties: string[] = [];
  let selectedCommittee: string = '';
  let startDate: string = '';
  let endDate: string = '';
  let activeOnly: boolean = false;

  function handleApply() {
    const filters: GraphFilters = {
      parties: selectedParties.length > 0 ? selectedParties : undefined,
      committees: selectedCommittee ? [selectedCommittee] : undefined,
      dateRange:
        startDate && endDate
          ? { start: startDate, end: endDate }
          : undefined,
      activeOnly,
    };
    onApplyFilters(filters);
  }

  function handleClear() {
    selectedParties = [];
    selectedCommittee = '';
    startDate = '';
    endDate = '';
    activeOnly = false;
    onApplyFilters({});
  }

  function toggleParty(partyId: string) {
    if (selectedParties.includes(partyId)) {
      selectedParties = selectedParties.filter((id) => id !== partyId);
    } else {
      selectedParties = [...selectedParties, partyId];
    }
  }
</script>

<div class="bg-white rounded-lg shadow-md p-4 w-full max-w-xs">
  <h3 class="text-lg font-semibold text-gray-800 mb-4">
    Filters
  </h3>

  <div class="space-y-4">
    <div>
      <span class="block text-sm font-medium text-gray-700 mb-2">
        Party
      </span>
      <div class="space-y-2 max-h-40 overflow-y-auto" role="group" aria-label="Party">
        {#each parties as party}
          <label class="flex items-center space-x-2 cursor-pointer hover:bg-gray-50 p-1 rounded">
            <input
              type="checkbox"
              checked={selectedParties.includes(party.id)}
              on:change={() => toggleParty(party.id)}
              class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
            />
            <span
              class="w-3 h-3 rounded-full"
              style="background-color: {party.color || '#ccc'}"
            ></span>
            <span class="text-sm text-gray-700">{party.name}</span>
          </label>
        {/each}
      </div>
    </div>

    <div>
      <label for="committee-select" class="block text-sm font-medium text-gray-700 mb-2">
        Committee
      </label>
      <select
        id="committee-select"
        bind:value={selectedCommittee}
        class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      >
        <option value="">Clear</option>
        {#each committees as committee}
          <option value={committee.id}>{committee.name}</option>
        {/each}
      </select>
    </div>

    <div>
      <span class="block text-sm font-medium text-gray-700 mb-2">
        Date Range
      </span>
      <div class="space-y-2">
        <input
          type="date"
          bind:value={startDate}
          aria-label="Start date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        <input
          type="date"
          bind:value={endDate}
          aria-label="End date"
          class="w-full px-3 py-2 border border-gray-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
      </div>
    </div>

    <label class="flex items-center space-x-2 cursor-pointer">
      <input
        type="checkbox"
        bind:checked={activeOnly}
        class="w-4 h-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500"
      />
      <span class="text-sm text-gray-700">Active Only</span>
    </label>

    <div class="flex gap-2 pt-2">
      <button
        on:click={handleApply}
        class="flex-1 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-md hover:bg-blue-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Apply
      </button>
      <button
        on:click={handleClear}
        class="flex-1 px-4 py-2 bg-gray-200 text-gray-700 text-sm font-medium rounded-md hover:bg-gray-300 transition-colors focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
      >
        Clear
      </button>
    </div>
  </div>
</div>
