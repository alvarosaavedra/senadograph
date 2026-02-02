<script lang="ts">
  export let onZoomIn: () => void;
  export let onZoomOut: () => void;
  export let onFit: () => void;
  export let onResetLayout: () => void;
</script>

<div class="absolute bottom-4 right-4 flex flex-col gap-2 bg-white rounded-lg shadow-md p-2 z-10">
  <button
    on:click={onZoomIn}
    class="p-2 hover:bg-gray-100 rounded-md transition-colors"
    title="Zoom In"
  >
    <svg class="w-5 h-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
    </svg>
  </button>
  
  <button
    on:click={onZoomOut}
    class="p-2 hover:bg-gray-100 rounded-md transition-colors"
    title="Zoom Out"
  >
    <svg class="w-5 h-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20 12H4" />
    </svg>
  </button>
  
  <div class="w-full h-px bg-gray-200 my-1"></div>
  
  <button
    on:click={onFit}
    class="p-2 hover:bg-gray-100 rounded-md transition-colors"
    title="Fit to Screen"
  >
    <svg class="w-5 h-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
    </svg>
  </button>
  
  <button
    on:click={onResetLayout}
    class="p-2 hover:bg-gray-100 rounded-md transition-colors"
    title="Reset Layout"
  >
    <svg class="w-5 h-5 text-gray-700" fill="none" viewBox="0 0 24 24" stroke="currentColor">
      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
    </svg>
  </button>
</div>
