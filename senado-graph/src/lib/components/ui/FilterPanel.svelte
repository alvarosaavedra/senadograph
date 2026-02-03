<script lang="ts">
  import type { GraphFilters, NodeType, LawStatus, LobbyistType, EdgeType } from '$lib/types';
  import PresetSelector from './PresetSelector.svelte';

  export let parties: { id: string; name: string; color?: string }[] = [];
  export let committees: { id: string; name: string }[] = [];
  export let currentFilters: GraphFilters = {};
  export let onApplyFilters: (filters: GraphFilters) => void;
  export let onClose: () => void;

  let selectedParties: string[] = [];
  let selectedCommittee: string = '';
  let startDate: string = '';
  let endDate: string = '';
  let activeOnly: boolean = false;

  let entityTypes: NodeType[] = ['senator', 'law', 'party', 'committee', 'lobbyist'];
  let lawStatuses: LawStatus[] = ['approved', 'rejected', 'in_discussion', 'withdrawn'];
  let selectedLawStatuses: LawStatus[] = [];
  let agreementMin: number = 0;
  let agreementMax: number = 100;
  let lobbyistTypes: LobbyistType[] = ['company', 'union', 'ngo', 'professional_college'];
  let selectedLobbyistTypes: LobbyistType[] = [];

  // Relationship types
  const relationshipTypesConfig: { type: EdgeType; label: string; color: string; description: string }[] = [
    { type: 'authored', label: 'Authored', color: '#3b82f6', description: 'Senators who authored a law' },
    { type: 'belongs_to', label: 'Belongs to', color: '#94a3b8', description: 'Senator party membership' },
    { type: 'member_of', label: 'Member of', color: '#8b5cf6', description: 'Committee membership' },
    { type: 'lobby', label: 'Lobby', color: '#f97316', description: 'Lobbyist influence on senators' },
    { type: 'voted_same', label: 'Voting agreement', color: '#10b981', description: 'Similar voting patterns between senators' },
    { type: 'voted_on', label: 'Voted on', color: '#ef4444', description: 'How senators voted on laws' }
  ];
  let selectedRelationshipTypes: EdgeType[] = ['authored', 'belongs_to', 'member_of', 'lobby', 'voted_same', 'voted_on'];

  // Sync with currentFilters when it changes
  $: if (currentFilters.parties) {
    selectedParties = currentFilters.parties;
  }
  $: if (currentFilters.committees && currentFilters.committees.length > 0) {
    selectedCommittee = currentFilters.committees[0];
  } else if (!currentFilters.committees) {
    selectedCommittee = '';
  }
  $: if (currentFilters.dateRange) {
    startDate = currentFilters.dateRange.start;
    endDate = currentFilters.dateRange.end;
  }
  $: if (currentFilters.activeOnly !== undefined) {
    activeOnly = currentFilters.activeOnly;
  }
  $: if (currentFilters.entityTypes) {
    entityTypes = currentFilters.entityTypes;
  }
  $: if (currentFilters.lawStatuses) {
    selectedLawStatuses = currentFilters.lawStatuses;
  } else {
    selectedLawStatuses = [];
  }
  $: if (currentFilters.agreementRange) {
    agreementMin = Math.round(currentFilters.agreementRange.min * 100);
    agreementMax = Math.round(currentFilters.agreementRange.max * 100);
  }
  $: if (currentFilters.lobbyistTypes) {
    selectedLobbyistTypes = currentFilters.lobbyistTypes;
  } else {
    selectedLobbyistTypes = [];
  }
  $: if (currentFilters.relationshipTypes) {
    selectedRelationshipTypes = currentFilters.relationshipTypes;
  } else {
    selectedRelationshipTypes = ['authored', 'belongs_to', 'member_of', 'lobby', 'voted_same', 'voted_on'];
  }

  function handleApply() {
    const filters: GraphFilters = {
      parties: selectedParties.length > 0 ? selectedParties : undefined,
      committees: selectedCommittee ? [selectedCommittee] : undefined,
      dateRange:
        startDate && endDate
          ? { start: startDate, end: endDate }
          : undefined,
      activeOnly,
      entityTypes,
      lawStatuses: selectedLawStatuses.length > 0 ? selectedLawStatuses : undefined,
      agreementRange: { min: agreementMin / 100, max: agreementMax / 100 },
      lobbyistTypes: selectedLobbyistTypes.length > 0 ? selectedLobbyistTypes : undefined,
      relationshipTypes: selectedRelationshipTypes
    };
    onApplyFilters(filters);
    onClose();
  }

  function handleApplyPreset(presetId: string) {
    const { applyPreset } = import('$lib/config/presets');
    const presetFilters = applyPreset(presetId);
    if (presetFilters) {
      onApplyFilters(presetFilters);
      onClose();
    }
  }

  function handlePresetReset() {
    handleClear();
  }

  function handleClear() {
    selectedParties = [];
    selectedCommittee = '';
    startDate = '';
    endDate = '';
    activeOnly = false;
    entityTypes = ['senator', 'law', 'party', 'committee', 'lobbyist'];
    selectedLawStatuses = [];
    agreementMin = 0;
    agreementMax = 100;
    selectedLobbyistTypes = [];
    selectedRelationshipTypes = ['authored', 'belongs_to', 'member_of', 'lobby', 'voted_same', 'voted_on'];
    onApplyFilters({});
  }

  function toggleParty(partyId: string) {
    if (selectedParties.includes(partyId)) {
      selectedParties = selectedParties.filter((id) => id !== partyId);
    } else {
      selectedParties = [...selectedParties, partyId];
    }
  }

  function toggleEntityType(type: NodeType) {
    if (entityTypes.includes(type)) {
      entityTypes = entityTypes.filter((t) => t !== type);
    } else {
      entityTypes = [...entityTypes, type];
    }
  }

  function toggleLawStatus(status: LawStatus) {
    if (selectedLawStatuses.includes(status)) {
      selectedLawStatuses = selectedLawStatuses.filter((s) => s !== status);
    } else {
      selectedLawStatuses = [...selectedLawStatuses, status];
    }
  }

  function toggleLobbyistType(type: LobbyistType) {
    if (selectedLobbyistTypes.includes(type)) {
      selectedLobbyistTypes = selectedLobbyistTypes.filter((t) => t !== type);
    } else {
      selectedLobbyistTypes = [...selectedLobbyistTypes, type];
    }
  }

  function toggleRelationshipType(type: EdgeType) {
    if (selectedRelationshipTypes.includes(type)) {
      selectedRelationshipTypes = selectedRelationshipTypes.filter((t) => t !== type);
    } else {
      selectedRelationshipTypes = [...selectedRelationshipTypes, type];
    }
  }
</script>

<div class="glass-panel rounded-2xl p-6 w-full max-w-md animate-fade-in-up shadow-glow relative max-h-[85vh] flex flex-col">
  <button
    on:click={onClose}
    class="absolute top-4 right-4 p-1 rounded-lg hover:bg-gray-100 transition-colors z-10"
    aria-label="Close filters"
  >
    <svg class="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
    </svg>
  </button>

  <h3 class="text-xl font-bold gradient-text mb-4 pr-8 flex-shrink-0">
    Filters
  </h3>

  <div class="space-y-4 overflow-y-auto pr-2 flex-1">
    <!-- Presets -->
    <div class="border-b border-gray-200 pb-4">
      <PresetSelector
        onApplyPreset={handleApplyPreset}
        onReset={handlePresetReset}
      />
    </div>

    <!-- Entity Types -->
    <div>
      <span class="block text-sm font-medium text-gray-700 mb-3">
        Show Entities
      </span>
      <div class="flex flex-wrap gap-2">
        {#each ['senator', 'law', 'party', 'committee', 'lobbyist'] as type}
          <button
            on:click={() => toggleEntityType(type as NodeType)}
            class:active={entityTypes.includes(type as NodeType)}
            class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-300 border border-gray-200"
          >
            {type.replace('_', ' ').replace('senator', 'Senator').replace('law', 'Law').replace('party', 'Party').replace('committee', 'Committee').replace('lobbyist', 'Lobbyist')}
          </button>
        {/each}
      </div>
    </div>

    <!-- Connection Types -->
    <div>
      <span class="block text-sm font-medium text-gray-700 mb-2">
        Connection Types
      </span>
      <div class="grid grid-cols-2 gap-2">
        {#each relationshipTypesConfig as config}
          <button
            on:click={() => toggleRelationshipType(config.type)}
            class="px-2 py-1.5 rounded-lg text-xs font-medium transition-all duration-300 border flex items-center gap-1.5"
            class:authored={config.type === 'authored'}
            style="background-color: {selectedRelationshipTypes.includes(config.type) ? config.color : 'transparent'}; color: {selectedRelationshipTypes.includes(config.type) ? 'white' : '#374151'}; border-color: {config.color}"
            title={config.description}
          >
            <span class="w-1.5 h-1.5 rounded-full flex-shrink-0" style="background-color: {selectedRelationshipTypes.includes(config.type) ? 'white' : config.color}"></span>
            <span class="truncate">{config.label}</span>
          </button>
        {/each}
      </div>
      <p class="text-xs text-gray-500 mt-2 italic">Hover over buttons for descriptions</p>
    </div>

    <!-- Parties -->
    <div>
      <span class="block text-sm font-medium text-gray-700 mb-3">
        Party
      </span>
      <div class="space-y-2 max-h-48 overflow-y-auto pr-2" role="group" aria-label="Party">
        {#each parties as party}
          <label class="flex items-center space-x-3 cursor-pointer hover:bg-white/50 p-2 rounded-lg transition-colors">
            <input
              type="checkbox"
              checked={selectedParties.includes(party.id)}
              on:change={() => toggleParty(party.id)}
              class="w-5 h-5 text-primary-600 border-gray-300 rounded focus:ring-primary-500 focus:ring-offset-0"
            />
            <span
              class="w-4 h-4 rounded-full shadow-sm"
              style="background-color: {party.color || '#ccc'}"
            ></span>
            <span class="text-sm text-gray-700">{party.name}</span>
          </label>
        {/each}
      </div>
    </div>

    <!-- Committee -->
    <div>
      <label for="committee-select" class="block text-sm font-medium text-gray-700 mb-3">
        Committee
      </label>
      <select
        id="committee-select"
        bind:value={selectedCommittee}
        class="w-full px-4 py-2 bg-white/50 border border-white/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent backdrop-blur-sm"
      >
        <option value="">Clear</option>
        {#each committees as committee}
          <option value={committee.id}>{committee.name}</option>
        {/each}
      </select>
    </div>

    <!-- Law Statuses -->
    {#if entityTypes.includes('law')}
      <div>
        <span class="block text-sm font-medium text-gray-700 mb-3">
          Law Status
        </span>
        <div class="flex flex-wrap gap-2">
          {#each ['approved', 'rejected', 'in_discussion', 'withdrawn'] as status}
            <button
              on:click={() => toggleLawStatus(status as LawStatus)}
              class:active={selectedLawStatuses.includes(status as LawStatus)}
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-300 border border-gray-200"
            >
              {status.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </button>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Agreement Range -->
    {#if entityTypes.includes('senator')}
      <div>
        <span class="block text-sm font-medium text-gray-700 mb-3">
          Voting Agreement: {agreementMin}% - {agreementMax}%
        </span>
        <input
          type="range"
          min="0"
          max="100"
          bind:value={agreementMin}
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-500"
        />
        <input
          type="range"
          min="0"
          max="100"
          bind:value={agreementMax}
          class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-primary-500"
        />
      </div>
    {/if}

    <!-- Lobbyist Types -->
    {#if entityTypes.includes('lobbyist')}
      <div>
        <span class="block text-sm font-medium text-gray-700 mb-3">
          Lobbyist Type
        </span>
        <div class="flex flex-wrap gap-2">
          {#each ['company', 'union', 'ngo', 'professional_college'] as type}
            <button
              on:click={() => toggleLobbyistType(type as LobbyistType)}
              class:active={selectedLobbyistTypes.includes(type as LobbyistType)}
              class="px-3 py-1.5 rounded-lg text-xs font-medium transition-all duration-300 border border-gray-200"
            >
              {type.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
            </button>
          {/each}
        </div>
      </div>
    {/if}

    <!-- Date Range -->
    <div>
      <span class="block text-sm font-medium text-gray-700 mb-3">
        Date Range
      </span>
      <div class="space-y-2">
        <input
          type="date"
          bind:value={startDate}
          aria-label="Start date"
          class="w-full px-4 py-2 bg-white/50 border border-white/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent backdrop-blur-sm"
        />
        <input
          type="date"
          bind:value={endDate}
          aria-label="End date"
          class="w-full px-4 py-2 bg-white/50 border border-white/30 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent backdrop-blur-sm"
        />
      </div>
    </div>

    <label class="flex items-center space-x-3 cursor-pointer p-2 rounded-lg hover:bg-white/50 transition-colors">
      <input
        type="checkbox"
        bind:checked={activeOnly}
        class="w-5 h-5 text-primary-600 border-gray-300 rounded focus:ring-primary-500 focus:ring-offset-0"
      />
      <span class="text-sm text-gray-700">Active Only</span>
    </label>

    <div class="flex gap-3 pt-4">
      <button
        on:click={handleApply}
        class="flex-1 px-6 py-2.5 bg-gradient-primary text-white text-sm font-medium rounded-lg hover:shadow-glow transition-all duration-300 hover:scale-105 active:scale-95"
      >
        Apply
      </button>
      <button
        on:click={handleClear}
        class="flex-1 px-6 py-2.5 bg-gray-200 text-gray-700 text-sm font-medium rounded-lg hover:bg-gray-300 transition-colors hover:scale-105 active:scale-95 duration-300"
      >
        Clear
      </button>
    </div>
  </div>
</div>

<style>
  .active {
    @apply bg-gradient-primary text-white border-transparent;
  }
  .authored {
    @apply font-bold shadow-sm;
    transform: scale(1.02);
  }
</style>
