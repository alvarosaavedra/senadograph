<script lang="ts">
  import { presets } from '$lib/config/presets';
  import { _ } from 'svelte-i18n';

  export let onApplyPreset: (presetId: string) => void;
  export let onReset: () => void;

  let selectedPresetId = '';
  let showDescription = false;

  function handlePresetChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    const presetId = target.value;
    selectedPresetId = presetId;

    if (presetId) {
      showDescription = true;
    } else {
      showDescription = false;
    }
  }

  function handleApply() {
    if (selectedPresetId) {
      onApplyPreset(selectedPresetId);
    }
  }

  $: selectedPreset = selectedPresetId ? presets.find(p => p.id === selectedPresetId) : null;
</script>

<div class="space-y-3">
  <div class="flex items-center justify-between mb-2">
    <h3 class="text-sm font-semibold text-gray-900">
      {$_('filters.presets.title')}
    </h3>
    <button
      type="button"
      on:click={onReset}
      class="text-xs text-primary-600 hover:text-primary-800 font-medium underline"
    >
      {$_('filters.presets.reset')}
    </button>
  </div>

  <div class="space-y-2">
    <select
      bind:value={selectedPresetId}
      on:change={handlePresetChange}
      class="w-full px-3 py-2 bg-white/80 border border-gray-300 rounded-lg text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent"
    >
      <option value="">{$_('filters.presets.select')}</option>
      {#each presets as preset}
        <option value={preset.id}>
          {$_(`filters.${preset.id}.name`)}
        </option>
      {/each}
    </select>

    {#if selectedPreset && showDescription}
      <div class="p-3 bg-primary-50 border border-primary-200 rounded-lg">
        <p class="text-sm text-gray-700">
          {$_(`filters.${selectedPreset.id}.description`)}
        </p>
      </div>
    {/if}

    {#if selectedPreset}
      <button
        type="button"
        on:click={handleApply}
        class="w-full px-4 py-2 bg-gradient-primary text-white text-sm font-medium rounded-lg hover:shadow-md transition-all duration-300"
      >
        {$_('filters.apply')}
      </button>
    {/if}
  </div>
</div>
