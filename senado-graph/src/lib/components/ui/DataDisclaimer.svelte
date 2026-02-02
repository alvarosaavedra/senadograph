<script lang="ts">
  import { fade, fly } from 'svelte/transition';

  export let dismissible: boolean = true;

  let isVisible: boolean = true;
  let isDismissed: boolean = false;

  function dismiss() {
    isVisible = false;
    isDismissed = true;
  }

  export function show() {
    isVisible = true;
    isDismissed = false;
  }

  export function hide() {
    isVisible = false;
  }
</script>

{#if isVisible && !isDismissed}
  <div
    class="bg-blue-50 border border-blue-200 rounded-lg p-4 relative"
    transition:fade={{ duration: 200 }}
  >
    <div class="flex gap-3">
      <div class="flex-shrink-0">
        <svg
          class="w-5 h-5 text-blue-600 mt-0.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
      </div>
      <div class="flex-1">
        <h4 class="text-sm font-semibold text-blue-900 mb-1">
          Data Disclaimer
        </h4>
        <p class="text-sm text-blue-800 leading-relaxed">
          This data is collected from public sources and may not reflect the most current information. Please verify with official sources.
        </p>
      </div>
      {#if dismissible}
        <button
          on:click={dismiss}
          class="flex-shrink-0 -mr-1 -mt-1 p-1 text-blue-400 hover:text-blue-600 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 rounded"
          aria-label="Close"
        >
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>
      {/if}
    </div>
  </div>
{/if}
