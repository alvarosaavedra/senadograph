<script lang="ts">
  import type { ClusterInfo } from '$lib/types';
  import { _ } from 'svelte-i18n';

  export let clusters: ClusterInfo[] = [];
  export let selectedCluster: number | null = null;
  export let onSelectCluster: (clusterId: number | null) => void = () => {};
  export let showClusterColors: boolean = false;
  export let onToggleClusterColors: () => void = () => {};

  function getDominantParty(cluster: ClusterInfo): { party: string; count: number } | null {
    const entries: [string, number][] = Object.entries(cluster.partyBreakdown);
    if (entries.length === 0) return null;
    
    const [party, count] = entries.sort((a, b) => b[1] - a[1])[0];
    return { party, count: count as number };
  }

  function getPartyPercentage(cluster: ClusterInfo, party: string): number {
    if (cluster.size === 0) return 0;
    return Math.round(((cluster.partyBreakdown[party] || 0) / cluster.size) * 100);
  }
</script>

<div class="cluster-stats-panel bg-white rounded-lg shadow-md p-4 max-w-sm">
  <div class="flex items-center justify-between mb-4">
    <h3 class="text-lg font-semibold text-gray-900">
      {$_('clustering.title')}
    </h3>
    <button
      class="text-sm px-3 py-1 rounded-full transition-colors {showClusterColors ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-700 hover:bg-gray-300'}"
      on:click={onToggleClusterColors}
    >
      {showClusterColors ? $_('clustering.hideColors') : $_('clustering.showColors')}
    </button>
  </div>

  {#if clusters.length === 0}
    <p class="text-gray-500 text-sm italic">
      {$_('clustering.noClusters')}
    </p>
  {:else}
    <div class="space-y-3 max-h-96 overflow-y-auto">
      {#each clusters as cluster}
        {@const dominantParty = getDominantParty(cluster)}
        <button
          class="w-full text-left p-3 rounded-lg border-2 transition-all hover:shadow-md {selectedCluster === cluster.id ? 'border-blue-500 bg-blue-50' : 'border-gray-200 hover:border-gray-300'}"
          on:click={() => onSelectCluster(selectedCluster === cluster.id ? null : cluster.id)}
        >
          <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-2">
              <div
                class="w-4 h-4 rounded-full"
                style="background-color: {cluster.color}"
              />
              <span class="font-medium text-gray-900">
                {cluster.name}
              </span>
            </div>
            <span class="text-sm text-gray-600">
              {cluster.size} {$_('clustering.senators')}
            </span>
          </div>

          <div class="space-y-1">
            {#if dominantParty}
              <div class="flex items-center justify-between text-sm">
                <span class="text-gray-600">{$_('clustering.dominantParty')}:</span>
                <span class="font-medium" style="color: {cluster.color}">
                  {dominantParty.party} ({getPartyPercentage(cluster, dominantParty.party)}%)
                </span>
              </div>
            {/if}

            <div class="flex items-center justify-between text-sm">
              <span class="text-gray-600">{$_('clustering.cohesion')}:</span>
              <div class="flex items-center gap-2">
                <div class="w-16 h-2 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    class="h-full rounded-full"
                    style="width: {cluster.cohesion * 100}%; background-color: {cluster.color}"
                  />
                </div>
                <span class="text-xs text-gray-500">
                  {Math.round(cluster.cohesion * 100)}%
                </span>
              </div>
            </div>

            {#if Object.keys(cluster.partyBreakdown).length > 1}
              <div class="mt-2 pt-2 border-t border-gray-100">
                <p class="text-xs text-gray-500 mb-1">{$_('clustering.partyDistribution')}:</p>
                <div class="flex flex-wrap gap-1">
                  {#each Object.entries(cluster.partyBreakdown) as [party, count]}
                    <span class="text-xs px-2 py-0.5 bg-gray-100 rounded-full text-gray-700">
                      {party}: {count}
                    </span>
                  {/each}
                </div>
              </div>
            {/if}
          </div>
        </button>
      {/each}
    </div>

    <div class="mt-4 pt-4 border-t border-gray-200">
      <p class="text-xs text-gray-500">
        {$_('clustering.description')}
      </p>
    </div>
  {/if}
</div>

<style>
  .cluster-stats-panel {
    max-height: calc(100vh - 200px);
  }
</style>
