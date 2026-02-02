<script context="module" lang="ts">
  export type SearchResult =
    | { type: 'senator'; id: string; name: string; party?: string }
    | { type: 'law'; id: string; title: string; boletin?: string }
    | { type: 'party'; id: string; name: string; shortName?: string };
</script>

<script lang="ts">
  import { createEventDispatcher, onMount, onDestroy } from 'svelte';
  import { browser } from '$app/environment';

  export let onSearch: (query: string) => void;
  export let results: SearchResult[] = [];
  export let placeholder: string = '';

  let query: string = '';
  let isOpen: boolean = false;
  let selectedIndex: number = -1;
  let inputElement: HTMLInputElement;
  let containerElement: HTMLElement;
  let debounceTimer: ReturnType<typeof setTimeout>;

  const dispatch = createEventDispatcher<{
    select: SearchResult;
    close: void;
  }>();

  $: displayPlaceholder = placeholder || 'Search senators, laws...';

  function handleInput() {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      if (query.length >= 2) {
        onSearch(query);
        isOpen = true;
        selectedIndex = -1;
      } else {
        isOpen = false;
      }
    }, 300);
  }

  function handleSelect(result: SearchResult) {
    dispatch('select', result);
    query = result.type === 'senator' || result.type === 'party' ? result.name : result.title;
    isOpen = false;
  }

  function handleKeydown(event: KeyboardEvent) {
    if (!isOpen || results.length === 0) return;

    switch (event.key) {
      case 'ArrowDown':
        event.preventDefault();
        selectedIndex = (selectedIndex + 1) % results.length;
        break;
      case 'ArrowUp':
        event.preventDefault();
        selectedIndex = selectedIndex <= 0 ? results.length - 1 : selectedIndex - 1;
        break;
      case 'Enter':
        event.preventDefault();
        if (selectedIndex >= 0) {
          handleSelect(results[selectedIndex]);
        }
        break;
      case 'Escape':
        isOpen = false;
        dispatch('close');
        break;
    }
  }

  function handleClickOutside(event: MouseEvent) {
    if (containerElement && !containerElement.contains(event.target as Node)) {
      isOpen = false;
    }
  }

  onMount(() => {
    if (browser) {
      document.addEventListener('click', handleClickOutside);
    }
  });

  onDestroy(() => {
    if (browser) {
      document.removeEventListener('click', handleClickOutside);
    }
    clearTimeout(debounceTimer);
  });
</script>

<div class="relative w-full" bind:this={containerElement}>
  <div class="relative">
    <input
      bind:this={inputElement}
      type="text"
      bind:value={query}
      on:input={handleInput}
      on:keydown={handleKeydown}
      placeholder={displayPlaceholder}
      class="w-full px-5 py-3 pl-12 bg-white/50 border-2 border-white/30 rounded-xl focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent backdrop-blur-sm text-gray-800 placeholder-gray-500 transition-all duration-300"
      aria-label="Search"
      aria-expanded={isOpen}
      aria-haspopup="listbox"
    />
    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
      <svg class="h-6 w-6 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
    {#if query}
      <button
        on:click={() => { query = ''; onSearch(''); }}
        class="absolute inset-y-0 right-0 pr-4 flex items-center hover:text-primary-600 transition-colors"
        aria-label="Clear search"
      >
        <svg class="h-6 w-6 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    {/if}
  </div>

  {#if isOpen && results.length > 0}
    <ul
      class="absolute z-50 w-full mt-2 glass-panel rounded-xl shadow-glow border border-white/30 max-h-80 overflow-auto"
      role="listbox"
    >
      {#each results as result, index}
        <li>
          <button
            class="w-full px-5 py-3 text-left hover:bg-white/70 focus:bg-white/70 focus:outline-none transition-all duration-200 {index === selectedIndex ? 'bg-primary-50' : ''}"
            on:click={() => handleSelect(result)}
            role="option"
            aria-selected={index === selectedIndex}
          >
            <div class="flex items-center space-x-3">
              {#if result.type === 'senator'}
                <div class="w-3 h-3 rounded-full bg-gradient-primary"></div>
                <span class="text-sm font-semibold text-gray-900">{result.name}</span>
                <span class="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">{result.party}</span>
              {:else if result.type === 'law'}
                <div class="w-3 h-3 rounded-full bg-gradient-success"></div>
                <span class="text-sm font-semibold text-gray-900">{result.title}</span>
                <span class="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">{result.boletin}</span>
              {:else if result.type === 'party'}
                <div class="w-3 h-3 rounded-full bg-gradient-secondary"></div>
                <span class="text-sm font-semibold text-gray-900">{result.name}</span>
                <span class="text-xs text-gray-500 bg-gray-100 px-2 py-0.5 rounded-full">{result.shortName}</span>
              {/if}
            </div>
          </button>
        </li>
      {/each}
    </ul>
  {:else if isOpen && query.length >= 2 && results.length === 0}
    <div class="absolute z-50 w-full mt-2 glass-panel rounded-xl shadow-glow border border-white/30 p-6">
      <div class="text-center">
        <svg class="w-12 h-12 mx-auto text-gray-400 mb-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <p class="text-sm text-gray-600 font-medium">No results found</p>
        <p class="text-xs text-gray-500 mt-1">Try different keywords</p>
      </div>
    </div>
  {/if}
</div>
