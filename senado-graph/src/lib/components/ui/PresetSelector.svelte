<script lang="ts">
  import { presets } from '$lib/config/presets';
  import { _ } from 'svelte-i18n';

  export let onApplyPreset: (presetId: string) => void;
  export let onReset: () => void;

  let selectedPresetId = '';

  function handlePresetClick(presetId: string) {
    selectedPresetId = selectedPresetId === presetId ? '' : presetId;
  }

  function handleApply() {
    if (selectedPresetId) {
      onApplyPreset(selectedPresetId);
      selectedPresetId = '';
    }
  }

  $: selectedPreset = selectedPresetId ? presets.find(p => p.id === selectedPresetId) : null;

  const presetIcons = {
    polarization: '⚡',
    'cross-party': '🤝',
    'power-brokers': '🏛️',
    'industry-influence': '💼',
    'legislative-collaboration': '📜'
  };
</script>

<div class="space-y-3">
  <div class="flex items-center justify-between mb-3">
    <h3 class="text-base font-bold gradient-text">
      {$_('filters.presets.title')}
    </h3>
    <button
      type="button"
      on:click={onReset}
      class="text-xs text-primary-600 hover:text-primary-800 font-medium flex items-center gap-1 px-2 py-1 rounded hover:bg-primary-50 transition-colors"
    >
      <svg class="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
      </svg>
      {$_('filters.presets.reset')}
    </button>
  </div>

  <div class="grid grid-cols-1 gap-3">
    {#each presets as preset}
      <button
        type="button"
        on:click={() => handlePresetClick(preset.id)}
        class:active={selectedPresetId === preset.id}
        class="relative p-3 rounded-xl border-2 transition-all duration-300 hover:shadow-lg text-left {selectedPresetId !== preset.id ? 'border-transparent bg-white text-gray-900 hover:bg-white/90 hover:scale-[1.02]' : 'border-primary-500 bg-gradient-primary text-white'}"
      >
        <div class="flex items-start gap-3">
          <span class="text-2xl flex-shrink-0">
            {presetIcons[preset.id as keyof typeof presetIcons] || '📊'}
          </span>
          <div class="flex-1 min-w-0">
            <p class="font-semibold text-sm">
              {$_(`filters.${preset.id}.name`)}
            </p>
            <p class="text-xs mt-1 opacity-90 line-clamp-2">
              {$_(`filters.${preset.id}.description`)}
            </p>
          </div>
        </div>
      </button>
    {/each}
  </div>

  {#if selectedPresetId}
    <button
      type="button"
      on:click={handleApply}
      class="w-full px-4 py-3 bg-gradient-primary text-white text-sm font-semibold rounded-xl hover:shadow-glow transition-all duration-300 hover:scale-[1.02] active:scale-95 flex items-center justify-center gap-2"
    >
      <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
      </svg>
      {$_('filters.apply')}
    </button>
  {/if}
</div>

<style>
  .line-clamp-2 {
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
</style>
