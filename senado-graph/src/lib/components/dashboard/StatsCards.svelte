<script lang="ts">
  import { onMount } from 'svelte';

  export let totalSenators: number = 0;
  export let totalParties: number = 0;
  export let totalLaws: number = 0;
  export let totalCommittees: number = 0;
  export let partyBreakdown: { name: string; count: number; color: string }[] = [];
  export let lawStatusBreakdown: { status: string; count: number }[] = [];

  let animatedTotalSenators = 0;
  let animatedTotalParties = 0;
  let animatedTotalLaws = 0;
  let animatedTotalCommittees = 0;

  function animateValue(start: number, end: number, duration: number): number {
    let startTimestamp: number | null = null;
    const step = (timestamp: number) => {
      if (!startTimestamp) startTimestamp = timestamp;
      const progress = Math.min((timestamp - startTimestamp) / duration, 1);
      return Math.floor(progress * (end - start) + start);
    };
    return step(performance.now());
  }

  onMount(() => {
    const duration = 1500;
    const startTime = performance.now();

    const animate = () => {
      const elapsed = performance.now() - startTime;
      const progress = Math.min(elapsed / duration, 1);
      const easeProgress = 1 - Math.pow(1 - progress, 3);

      animatedTotalSenators = Math.floor(easeProgress * totalSenators);
      animatedTotalParties = Math.floor(easeProgress * totalParties);
      animatedTotalLaws = Math.floor(easeProgress * totalLaws);
      animatedTotalCommittees = Math.floor(easeProgress * totalCommittees);

      if (progress < 1) {
        requestAnimationFrame(animate);
      }
    };

    requestAnimationFrame(animate);
  });
</script>

<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
  <!-- Senators Card -->
  <div class="stat-card animate-fade-in-up" style="animation-delay: 0ms;">
    <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-primary opacity-10 rounded-full -translate-y-16 translate-x-16"></div>
    <div class="relative z-10">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-gray-600 uppercase tracking-wide">Senators</h3>
        <svg class="w-6 h-6 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
        </svg>
      </div>
      <p class="text-4xl font-bold gradient-text mb-2">{animatedTotalSenators}</p>
      <div class="space-y-1">
        {#each partyBreakdown.slice(0, 3) as party}
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600">{party.name}</span>
            <span class="font-medium" style="color: {party.color}">{party.count}</span>
          </div>
        {/each}
        {#if partyBreakdown.length > 3}
          <p class="text-xs text-gray-500">+{partyBreakdown.length - 3} more parties</p>
        {/if}
      </div>
    </div>
  </div>

  <!-- Parties Card -->
  <div class="stat-card animate-fade-in-up" style="animation-delay: 100ms;">
    <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-secondary opacity-10 rounded-full -translate-y-16 translate-x-16"></div>
    <div class="relative z-10">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-gray-600 uppercase tracking-wide">Political Parties</h3>
        <svg class="w-6 h-6 text-cyan-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
        </svg>
      </div>
      <p class="text-4xl font-bold gradient-text-secondary mb-2">{animatedTotalParties}</p>
      <p class="text-sm text-gray-600">Across the political spectrum</p>
      <div class="mt-3 flex flex-wrap gap-1">
        {#each partyBreakdown.slice(0, 4) as party}
          <div class="w-4 h-4 rounded-full" style="background-color: {party.color};"></div>
        {/each}
      </div>
    </div>
  </div>

  <!-- Laws Card -->
  <div class="stat-card animate-fade-in-up" style="animation-delay: 200ms;">
    <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-success opacity-10 rounded-full -translate-y-16 translate-x-16"></div>
    <div class="relative z-10">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-gray-600 uppercase tracking-wide">Law Projects</h3>
        <svg class="w-6 h-6 text-emerald-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <p class="text-4xl font-bold text-emerald-600 mb-2">{animatedTotalLaws}</p>
      <div class="space-y-1">
        {#each lawStatusBreakdown as status}
          <div class="flex items-center justify-between text-sm">
            <span class="text-gray-600 capitalize">{status.status.replace('_', ' ')}</span>
            <span class="font-medium text-gray-800">{status.count}</span>
          </div>
        {/each}
      </div>
    </div>
  </div>

  <!-- Committees Card -->
  <div class="stat-card animate-fade-in-up" style="animation-delay: 300ms;">
    <div class="absolute top-0 right-0 w-32 h-32 bg-gradient-accent opacity-10 rounded-full -translate-y-16 translate-x-16"></div>
    <div class="relative z-10">
      <div class="flex items-center justify-between mb-2">
        <h3 class="text-sm font-medium text-gray-600 uppercase tracking-wide">Committees</h3>
        <svg class="w-6 h-6 text-accent-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      </div>
      <p class="text-4xl font-bold gradient-text-accent mb-2">{animatedTotalCommittees}</p>
      <p class="text-sm text-gray-600">Specialized legislative bodies</p>
      <div class="mt-3 flex items-center gap-2">
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div class="bg-gradient-accent h-2 rounded-full" style="width: 75%;"></div>
        </div>
        <span class="text-xs text-gray-500">75% active</span>
      </div>
    </div>
  </div>
</div>
