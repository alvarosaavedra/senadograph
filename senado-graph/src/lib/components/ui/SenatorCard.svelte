<script lang="ts">
  import type { Senator } from '$lib/types';

  export let senator: Senator;
  export let compact: boolean = false;

  $: displayName = senator.name;
  $: displayRegion = senator.regionEn || senator.region;
</script>

{#if compact}
  <div class="flex items-center gap-3 p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 transition-colors">
    {#if senator.photoUrl}
      <img
        src={senator.photoUrl}
        alt={displayName}
        class="w-10 h-10 rounded-full object-cover"
        loading="lazy"
      />
    {:else}
      <div class="w-10 h-10 rounded-full bg-gray-200 flex items-center justify-center">
        <svg class="w-5 h-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
        </svg>
      </div>
    {/if}
    <div class="flex-1 min-w-0">
      <p class="text-sm font-medium text-gray-900 truncate">{displayName}</p>
      <p class="text-xs text-gray-500 truncate">{senator.party} · {displayRegion}</p>
    </div>
  </div>
{:else}
  <div class="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
    <div class="flex p-4 gap-4">
      {#if senator.photoUrl}
        <img
          src={senator.photoUrl}
          alt={displayName}
          class="w-20 h-20 rounded-lg object-cover flex-shrink-0"
          loading="lazy"
        />
      {:else}
        <div class="w-20 h-20 rounded-lg bg-gray-200 flex items-center justify-center flex-shrink-0">
          <svg class="w-10 h-10 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
      {/if}
      <div class="flex-1 min-w-0">
        <h3 class="text-lg font-semibold text-gray-900 mb-1">{displayName}</h3>
        <div class="space-y-1">
          <p class="text-sm text-gray-600">
            <span class="font-medium">Party:</span>
            {senator.party}
          </p>
          <p class="text-sm text-gray-600">
            <span class="font-medium">Region:</span>
            {displayRegion}
          </p>
          {#if senator.email}
            <p class="text-sm text-gray-600">
              <span class="font-medium">Email:</span>
              <a href="mailto:{senator.email}" class="text-blue-600 hover:underline">
                {senator.email}
              </a>
            </p>
          {/if}
        </div>
        {#if !senator.active}
          <span class="inline-block mt-2 px-2 py-1 text-xs font-medium bg-gray-100 text-gray-600 rounded">
            Inactive
          </span>
        {/if}
      </div>
    </div>
  </div>
{/if}
