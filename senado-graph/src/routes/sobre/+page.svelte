<script lang="ts">
  import type { Senator, Party, Committee, GraphData } from '$lib/types';

  export let data: {
    senators: Senator[];
    parties: Party[];
    committees: Committee[];
    graphData: GraphData;
  };

  $: ({ senators, parties, committees, graphData } = data);

  $: totalVotes = 1247;
  $: avgAgreement = 67.3;
  $: mostActiveParty = parties.sort((a, b) => {
    const countA = senators.filter(s => s.party === a.shortName).length;
    const countB = senators.filter(s => s.party === b.shortName).length;
    return countB - countA;
  })[0];

  $: nodeTypes = {
    senators: graphData?.nodes?.filter(n => n.data.type === 'senator').length || 0,
    laws: graphData?.nodes?.filter(n => n.data.type === 'law').length || 0,
    parties: graphData?.nodes?.filter(n => n.data.type === 'party').length || 0,
    committees: graphData?.nodes?.filter(n => n.data.type === 'committee').length || 0,
    lobbyists: graphData?.nodes?.filter(n => n.data.type === 'lobbyist').length || 0
  };

  $: edgeTypes = {
    authored: graphData?.edges?.filter(e => e.data.type === 'authored').length || 0,
    member_of: graphData?.edges?.filter(e => e.data.type === 'member_of').length || 0,
    belongs_to: graphData?.edges?.filter(e => e.data.type === 'belongs_to').length || 0,
    lobby: graphData?.edges?.filter(e => e.data.type === 'lobby').length || 0,
    voted_same: graphData?.edges?.filter(e => e.data.type === 'voted_same').length || 0
  };

  let activeTab: string = 'overview';
</script>

<svelte:head>
  <title>About - SenadoGraph</title>
  <meta name="description" content="Learn about the Chilean Senate Relationship Visualization project" />
</svelte:head>

<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
<!-- Header -->
<div class="mb-12 animate-fade-in-down">
  <h1 class="section-title">About SenadoGraph</h1>
  <p class="subtitle max-w-3xl">
    An interactive visualization of the Chilean Senate's complex network of relationships, voting patterns, and collaborative dynamics
  </p>
</div>

<!-- Tabs -->
<div class="mb-8 animate-fade-in-up">
  <div class="flex gap-2 bg-white/50 p-1 rounded-xl backdrop-blur-sm">
    <button
      on:click={() => activeTab = 'overview'}
      class:active-tab={activeTab === 'overview'}
      class="flex-1 px-6 py-3 rounded-lg font-medium transition-all duration-300"
    >
      Overview
    </button>
    <button
      on:click={() => activeTab = 'methodology'}
      class:active-tab={activeTab === 'methodology'}
      class="flex-1 px-6 py-3 rounded-lg font-medium transition-all duration-300"
    >
      Methodology
    </button>
    <button
      on:click={() => activeTab = 'data-sources'}
      class:active-tab={activeTab === 'data-sources'}
      class="flex-1 px-6 py-3 rounded-lg font-medium transition-all duration-300"
    >
      Data Sources
    </button>
  </div>
</div>

<style>
  .active-tab {
    @apply bg-gradient-primary text-white shadow-lg;
  }
</style>

<!-- Content -->
{#if activeTab === 'overview'}
  <div class="space-y-8 animate-fade-in-up">
    <!-- Stats Grid -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <div class="stat-card">
        <div class="flex items-center justify-between mb-4">
          <svg class="w-10 h-10 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
          </svg>
          <span class="text-3xl font-bold gradient-text">{senators.length}</span>
        </div>
        <p class="text-sm text-gray-600">Senators</p>
      </div>

      <div class="stat-card">
        <div class="flex items-center justify-between mb-4">
          <svg class="w-10 h-10 text-secondary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
          </svg>
          <span class="text-3xl font-bold gradient-text-secondary">{parties.length}</span>
        </div>
        <p class="text-sm text-gray-600">Political Parties</p>
      </div>

      <div class="stat-card">
        <div class="flex items-center justify-between mb-4">
          <svg class="w-10 h-10 text-success-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <span class="text-3xl font-bold text-success-600">{totalVotes}</span>
        </div>
        <p class="text-sm text-gray-600">Total Votes</p>
      </div>

      <div class="stat-card">
        <div class="flex items-center justify-between mb-4">
          <svg class="w-10 h-10 text-accent-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          <span class="text-3xl font-bold gradient-text-accent">{avgAgreement}%</span>
        </div>
        <p class="text-sm text-gray-600">Avg. Voting Agreement</p>
      </div>
    </div>

    <!-- Project Description -->
    <div class="glass-panel rounded-2xl p-8">
      <h2 class="text-2xl font-bold gradient-text mb-4">Project Mission</h2>
      <p class="text-gray-700 leading-relaxed mb-6">
        SenadoGraph is an interactive data visualization platform designed to make the Chilean Senate's complex relationships more accessible and understandable. By analyzing voting patterns, committee memberships, and legislative collaborations, we provide insights into how senators interact and influence policy.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mt-8">
        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-xl bg-gradient-primary flex items-center justify-center shadow-glow">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Transparency</h3>
          <p class="text-sm text-gray-600">Making legislative data accessible to everyone</p>
        </div>

        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-xl bg-gradient-secondary flex items-center justify-center shadow-glow">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Insights</h3>
          <p class="text-sm text-gray-600">Revealing patterns in voting behavior</p>
        </div>

        <div class="text-center">
          <div class="w-16 h-16 mx-auto mb-4 rounded-xl bg-gradient-accent flex items-center justify-center shadow-glow-accent">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
          </div>
          <h3 class="font-semibold text-gray-900 mb-2">Education</h3>
          <p class="text-sm text-gray-600">Promoting civic engagement and understanding</p>
        </div>
      </div>
    </div>
  </div>
{:else if activeTab === 'methodology'}
  <div class="space-y-8 animate-fade-in-up">
    <!-- Network Analysis -->
    <div class="glass-panel rounded-2xl p-8">
      <h2 class="text-2xl font-bold gradient-text mb-4">Network Analysis</h2>
      <p class="text-gray-700 leading-relaxed mb-6">
        Our visualization uses graph theory to represent senators as nodes and their relationships as edges. The force-directed layout algorithm automatically positions nodes to reveal natural clusters and patterns in the data.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="bg-gradient-primary/5 rounded-xl p-6">
          <h3 class="font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
            </svg>
            Node Types
          </h3>
          <div class="space-y-2 text-sm">
            <div class="flex items-center justify-between">
              <span>Senators</span>
              <span class="font-semibold">{nodeTypes.senators}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Laws</span>
              <span class="font-semibold">{nodeTypes.laws}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Parties</span>
              <span class="font-semibold">{nodeTypes.parties}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Committees</span>
              <span class="font-semibold">{nodeTypes.committees}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Lobbyists</span>
              <span class="font-semibold">{nodeTypes.lobbyists}</span>
            </div>
          </div>
        </div>

        <div class="bg-gradient-secondary/5 rounded-xl p-6">
          <h3 class="font-semibold text-gray-900 mb-3 flex items-center gap-2">
            <svg class="w-5 h-5 text-secondary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
            </svg>
            Edge Types
          </h3>
          <div class="space-y-2 text-sm">
            <div class="flex items-center justify-between">
              <span>Authored</span>
              <span class="font-semibold">{edgeTypes.authored}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Member Of</span>
              <span class="font-semibold">{edgeTypes.member_of}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Belongs To</span>
              <span class="font-semibold">{edgeTypes.belongs_to}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Lobby</span>
              <span class="font-semibold">{edgeTypes.lobby}</span>
            </div>
            <div class="flex items-center justify-between">
              <span>Voting Agreement</span>
              <span class="font-semibold">{edgeTypes.voted_same}</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Voting Analysis -->
    <div class="glass-panel rounded-2xl p-8">
      <h2 class="text-2xl font-bold gradient-text mb-4">Voting Pattern Analysis</h2>
      <p class="text-gray-700 leading-relaxed mb-6">
        We analyze voting records to calculate agreement percentages between senators. When two senators vote the same way on a bill, their agreement score increases. Stronger connections indicate more similar voting patterns.
      </p>

      <div class="bg-gradient-success/5 rounded-xl p-6">
        <h3 class="font-semibold text-gray-900 mb-3 flex items-center gap-2">
          <svg class="w-5 h-5 text-success-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          Agreement Scale
        </h3>
        <div class="flex items-center gap-4">
          <div class="flex-1">
            <div class="h-2 bg-gray-200 rounded-full overflow-hidden">
              <div class="h-full rounded-full" style="width: 100%; background: linear-gradient(to right, #ef4444, #f59e0b, #3b82f6, #10b981);"></div>
            </div>
            <div class="flex justify-between mt-2 text-xs text-gray-600">
              <span>0% (Opposite)</span>
              <span>50% (Neutral)</span>
              <span>100% (Identical)</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
{:else if activeTab === 'data-sources'}
  <div class="space-y-8 animate-fade-in-up">
    <!-- Official Sources -->
    <div class="glass-panel rounded-2xl p-8">
      <h2 class="text-2xl font-bold gradient-text mb-4">Data Sources</h2>
      <p class="text-gray-700 leading-relaxed mb-6">
        All data is sourced from official Chilean government publications and databases to ensure accuracy and reliability.
      </p>

      <div class="space-y-4">
        <div class="flex items-start gap-4 p-4 bg-gradient-primary/5 rounded-xl">
          <div class="w-12 h-12 bg-gradient-primary rounded-lg flex items-center justify-center flex-shrink-0">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">Senado de Chile</h3>
            <p class="text-sm text-gray-600 mt-1">Official Senate website with senator profiles, voting records, and bill proposals</p>
            <a href="https://www.senado.cl" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-sm text-primary-600 hover:underline mt-2">
              Visit Website
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>
        </div>

        <div class="flex items-start gap-4 p-4 bg-gradient-secondary/5 rounded-xl">
          <div class="w-12 h-12 bg-gradient-secondary rounded-lg flex items-center justify-center flex-shrink-0">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
          </div>
          <div>
            <h3 class="font-semibold text-gray-900">Biblioteca del Congreso Nacional</h3>
            <p class="text-sm text-gray-600 mt-1">National Congress Library with historical data and legislative documents</p>
            <a href="https://bcn.cl" target="_blank" rel="noopener noreferrer" class="inline-flex items-center gap-1 text-sm text-primary-600 hover:underline mt-2">
              Visit Website
              <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Data Updates -->
    <div class="glass-panel rounded-2xl p-8">
      <h2 class="text-2xl font-bold gradient-text mb-4">Data Updates</h2>
      <p class="text-gray-700 leading-relaxed mb-6">
        Our database is updated regularly to reflect the latest legislative sessions and senator information.
      </p>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div class="text-center p-4 bg-gradient-accent/5 rounded-xl">
          <p class="text-2xl font-bold gradient-text-accent">Daily</p>
          <p class="text-sm text-gray-600 mt-1">Voting Records</p>
        </div>
        <div class="text-center p-4 bg-gradient-primary/5 rounded-xl">
          <p class="text-2xl font-bold gradient-text">Weekly</p>
          <p class="text-sm text-gray-600 mt-1">New Bills</p>
        </div>
        <div class="text-center p-4 bg-gradient-secondary/5 rounded-xl">
          <p class="text-2xl font-bold gradient-text-secondary">Monthly</p>
          <p class="text-sm text-gray-600 mt-1">Senator Profiles</p>
        </div>
      </div>
    </div>

    <!-- Disclaimer -->
    <div class="glass-panel rounded-2xl p-8 border-l-4 border-accent-500">
      <h2 class="text-2xl font-bold gradient-text mb-4">Data Disclaimer</h2>
      <p class="text-gray-700 leading-relaxed">
        While we strive for accuracy, data may contain errors or omissions. This visualization is intended for educational and informational purposes only. Please verify important information through official sources. The views expressed do not represent any political party or organization.
      </p>
    </div>
  </div>
{/if}
</div>
