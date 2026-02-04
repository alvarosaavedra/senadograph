<script lang="ts">
  import SearchBar from '$lib/components/ui/SearchBar.svelte';
  import DataDisclaimer from '$lib/components/ui/DataDisclaimer.svelte';
  import StatsCards from '$lib/components/dashboard/StatsCards.svelte';
  import { searchQuery } from '$lib/stores/filters';
  import { goto } from '$app/navigation';
  import type { SearchResult } from '$lib/components/ui/SearchBar.svelte';

  export let data;

  let searchResults: SearchResult[] = [];

  $: ({ senators, parties, stats } = data);

  function handleSearch(query: string) {
    searchQuery.set(query);
    const senatorResults: SearchResult[] = senators.map((s: { id: string; name: string; party: string }) => ({
      type: 'senator' as const,
      id: s.id,
      name: s.name,
      party: s.party
    }));
    const partyResults: SearchResult[] = parties.map((p: { id: string; name: string; shortName: string }) => ({
      type: 'party' as const,
      id: p.id,
      name: p.name,
      shortName: p.shortName
    }));

    searchResults = [...senatorResults, ...partyResults].filter(item => {
      const itemName = item.type === 'law' ? item.title : item.name;
      return itemName.toLowerCase().includes(query.toLowerCase());
    }).slice(0, 5);
  }

  function handleSearchSelect(event: CustomEvent) {
    const item = event.detail;
    if (item.type === 'senator') {
      goto(`/senador/${item.id}`);
    }
  }
</script>

<svelte:head>
  <title>SenadoGraph</title>
  <meta name="description" content="Chilean Senate Relationship Visualization" />
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
<!-- Data Disclaimer -->
<DataDisclaimer />

<!-- Hero Section -->
<div class="text-center mb-8 animate-fade-in-down">
  <h1 class="section-title">
    SenadoGraph
  </h1>
  <p class="subtitle max-w-2xl mx-auto">
    Explore the Chilean Senate's intricate network of relationships, voting patterns, and collaborations
  </p>
</div>

<!-- Stats Cards -->
<StatsCards
   totalSenators={stats?.senatorCount || 0}
   totalParties={stats?.partyCount || 0}
   totalLaws={stats?.lawCount || 0}
   totalCommittees={stats?.committeeCount || 0}
   partyBreakdown={stats?.partyBreakdown || []}
   lawStatusBreakdown={stats?.lawStatusBreakdown || []}
/>

<!-- Search Bar -->
<div class="mb-6 animate-fade-in-up" style="animation-delay: 400ms;">
  <SearchBar
    onSearch={handleSearch}
    results={searchResults}
    placeholder="Search senators, parties, laws..."
    on:select={handleSearchSelect}
  />
</div>

<!-- Senator List -->
<div class="glass-panel rounded-2xl overflow-hidden animate-fade-in-up" style="animation-delay: 500ms;">
  <div class="px-6 py-4 border-b border-white/20 bg-gradient-primary/10">
    <h2 class="text-lg font-semibold gradient-text">Featured Senators</h2>
  </div>

  <div class="divide-y divide-white/10">
    {#each senators.slice(0, 10) as senator, index}
      <a
        href="/senador/{senator.id}"
        class="block px-6 py-4 hover:bg-white/50 transition-all duration-300 hover:scale-[1.01] hover:shadow-lg"
        style="animation-delay: {500 + index * 50}ms;"
      >
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-4">
            {#if senator.photoUrl}
              <img
                src={senator.photoUrl}
                alt={senator.name}
                class="w-12 h-12 rounded-full object-cover shadow-md"
              />
            {:else}
              <div class="w-12 h-12 rounded-full bg-gradient-primary flex items-center justify-center text-white font-bold">
                {senator.name.charAt(0)}
              </div>
            {/if}
            <div>
              <h3 class="text-sm font-semibold text-gray-900">{senator.name}</h3>
              <p class="text-sm text-gray-600">{senator.party} • {senator.region}</p>
            </div>
          </div>
          <svg class="h-5 w-5 text-gray-400" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </div>
      </a>
    {/each}
  </div>

  {#if senators.length > 10}
    <div class="px-6 py-4 border-t border-white/20 bg-gradient-primary/5">
      <p class="text-sm text-gray-600 text-center font-medium">
        {senators.length - 10} more senators
      </p>
    </div>
  {/if}
</div>
</div>
