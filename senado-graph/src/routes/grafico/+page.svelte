<script lang="ts">
  import { onMount } from 'svelte';
  import CytoscapeGraph from '$lib/components/graph/CytoscapeGraph.svelte';
  import ClusterStatsPanel from '$lib/components/ui/ClusterStatsPanel.svelte';
  import GraphControls from '$lib/components/graph/GraphControls.svelte';
  import GraphLegend from '$lib/components/graph/GraphLegend.svelte';
  import { detectVotingClusters } from '$lib/utils/clustering';
  import type { GraphData, ClusterInfo, GraphFilters } from '$lib/types';
  import { _ } from 'svelte-i18n';
  import { goto } from '$app/navigation';

  export let data;

  let { senators, parties, committees, initialGraphData, votingGraphData } = data;

  // UI State
  let sidebarOpen = true;
  let activeTab: 'clusters' | 'filters' | 'details' = 'clusters';

  // Clustering state
  let clusters: ClusterInfo[] = [];
  let showClusterColors = false;
  let selectedCluster: number | null = null;
  let clusteredGraphData: GraphData = initialGraphData;
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

  function toggleSidebar() {
    sidebarOpen = !sidebarOpen;
  }
</script>

<svelte:head>
  <title>{$_('app.title')} - Graph Visualization</title>
  <meta name="description" content="Explore Chilean Senate voting pattern clusters" />
</svelte:head>

<!-- Full-height container -->
<div class="h-full flex">
  <!-- Sidebar - collapsible -->
  {#if sidebarOpen}
    <div class="w-80 bg-white shadow-xl flex flex-col z-20 border-r border-gray-200 transition-all duration-300">
      <!-- Sidebar Header -->
      <div class="p-4 border-b border-gray-200 bg-gradient-to-r from-blue-50 to-indigo-50">
        <div class="flex items-center justify-between">
          <h2 class="text-lg font-bold text-gray-800">{$_('app.title')}</h2>
          <button
            on:click={toggleSidebar}
            class="p-2 hover:bg-gray-100 rounded-lg transition-colors"
            title="Hide sidebar"
          >
            <svg class="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 19l-7-7 7-7m8 14l-7-7 7-7" />
            </svg>
          </button>
        </div>
        <p class="text-sm text-gray-600 mt-1">Explore voting patterns and clusters</p>
      </div>

      <!-- Tabs -->
      <div class="flex border-b border-gray-200">
        <button
          class="flex-1 py-3 px-4 text-sm font-medium transition-colors {activeTab === 'clusters' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50' : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'}"
          on:click={() => activeTab = 'clusters'}
        >
          Clusters
          {#if clusters.length > 0}
            <span class="ml-2 px-2 py-0.5 bg-blue-100 text-blue-700 rounded-full text-xs">
              {clusters.length}
            </span>
          {/if}
        </button>
        <button
          class="flex-1 py-3 px-4 text-sm font-medium transition-colors {activeTab === 'details' ? 'text-blue-600 border-b-2 border-blue-600 bg-blue-50' : 'text-gray-600 hover:text-gray-800 hover:bg-gray-50'}"
          on:click={() => activeTab = 'details'}
        >
          Details
        </button>
      </div>

      <!-- Tab Content -->
      <div class="flex-1 overflow-y-auto p-4">
        {#if activeTab === 'clusters'}
          {#if clusters.length > 0}
            <ClusterStatsPanel
              {clusters}
              {selectedCluster}
              {showClusterColors}
              onSelectCluster={handleSelectCluster}
              onToggleClusterColors={handleToggleClusterColors}
            />
          {:else}
            <div class="text-center py-8">
              <div class="w-16 h-16 mx-auto mb-4 bg-gray-100 rounded-full flex items-center justify-center">
                <svg class="w-8 h-8 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                </svg>
              </div>
              <p class="text-gray-600 mb-2">No clusters detected</p>
              <p class="text-sm text-gray-500">Not enough voting data to identify patterns</p>
            </div>
          {/if}
        {:else if activeTab === 'details'}
          <div class="space-y-4">
            <div class="bg-blue-50 rounded-lg p-4">
              <h4 class="font-semibold text-blue-900 mb-2">Graph Overview</h4>
              <div class="space-y-2 text-sm">
                <div class="flex justify-between">
                  <span class="text-blue-700">Senators:</span>
                  <span class="font-medium">{clusteredGraphData.nodes.filter(n => n.data.type === 'senator').length}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-blue-700">Laws:</span>
                  <span class="font-medium">{clusteredGraphData.nodes.filter(n => n.data.type === 'law').length}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-blue-700">Relationships:</span>
                  <span class="font-medium">{clusteredGraphData.edges.length}</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-blue-700">Voting Agreements:</span>
                  <span class="font-medium">{clusteredGraphData.edges.filter(e => e.data.type === 'voted_same').length}</span>
                </div>
              </div>
            </div>

            <div class="bg-gray-50 rounded-lg p-4">
              <h4 class="font-semibold text-gray-900 mb-2">How to Use</h4>
              <ul class="text-sm text-gray-600 space-y-2">
                <li class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                  </svg>
                  <span>Click nodes to view senator or law details</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 20l4-16m2 16l4-16M6 9h14M4 15h14" />
                  </svg>
                  <span>Hover over edges to see relationship type</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                  </svg>
                  <span>Use mouse wheel to zoom in/out</span>
                </li>
                <li class="flex items-start gap-2">
                  <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                  <span>Toggle cluster colors to see voting blocs</span>
                </li>
              </ul>
            </div>
          </div>
        {/if}
      </div>
    </div>
  {/if}

  <!-- Main Graph Area -->
  <div class="flex-1 relative bg-gray-100">
    <!-- Toggle Sidebar Button (when closed) -->
    {#if !sidebarOpen}
      <button
        on:click={toggleSidebar}
        class="absolute top-4 left-4 z-30 bg-white shadow-lg rounded-lg p-3 hover:bg-gray-50 transition-colors border border-gray-200"
        title="Show sidebar"
      >
        <svg class="w-6 h-6 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </button>
    {/if}

    <!-- Floating Controls -->
    <div class="absolute top-4 right-4 z-30 flex flex-col gap-2">
      <div class="bg-white shadow-lg rounded-lg p-2 border border-gray-200">
        <GraphControls
          onZoomIn={() => cytoscapeRef?.zoomIn()}
          onZoomOut={() => cytoscapeRef?.zoomOut()}
          onFit={() => cytoscapeRef?.fit()}
          onResetLayout={() => cytoscapeRef?.resetLayout()}
        />
      </div>
    </div>

    <!-- Legend Overlay -->
    <div class="absolute bottom-4 right-4 z-30">
      <GraphLegend />
    </div>

    <!-- Graph Canvas -->
    <div class="absolute inset-0">
      <CytoscapeGraph
        bind:this={cytoscapeRef}
        graphData={clusteredGraphData}
        {showClusterColors}
        {selectedCluster}
        onNodeClick={handleNodeClick}
      />
    </div>
  </div>
</div>
