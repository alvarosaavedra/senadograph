<script lang="ts">
  export let isOpen: boolean = true;
  export let nodeCounts: {
    senators?: number;
    laws?: number;
    parties?: number;
    committees?: number;
    lobbyists?: number;
  } = {};
  export let edgeCounts: {
    authored?: number;
    member_of?: number;
    belongs_to?: number;
    lobby?: number;
    voted_same?: number;
    voted_on?: number;
  } = {};

  let isDragging: boolean = false;
  let dragOffset: { x: number; y: number } = { x: 0, y: 0 };
  let position: { x: number; y: number } = { x: 20, y: 20 };
  let panelElement: HTMLDivElement;
  let headerElement: HTMLDivElement;

  function startDrag(e: MouseEvent | TouchEvent) {
    if (!(e.target instanceof Element)) return;
    if (!headerElement.contains(e.target)) return;

    isDragging = true;

    const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
    const clientY = 'touches' in e ? e.touches[0].clientY : e.clientY;

    dragOffset = {
      x: clientX - position.x,
      y: clientY - position.y
    };
  }

  function drag(e: MouseEvent | TouchEvent) {
    if (!isDragging) return;

    e.preventDefault();

    const clientX = 'touches' in e ? e.touches[0].clientX : e.clientX;
    const clientY = 'touches' in e ? e.touches[0].clientY : e.clientY;

    position = {
      x: clientX - dragOffset.x,
      y: clientY - dragOffset.y
    };
  }

  function stopDrag() {
    isDragging = false;
  }
</script>

{#if isOpen}
  <div
    class="fixed z-40 glass-panel rounded-xl shadow-glow p-4 max-w-sm animate-scale-in"
    style="left: {position.x}px; top: {position.y}px;"
    bind:this={panelElement}
  >
    <div
      bind:this={headerElement}
      class="flex items-center justify-between mb-4 cursor-move select-none"
      on:mousedown={startDrag}
      on:touchstart={startDrag}
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
          Nodes
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
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-4 h-3 rounded bg-green-500"></div>
              <span>Laws</span>
            </div>
            {#if nodeCounts.laws}
              <span class="text-xs bg-success-100 text-success-700 px-2 py-0.5 rounded-full font-medium">
                {nodeCounts.laws}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-4 h-4 bg-purple-500" style="clip-path: polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%);"></div>
              <span>Parties</span>
            </div>
            {#if nodeCounts.parties}
              <span class="text-xs bg-secondary-100 text-secondary-700 px-2 py-0.5 rounded-full font-medium">
                {nodeCounts.parties}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-4 h-4 bg-gradient-primary"></div>
              <span>Committees</span>
            </div>
            {#if nodeCounts.committees}
              <span class="text-xs bg-purple-100 text-purple-700 px-2 py-0.5 rounded-full font-medium">
                {nodeCounts.committees}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-3 h-3 rounded-full bg-orange-500"></div>
              <span>Lobbyists</span>
            </div>
            {#if nodeCounts.lobbyists}
              <span class="text-xs bg-accent-100 text-accent-700 px-2 py-0.5 rounded-full font-medium">
                {nodeCounts.lobbyists}
              </span>
            {/if}
          </div>
        </div>
      </div>

      <div class="border-t border-white/20 pt-4">
        <h4 class="text-sm font-semibold text-gray-700 mb-2 flex items-center gap-2">
          <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
          </svg>
          Edges
        </h4>
        <div class="space-y-2 text-sm">
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-0.5 bg-blue-500"></div>
              <span>Authored</span>
            </div>
            {#if edgeCounts.authored}
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {edgeCounts.authored}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-0.5 bg-purple-500" style="background: repeating-linear-gradient(90deg, #8b5cf6, #8b5cf6 4px, transparent 4px, transparent 6px);"></div>
              <span>Member of</span>
            </div>
            {#if edgeCounts.member_of}
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {edgeCounts.member_of}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-0.5 bg-gray-400"></div>
              <span>Belongs to</span>
            </div>
            {#if edgeCounts.belongs_to}
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {edgeCounts.belongs_to}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-0.5 bg-orange-500" style="background: repeating-linear-gradient(90deg, #f97316, #f97316 2px, transparent 2px, transparent 4px);"></div>
              <span>Lobby</span>
            </div>
            {#if edgeCounts.lobby}
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {edgeCounts.lobby}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-0.5 bg-green-500"></div>
              <span>Voting agreement</span>
            </div>
            {#if edgeCounts.voted_same}
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {edgeCounts.voted_same}
              </span>
            {/if}
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <div class="w-8 h-0.5 bg-red-500"></div>
              <span>Voted on law</span>
            </div>
            {#if edgeCounts.voted_on}
              <span class="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded-full">
                {edgeCounts.voted_on}
              </span>
            {/if}
          </div>
        </div>
      </div>
    </div>
  </div>
{/if}

{#if !isOpen}
  <button
    on:click={() => (isOpen = true)}
    class="fixed z-40 top-4 right-4 glass-panel px-4 py-2 rounded-xl font-medium text-sm gradient-text hover:shadow-glow transition-all duration-300"
    aria-label="Open legend"
  >
    <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
    </svg>
    <span class="ml-2">Legend</span>
  </button>
{/if}

<svelte:window on:mousemove={drag} on:mouseup={stopDrag} on:touchmove={drag} on:touchend={stopDrag} />
