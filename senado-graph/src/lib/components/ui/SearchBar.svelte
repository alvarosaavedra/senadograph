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
      class="w-full px-4 py-2 pl-10 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
      aria-label="Search"
      aria-expanded={isOpen}
      aria-haspopup="listbox"
    />
    <div class="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
      <svg class="h-5 w-5 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
      </svg>
    </div>
    {#if query}
      <button
        on:click={() => { query = ''; onSearch(''); }}
        class="absolute inset-y-0 right-0 pr-3 flex items-center"
        aria-label="Clear search"
      >
        <svg class="h-5 w-5 text-gray-400 hover:text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
        </svg>
      </button>
    {/if}
  </div>

  {#if isOpen && results.length > 0}
    <ul
      class="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 max-h-60 overflow-auto"
      role="listbox"
    >
      {#each results as result, index}
        <li>
          <button
            class="w-full px-4 py-2 text-left hover:bg-gray-50 focus:bg-gray-50 focus:outline-none {index === selectedIndex ? 'bg-blue-50' : ''}"
            on:click={() => handleSelect(result)}
            role="option"
            aria-selected={index === selectedIndex}
          >
            <div class="flex items-center space-x-2">
              {#if result.type === 'senator'}
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                <span class="text-sm font-medium text-gray-900">{result.name}</span>
                <span class="text-xs text-gray-500">{result.party}</span>
              {:else if result.type === 'law'}
                <span class="w-2 h-2 rounded-full bg-green-500"></span>
                <span class="text-sm font-medium text-gray-900">{result.title}</span>
                <span class="text-xs text-gray-500">{result.boletin}</span>
              {:else if result.type === 'party'}
                <span class="w-2 h-2 rounded-full bg-purple-500"></span>
                <span class="text-sm font-medium text-gray-900">{result.name}</span>
                <span class="text-xs text-gray-500">{result.shortName}</span>
              {/if}
            </div>
          </button>
        </li>
      {/each}
    </ul>
  {:else if isOpen && query.length >= 2 && results.length === 0}
    <div class="absolute z-50 w-full mt-1 bg-white rounded-lg shadow-lg border border-gray-200 p-4">
      <p class="text-sm text-gray-500 text-center">No results found</p>
    </div>
  {/if}
</div>
