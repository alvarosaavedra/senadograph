<script lang="ts">
  import { _ } from '$lib/i18n';
  import type { GraphData } from '$lib/types';
  import CytoscapeGraph from '$lib/components/graph/CytoscapeGraph.svelte';
  import GraphControls from '$lib/components/graph/GraphControls.svelte';
  import { goto } from '$app/navigation';
  
  export let data;
  
  $: ({ senators, graphData, parties, committees } = data);
  
  let graphComponent: CytoscapeGraph;
  
  function handleNodeClick(nodeId: string, type: string) {
    if (type === 'senator') {
      goto(`/senador/${nodeId}`);
    } else if (type === 'law') {
      goto(`/ley/${nodeId}`);
    }
  }
</script>

<svelte:head>
  <title>SenadoGraph - {$_('app.subtitle')}</title>
  <meta name="description" content={$_('app.subtitle')} />
</svelte:head>

<!-- Hero Section -->
<div class="text-center mb-12">
  <h1 class="text-4xl font-bold text-gray-900 mb-4">
    {$_('app.title')}
  </h1>
  <p class="text-xl text-gray-600 max-w-2xl mx-auto">
    {$_('app.subtitle')}
  </p>
</div>

<!-- Data Disclaimer -->
<div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
  <div class="flex items-start">
    <div class="flex-shrink-0">
      <svg class="h-5 w-5 text-blue-400" viewBox="0 0 20 20" fill="currentColor">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
      </svg>
    </div>
    <div class="ml-3">
      <h3 class="text-sm font-medium text-blue-800">{$_('disclaimer.title')}</h3>
      <p class="mt-1 text-sm text-blue-700">{$_('disclaimer.text')}</p>
    </div>
  </div>
</div>

<!-- Graph Visualization -->
<div class="bg-white rounded-lg shadow-md overflow-hidden mb-8">
  <div class="px-6 py-4 border-b border-gray-200">
    <h2 class="text-lg font-semibold text-gray-900">{$_('nav.senators')}</h2>
    <p class="text-sm text-gray-500 mt-1">
      {graphData.nodes.length} {$_('nav.senators').toLowerCase()} {$_('common.loading') === 'Loading...' ? '' : ''}
    </p>
  </div>
  
  <div class="relative h-[600px]">
    <CytoscapeGraph 
      bind:this={graphComponent}
      {graphData} 
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
    <h2 class="text-lg font-semibold text-gray-900">{$_('nav.senators')}</h2>
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
        {senators.length - 10} {$_('common.more')}...
      </p>
    </div>
  {/if}
</div>
