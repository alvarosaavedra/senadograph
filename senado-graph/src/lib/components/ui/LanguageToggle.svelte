<script lang="ts">
  import { createEventDispatcher } from 'svelte';

  export let currentLang: 'es' | 'en' = 'es';
  export let onChange: ((lang: 'es' | 'en') => void) | undefined = undefined;

  const dispatch = createEventDispatcher<{ change: 'es' | 'en' }>();

  function setLanguage(lang: 'es' | 'en') {
    if (onChange) {
      onChange(lang);
    }
    dispatch('change', lang);
  }
</script>

<div class="inline-flex rounded-lg border border-gray-200 bg-white p-1 shadow-sm">
  <button
    on:click={() => setLanguage('es')}
    class="px-3 py-1.5 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 {currentLang === 'es'
      ? 'bg-blue-600 text-white'
      : 'text-gray-700 hover:bg-gray-100'}"
    aria-pressed={currentLang === 'es'}
  >
    ES
  </button>
  <button
    on:click={() => setLanguage('en')}
    class="px-3 py-1.5 text-sm font-medium rounded-md transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-1 {currentLang === 'en'
      ? 'bg-blue-600 text-white'
      : 'text-gray-700 hover:bg-gray-100'}"
    aria-pressed={currentLang === 'en'}
  >
    EN
  </button>
</div>
