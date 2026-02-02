<script lang="ts">
  import type { Senator } from '$lib/types';

  export let senator: Senator;
  export let compact: boolean = false;

  $: displayName = senator.name;
  $: displayRegion = senator.regionEn || senator.region;
  $: initials = displayName.split(' ').map(n => n[0]).join('').slice(0, 2);
</script>

{#if compact}
  <div class="flex items-center gap-3 p-3 bg-white/70 backdrop-blur-sm rounded-xl border border-white/30 hover:border-primary-300 transition-all duration-300 hover:shadow-md hover:scale-[1.02]">
    {#if senator.photoUrl}
      <img
        src={senator.photoUrl}
        alt={displayName}
        class="w-10 h-10 rounded-full object-cover shadow-md"
        loading="lazy"
      />
    {:else}
      <div class="w-10 h-10 rounded-full bg-gradient-primary flex items-center justify-center text-white font-bold shadow-md">
        {initials}
      </div>
    {/if}
    <div class="flex-1 min-w-0">
      <p class="text-sm font-semibold text-gray-900 truncate">{displayName}</p>
      <p class="text-xs text-gray-600 truncate">{senator.party} · {displayRegion}</p>
    </div>
  </div>
{:else}
  <div class="glass-panel rounded-2xl overflow-hidden card-glow">
    <div class="flex p-6 gap-5">
      {#if senator.photoUrl}
        <div class="relative">
          <img
            src={senator.photoUrl}
            alt={displayName}
            class="w-24 h-24 rounded-xl object-cover flex-shrink-0 shadow-lg"
            loading="lazy"
          />
          {#if senator.active}
            <div class="absolute -bottom-1 -right-1 w-6 h-6 bg-gradient-success rounded-full border-2 border-white flex items-center justify-center">
              <svg class="w-3 h-3 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="3" d="M5 13l4 4L19 7" />
              </svg>
            </div>
          {/if}
        </div>
      {:else}
        <div class="w-24 h-24 rounded-xl bg-gradient-primary flex items-center justify-center flex-shrink-0 shadow-lg">
          <span class="text-white text-3xl font-bold">{initials}</span>
        </div>
      {/if}
      <div class="flex-1 min-w-0">
        <h3 class="text-xl font-bold text-gray-900 mb-2">{displayName}</h3>
        <div class="space-y-2">
          <p class="text-sm text-gray-700">
            <span class="font-semibold text-primary-600">Party:</span>
            {senator.party}
          </p>
          <p class="text-sm text-gray-700">
            <span class="font-semibold text-primary-600">Region:</span>
            {displayRegion}
          </p>
          {#if senator.email}
            <p class="text-sm text-gray-700">
              <span class="font-semibold text-primary-600">Email:</span>
              <a href="mailto:{senator.email}" class="text-primary-600 hover:text-primary-700 hover:underline transition-colors">
                {senator.email}
              </a>
            </p>
          {/if}
        </div>
        {#if !senator.active}
          <span class="inline-block mt-3 px-3 py-1 text-xs font-semibold bg-gray-200 text-gray-700 rounded-full">
            Inactive
          </span>
        {:else}
          <span class="inline-block mt-3 px-3 py-1 text-xs font-semibold bg-gradient-success/20 text-emerald-700 rounded-full">
            Active Senator
          </span>
        {/if}
      </div>
    </div>
  </div>
{/if}
