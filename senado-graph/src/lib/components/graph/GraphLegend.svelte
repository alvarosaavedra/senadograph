<script lang="ts">
  import type { Party } from '$lib/types';
  
  export let isOpen: boolean = true;
  export let nodeCounts: {
    senators?: number;
  } = {};
  export let edgeCounts: {
    voted_same?: number;
  } = {};
  export let parties: Party[] = [];

  let panelElement: HTMLDivElement;

</script>

{#if isOpen}
  <div
    class="z-40 glass-panel rounded-xl shadow-glow p-4 max-w-sm animate-scale-in"
    style="position: fixed; right: 20px; top: 20px;"
    bind:this={panelElement}
  >
    <div
      class="flex items-center justify-between mb-4"
    >
      <h3 class="text-lg font-bold gradient-text">Graph Legend</h3>
      <button
        on:click={() => (isOpen = false)}
        class="p-1 rounded-lg hover:bg-gray-100 transition-colors"
        aria-label="Close legend"
      >
        <svg class="w-5 h-5 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    </div>

    <div class="space-y-4">
      <div>
        <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
          </svg>
          Senators
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-4 h-4 rounded-full bg-blue-500"></div>
              <span>Senators</span>
            </div>
            {#if nodeCounts.senators}
              <span class="text-xs bg-primary-100 text-primary-700 px-2 py-0.5 rounded-full font-medium">
                {nodeCounts.senators}
              </span>
            {/if}
          </div>
        </div>
        <p class="text-xs text-gray-500 mt-2">
          Each node represents a senator
        </p>
      </div>

      {#if parties.length > 0}
        <div class="border-t border-white/20 pt-4">
          <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
            <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
            </svg>
            Party Colors
          </h4>
          <div class="space-y-1 text-sm">
            {#each parties as party}
              <div class="flex items-center gap-2">
                <div class="w-4 h-4 rounded-full" style="background-color: {party.color}"></div>
                <span class="text-gray-700">{party.shortName}</span>
              </div>
            {/each}
          </div>
          <p class="text-xs text-gray-500 mt-2">
            Toggle cluster colors to see voting blocs
          </p>
        </div>
      {/if}

      <div class="border-t border-white/20 pt-4">
        <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
          Voting Agreements
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-0.5 bg-green-500"></div>
              <span>Similar voting pattern</span>
            </div>
            {#if edgeCounts.voted_same}
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {edgeCounts.voted_same}
              </span>
            {/if}
          </div>
        </div>
        <p class="text-xs text-gray-500 mt-2">
          Lines connect senators who vote similarly on bills
        </p>
      </div>
    </div>
  </div>
{/if}

{#if !isOpen}
  <button
    on:click={() => (isOpen = true)}
    class="fixed z-40 bottom-4 right-4 glass-panel px-4 py-2 rounded-xl font-medium text-sm gradient-text hover:shadow-glow transition-all duration-300"
    aria-label="Open legend"
  >
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
    </svg>
    <span class="ml-2">Legend</span>
  </button>
{/if}


