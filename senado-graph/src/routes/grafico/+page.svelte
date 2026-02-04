<script lang="ts">
  import { onMount } from 'svelte';
  import CytoscapeGraph from '$lib/components/graph/CytoscapeGraph.svelte';
  import ClusterStatsPanel from '$lib/components/ui/ClusterStatsPanel.svelte';
  import FilterPanel from '$lib/components/ui/FilterPanel.svelte';
  import GraphControls from '$lib/components/graph/GraphControls.svelte';
  import GraphLegend from '$lib/components/graph/GraphLegend.svelte';
  import { detectVotingClusters } from '$lib/utils/clustering';
  import type { GraphData, ClusterInfo, GraphFilters } from '$lib/types';
  import { _ } from 'svelte-i18n';
  import { goto } from '$app/navigation';

  export let data;

  let { senators, parties, committees, initialGraphData, votingGraphData } = data;

  // Clustering state
  let clusters: ClusterInfo[] = [];
  let showClusterColors = false;
  let selectedCluster: number | null = null;
  let clusteredGraphData: GraphData = initialGraphData;

  // Filter panel state
  let showFilters = false;
  let currentFilters: GraphFilters = {};

  // Cytoscape ref
  let cytoscapeRef: CytoscapeGraph;

  // Initialize clustering on mount
  onMount(() => {
    if (votingGraphData && votingGraphData.edges.length > 0) {
      const result = detectVotingClusters(votingGraphData);
      clusters = result.clusters;
      // Merge cluster data into initial graph data
      clusteredGraphData = {
        nodes: initialGraphData.nodes.map(node => {
          const clusteredNode = result.nodes.find(n => n.data.id === node.data.id);
          if (clusteredNode && clusteredNode.data.clusterId !== undefined) {
            return {
              ...node,
              data: {
                ...node.data,
                clusterId: clusteredNode.data.clusterId,
                clusterColor: clusteredNode.data.clusterColor,
              }
            };
          }
          return node;
        }),
        edges: initialGraphData.edges,
      };
    }
  });

  function handleNodeClick(nodeId: string, type: string) {
    if (type === 'senator') {
      goto(`/senador/${nodeId}`);
    } else if (type === 'law') {
      goto(`/ley/${nodeId}`);
    }
  }

  function handleToggleClusterColors() {
    showClusterColors = !showClusterColors;
  }

  function handleSelectCluster(clusterId: number | null) {
    selectedCluster = clusterId;
  }

  function handleToggleFilters() {
    showFilters = !showFilters;
  }

  function handleApplyFilters(filters: GraphFilters) {
    currentFilters = filters;
    // In a real implementation, this would refetch data with filters
    // and re-run clustering
    showFilters = false;
  }
</script>

<svelte:head>
  <title>{$_('app.title')} - Graph Visualization</title>
  <meta name="description" content="Explore Chilean Senate voting pattern clusters" />
</svelte:head>

<div class="h-[calc(100vh-200px)] min-h-[600px] flex gap-4">
  <!-- Left sidebar: Cluster stats -->
  {#if clusters.length > 0}
    <div class="w-80 flex-shrink-0">
      <ClusterStatsPanel
        {clusters}
        {selectedCluster}
        {showClusterColors}
        onSelectCluster={handleSelectCluster}
        onToggleClusterColors={handleToggleClusterColors}
      />
    </div>
  {/if}

  <!-- Main graph area -->
  <div class="flex-1 flex flex-col gap-4">
    <!-- Controls bar -->
    <div class="flex items-center justify-between bg-white rounded-lg shadow-md p-3">
      <div class="flex items-center gap-4">
        <button
          class="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-600 transition-colors text-sm font-medium"
          on:click={handleToggleFilters}
        >
          {showFilters ? 'Hide Filters' : 'Show Filters'}
        </button>
        
        {#if clusters.length > 0}
          <div class="text-sm text-gray-600">
            {clusters.length} clusters detected
          </div>
        {/if}
      </div>

      <GraphControls
        onZoomIn={() => cytoscapeRef?.zoomIn()}
        onZoomOut={() => cytoscapeRef?.zoomOut()}
        onFit={() => cytoscapeRef?.fit()}
        onReset={() => cytoscapeRef?.resetLayout()}
      />
    </div>

    <!-- Filter panel (conditional) -->
    {#if showFilters}
      <div class="bg-white rounded-lg shadow-md p-4">
        <FilterPanel
          {parties}
          {committees}
          {currentFilters}
          onApplyFilters={handleApplyFilters}
          onClose={() => showFilters = false}
        />
      </div>
    {/if}

    <!-- Graph container -->
    <div class="flex-1 bg-white rounded-lg shadow-md overflow-hidden relative">
      <CytoscapeGraph
        bind:this={cytoscapeRef}
        graphData={clusteredGraphData}
        {showClusterColors}
        {selectedCluster}
        onNodeClick={handleNodeClick}
      />
      
      <!-- Legend overlay -->
      <div class="absolute bottom-4 right-4">
        <GraphLegend />
      </div>
    </div>
  </div>
</div>

<style>
  :global(.cluster-stats-panel) {
    max-height: 100%;
    overflow-y: auto;
  }
</style>
