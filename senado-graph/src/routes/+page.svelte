<script lang="ts">
  import type { GraphData, NodeType, EdgeType } from '$lib/types';
  import CytoscapeGraph from '$lib/components/graph/CytoscapeGraph.svelte';
  import GraphControls from '$lib/components/graph/GraphControls.svelte';
  import GraphLegend from '$lib/components/graph/GraphLegend.svelte';
  import NodeDetailsPanel from '$lib/components/graph/NodeDetailsPanel.svelte';
  import FilterPanel from '$lib/components/ui/FilterPanel.svelte';
  import SearchBar from '$lib/components/ui/SearchBar.svelte';
  import DataDisclaimer from '$lib/components/ui/DataDisclaimer.svelte';
  import StatsCards from '$lib/components/dashboard/StatsCards.svelte';
  import { filterStore, searchQuery, updateFilters, clearFilters } from '$lib/stores/filters';
  import { goto } from '$app/navigation';
  import type { GraphFilters } from '$lib/types';
  import type { SearchResult } from '$lib/components/ui/SearchBar.svelte';
  import { getMockSenators, getMockLaws } from '$lib/database/mockData';

   export let data;

   let graphComponent: CytoscapeGraph;
   let currentGraphData: GraphData;
   let showFilters = false;
   let searchResults: SearchResult[] = [];
   let showNodeDetails = false;
   let selectedNode: any = null;
   let currentFilters: GraphFilters = {
    lawStatuses: ['approved', 'rejected', 'withdrawn'],
    relationshipTypes: ['authored', 'belongs_to', 'member_of', 'lobby', 'voted_same', 'voted_on']
   };

   $: ({ senators, graphData, parties, committees } = data);

     // Initialize currentGraphData when data loads
     $: if (graphData && !currentGraphData) {
       console.log('Page: Initializing currentGraphData', graphData);
       currentGraphData = graphData;
     }

  $: partyBreakdown = (() => {
    const dataToUse = currentGraphData || graphData;
    const visibleParties = dataToUse?.nodes?.filter(n => n.data.type === 'party') || [];
    const visibleSenators = dataToUse?.nodes?.filter(n => n.data.type === 'senator') || [];
    return visibleParties.map(p => ({
      name: p.data.label,
      count: visibleSenators.filter(s => s.data.party === p.data.label).length,
      color: p.data.color
    })).filter(p => p.count > 0).sort((a, b) => b.count - a.count);
  })();

   $: lawStatusBreakdown = (() => {
     const dataToUse = currentGraphData || graphData;
     const laws = dataToUse?.nodes?.filter(n => n.data.type === 'law') || [];
     const statusCounts = { approved: 0, in_discussion: 0, rejected: 0, withdrawn: 0 };
     laws.forEach(law => {
       const status = law.data.status;
       if (status && statusCounts.hasOwnProperty(status)) {
         statusCounts[status]++;
       }
     });
     return [
       { status: 'approved', count: statusCounts.approved },
       { status: 'in_discussion', count: statusCounts.in_discussion },
       { status: 'rejected', count: statusCounts.rejected },
       { status: 'withdrawn', count: statusCounts.withdrawn }
     ].filter(s => s.count > 0);
   })();

   $: nodeCounts = {
    senators: (currentGraphData || graphData)?.nodes?.filter(n => n.data.type === 'senator').length || 0,
    laws: (currentGraphData || graphData)?.nodes?.filter(n => n.data.type === 'law').length || 0,
    parties: (currentGraphData || graphData)?.nodes?.filter(n => n.data.type === 'party').length || 0,
    committees: (currentGraphData || graphData)?.nodes?.filter(n => n.data.type === 'committee').length || 0,
    lobbyists: (currentGraphData || graphData)?.nodes?.filter(n => n.data.type === 'lobbyist').length || 0
  };

   $: edgeCounts = {
    authored: (currentGraphData || graphData)?.edges?.filter(e => e.data.type === 'authored').length || 0,
    member_of: (currentGraphData || graphData)?.edges?.filter(e => e.data.type === 'member_of').length || 0,
    belongs_to: (currentGraphData || graphData)?.edges?.filter(e => e.data.type === 'belongs_to').length || 0,
    lobby: (currentGraphData || graphData)?.edges?.filter(e => e.data.type === 'lobby').length || 0,
    voted_same: (currentGraphData || graphData)?.edges?.filter(e => e.data.type === 'voted_same').length || 0,
    voted_on: (currentGraphData || graphData)?.edges?.filter(e => e.data.type === 'voted_on').length || 0
   };

  $: if (graphData) {
    console.log('Page: graphData available, setting currentGraphData', graphData);
    currentGraphData = graphData;
  }

  function handleNodeClick(nodeId: string, type: string) {
    const dataToUse = currentGraphData || graphData;
    const node = dataToUse?.nodes?.find(n => n.data.id === nodeId);
    if (!node) return;

    selectedNode = node.data;

    if (type === 'senator') {
      showNodeDetails = true;
    } else if (type === 'law') {
      showNodeDetails = true;
    } else {
      showNodeDetails = true;
    }
  }

  function getConnectedNodes(nodeId: string) {
    const dataToUse = currentGraphData || graphData;
    if (!dataToUse) return [];

    const connectedEdges = dataToUse.edges.filter(e =>
      e.data.source === nodeId || e.data.target === nodeId
    );

    return connectedEdges.map(edge => {
      const connectedId = edge.data.source === nodeId ? edge.data.target : edge.data.source;
      const connectedNode = dataToUse?.nodes?.find(n => n.data.id === connectedId);

      if (!connectedNode) return null;

      return {
        id: connectedNode.data.id,
        label: connectedNode.data.label,
        type: connectedNode.data.type,
        edgeType: edge.data.type
      };
    }).filter(Boolean) as Array<{
      id: string;
      label: string;
      type: NodeType;
      edgeType: EdgeType;
    }>;
  }

  $: connectedNodes = selectedNode ? getConnectedNodes(selectedNode.id) : [];

  async function handleApplyFilters(filters: GraphFilters) {
    currentFilters = filters;
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
    currentFilters = {
      lawStatuses: ['approved', 'rejected', 'withdrawn'],
      relationshipTypes: ['authored', 'belongs_to', 'member_of', 'lobby', 'voted_same', 'voted_on']
    };
    currentGraphData = graphData;
  }

  function handleSearch(query: string) {
    searchQuery.set(query);
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

  function closeNodeDetails() {
    showNodeDetails = false;
    selectedNode = null;
  }

  function handleEscape(e: KeyboardEvent) {
    if (e.key === 'Escape' && showNodeDetails) {
      closeNodeDetails();
    }
  }
</script>

<svelte:window on:keydown={handleEscape} />

<svelte:head>
  <title>SenadoGraph</title>
  <meta name="description" content="Chilean Senate Relationship Visualization" />
</svelte:head>

<!-- Data Disclaimer -->
<DataDisclaimer />

<!-- Hero Section -->
<div class="text-center mb-8 animate-fade-in-down">
  <h1 class="section-title">
    SenadoGraph
  </h1>
  <p class="subtitle max-w-2xl mx-auto">
    Explore the Chilean Senate's intricate network of relationships, voting patterns, and collaborations
  </p>
</div>

 <!-- Stats Cards -->
<StatsCards
   totalSenators={nodeCounts.senators}
   totalParties={nodeCounts.parties}
   totalLaws={nodeCounts.laws}
   totalCommittees={nodeCounts.committees}
   {partyBreakdown}
   {lawStatusBreakdown}
 />

<!-- Search Bar -->
<div class="mb-6 animate-fade-in-up" style="animation-delay: 400ms;">
  <SearchBar
    onSearch={handleSearch}
    results={searchResults}
    placeholder="Search senators, parties, laws..."
    on:select={handleSearchSelect}
  />
</div>

<!-- Controls Bar -->
<div class="flex justify-between items-center mb-4 animate-fade-in-up" style="animation-delay: 500ms;">
  <button
    on:click={() => showFilters = !showFilters}
    class="btn-gradient-secondary flex items-center space-x-2"
  >
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
    </svg>
    <span>Filters</span>
    {#if ($filterStore.parties && $filterStore.parties.length > 0) || ($filterStore.committees && $filterStore.committees.length > 0)}
      <span class="ml-2 px-2 py-0.5 bg-white/30 text-xs rounded-full backdrop-blur-sm">
        {($filterStore.parties?.length || 0) + ($filterStore.committees?.length || 0)} active
      </span>
    {/if}
  </button>

   <p class="text-sm text-gray-600 font-medium">
     {(currentGraphData || graphData)?.nodes?.length || 0} nodes • {(currentGraphData || graphData)?.edges?.length || 0} connections
   </p>
</div>

 <!-- Filter Panel Overlay -->
 {#if showFilters}
   <div class="fixed inset-0 z-50 animate-fade-in">
     <div
       class="absolute inset-0 bg-black/30 backdrop-blur-sm"
       on:click={() => showFilters = false}
     ></div>
      <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
        <FilterPanel
          {parties}
          {committees}
          currentFilters={currentFilters}
          onApplyFilters={handleApplyFilters}
          onClose={() => showFilters = false}
        />
      </div>
   </div>
 {/if}

 <!-- Graph Visualization -->
 <div class="glass-panel rounded-2xl overflow-hidden mb-8 animate-fade-in-up" style="animation-delay: 600ms;">
    <div class="relative h-[700px]">
      <CytoscapeGraph
        bind:this={graphComponent}
        graphData={currentGraphData || graphData}
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
<div class="glass-panel rounded-2xl overflow-hidden animate-fade-in-up" style="animation-delay: 700ms;">
  <div class="px-6 py-4 border-b border-white/20 bg-gradient-primary/10">
    <h2 class="text-lg font-semibold gradient-text">Featured Senators</h2>
  </div>

  <div class="divide-y divide-white/10">
    {#each senators.slice(0, 10) as senator, index}
      <a
        href="/senador/{senator.id}"
        class="block px-6 py-4 hover:bg-white/50 transition-all duration-300 hover:scale-[1.01] hover:shadow-lg"
        style="animation-delay: {700 + index * 50}ms;"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            {#if senator.photoUrl}
              <img
                src={senator.photoUrl}
                alt={senator.name}
                class="w-12 h-12 rounded-full object-cover shadow-md"
              />
            {:else}
              <div class="w-12 h-12 rounded-full bg-gradient-primary flex items-center justify-center text-white font-bold">
                {senator.name.charAt(0)}
              </div>
            {/if}
            <div>
              <h3 class="text-sm font-semibold text-gray-900">{senator.name}</h3>
              <p class="text-sm text-gray-600">{senator.party} • {senator.region}</p>
            </div>
          </div>
          <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </div>
      </a>
    {/each}
  </div>

  {#if senators.length > 10}
    <div class="px-6 py-4 border-t border-white/20 bg-gradient-primary/5">
      <p class="text-sm text-gray-600 text-center font-medium">
        {senators.length - 10} more senators
      </p>
    </div>
  {/if}
</div>

<!-- Graph Legend -->
<GraphLegend
  {nodeCounts}
  {edgeCounts}
/>

<!-- Node Details Panel -->
<NodeDetailsPanel
  bind:isOpen={showNodeDetails}
  nodeData={selectedNode}
  connectedNodes={connectedNodes}
  onClose={closeNodeDetails}
/>
