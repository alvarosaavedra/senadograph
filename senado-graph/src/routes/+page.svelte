<script lang="ts">
  import type { GraphData } from '$lib/types';
  import CytoscapeGraph from '$lib/components/graph/CytoscapeGraph.svelte';
  import GraphControls from '$lib/components/graph/GraphControls.svelte';
  import FilterPanel from '$lib/components/ui/FilterPanel.svelte';
  import SearchBar from '$lib/components/ui/SearchBar.svelte';
  import DataDisclaimer from '$lib/components/ui/DataDisclaimer.svelte';
  import { filterStore, searchQuery, updateFilters, clearFilters } from '$lib/stores/filters';
  import { goto } from '$app/navigation';
  import type { GraphFilters } from '$lib/types';
  import type { SearchResult } from '$lib/components/ui/SearchBar.svelte';
  
  export let data;
  
  $: ({ senators, graphData, parties, committees } = data);
  
  let graphComponent: CytoscapeGraph;
  let currentGraphData: GraphData = graphData || { nodes: [], edges: [] };
  let showFilters = false;
  let searchResults: SearchResult[] = [];
  
  function handleNodeClick(nodeId: string, type: string) {
    if (type === 'senator') {
      goto(`/senador/${nodeId}`);
    } else if (type === 'law') {
      goto(`/ley/${nodeId}`);
    }
  }
  
  async function handleApplyFilters(filters: GraphFilters) {
    updateFilters(filters);
    
    try {
      const res = await fetch('/api/graph', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(filters)
      });
      
      if (!res.ok) throw new Error('Failed to fetch filtered data');
      currentGraphData = await res.json();
    } catch (err) {
      console.error('Error applying filters:', err);
    }
  }
  
  function handleClearFilters() {
    clearFilters();
    currentGraphData = graphData;
  }
  
  function handleSearch(query: string) {
    searchQuery.set(query);
    // Simple client-side search for demo
    const senatorResults: SearchResult[] = senators.map(s => ({ 
      type: 'senator' as const, 
      id: s.id, 
      name: s.name,
      party: s.party 
    }));
    const partyResults: SearchResult[] = parties.map(p => ({ 
      type: 'party' as const, 
      id: p.id, 
      name: p.name,
      shortName: p.shortName 
    }));
    
    searchResults = [...senatorResults, ...partyResults].filter(item => {
      const itemName = item.type === 'law' ? item.title : item.name;
      return itemName.toLowerCase().includes(query.toLowerCase());
    }).slice(0, 5);
  }
  
  function handleSearchSelect(event: CustomEvent) {
    const item = event.detail;
    if (item.type === 'senator') {
      goto(`/senador/${item.id}`);
    }
  }
</script>

<svelte:head>
  <title>SenadoGraph</title>
  <meta name="description" content="Chilean Senate Relationship Visualization" />
</svelte:head>

<!-- Data Disclaimer -->
<DataDisclaimer />

<!-- Hero Section -->
<div class="text-center mb-8">
  <h1 class="text-4xl font-bold text-gray-900 mb-4">
    SenadoGraph
  </h1>
  <p class="text-xl text-gray-600 max-w-2xl mx-auto">
    Chilean Senate Relationship Visualization
  </p>
</div>

<!-- Search Bar -->
<div class="mb-6">
  <SearchBar 
    onSearch={handleSearch}
    results={searchResults}
    placeholder="Search senators, parties..."
    on:select={handleSearchSelect}
  />
</div>

<!-- Controls Bar -->
<div class="flex justify-between items-center mb-4">
  <button
    on:click={() => showFilters = !showFilters}
    class="flex items-center space-x-2 px-4 py-2 bg-white border border-gray-300 rounded-md shadow-sm hover:bg-gray-50 transition-colors"
  >
    <svg class="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
    </svg>
    <span class="text-gray-700">Filters</span>
    {#if ($filterStore.parties && $filterStore.parties.length > 0) || ($filterStore.committees && $filterStore.committees.length > 0)}
      <span class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded-full">
        {($filterStore.parties?.length || 0) + ($filterStore.committees?.length || 0)}
      </span>
    {/if}
  </button>
  
  <p class="text-sm text-gray-500">
    {currentGraphData?.nodes?.length || 0} senators
  </p>
</div>

<!-- Filter Panel -->
{#if showFilters}
  <div class="mb-6">
    <FilterPanel 
      {parties}
      {committees}
      onApplyFilters={handleApplyFilters}
    />
  </div>
{/if}

<!-- Graph Visualization -->
<div class="bg-white rounded-lg shadow-md overflow-hidden mb-8">
  <div class="relative h-[600px]">
    <CytoscapeGraph 
      bind:this={graphComponent}
      graphData={currentGraphData} 
      onNodeClick={handleNodeClick} 
    />
    <GraphControls 
      onZoomIn={() => graphComponent?.zoomIn()}
      onZoomOut={() => graphComponent?.zoomOut()}
      onFit={() => graphComponent?.fit()}
      onResetLayout={() => graphComponent?.resetLayout()}
    />
  </div>
</div>

<!-- Senator List -->
<div class="bg-white rounded-lg shadow-md overflow-hidden">
  <div class="px-6 py-4 border-b border-gray-200">
    <h2 class="text-lg font-semibold text-gray-900">Senators</h2>
  </div>
  
  <div class="divide-y divide-gray-200">
    {#each senators.slice(0, 10) as senator}
      <a 
        href="/senador/{senator.id}" 
        class="block px-6 py-4 hover:bg-gray-50 transition-colors"
      >
        <div class="flex items-center justify-between">
          <div>
            <h3 class="text-sm font-medium text-gray-900">{senator.name}</h3>
            <p class="text-sm text-gray-500">{senator.party} • {senator.region}</p>
          </div>
          <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </div>
      </a>
    {/each}
  </div>
  
  {#if senators.length > 10}
    <div class="px-6 py-4 border-t border-gray-200">
      <p class="text-sm text-gray-500 text-center">
        {senators.length - 10} more...
      </p>
    </div>
  {/if}
</div>
