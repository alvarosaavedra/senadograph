<script lang="ts">
  import { _ } from '$lib/i18n';
  
  export let data;
  
  $: ({ senator, laws, committees } = data);
</script>

<svelte:head>
  <title>{senator.name} - SenadoGraph</title>
  <meta name="description" content="{senator.name} - {senator.party}, {senator.region}" />
</svelte:head>

<!-- Back Navigation -->
<div class="mb-6">
  <a href="/" class="text-blue-600 hover:text-blue-800 flex items-center text-sm">
    <svg class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
      <path fill-rule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clip-rule="evenodd" />
    </svg>
    {$_('nav.home')}
  </a>
</div>

<!-- Senator Header -->
<div class="bg-white rounded-lg shadow-md overflow-hidden mb-8">
  <div class="px-6 py-6">
    <div class="flex flex-col md:flex-row md:items-center">
      {#if senator.photoUrl}
        <img 
          src={senator.photoUrl} 
          alt={senator.name}
          class="w-24 h-24 rounded-full object-cover mb-4 md:mb-0 md:mr-6"
        />
      {:else}
        <div class="w-24 h-24 rounded-full bg-gray-200 flex items-center justify-center mb-4 md:mb-0 md:mr-6">
          <svg class="h-12 w-12 text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
        </div>
      {/if}
      
      <div class="flex-1">
        <h1 class="text-2xl font-bold text-gray-900">{senator.name}</h1>
        <p class="text-lg text-gray-600">{senator.party}</p>
        <p class="text-sm text-gray-500">{senator.region}</p>
        
        {#if senator.email}
          <a 
            href="mailto:{senator.email}" 
            class="text-blue-600 hover:text-blue-800 text-sm mt-2 inline-block"
          >
            {senator.email}
          </a>
        {/if}
      </div>
    </div>
  </div>
</div>

<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
  <!-- Biography -->
  {#if senator.biography}
    <div class="lg:col-span-2">
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">{$_('senator.biography')}</h2>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-700 whitespace-pre-line">{senator.biography}</p>
        </div>
      </div>
    </div>
  {/if}

  <!-- Sidebar -->
  <div class="space-y-6">
    <!-- Committees -->
    {#if committees.length > 0}
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">{$_('senator.committees')}</h2>
        </div>
        <ul class="divide-y divide-gray-200">
          {#each committees as committee}
            <li class="px-6 py-3 text-sm text-gray-700">
              {committee.name}
            </li>
          {/each}
        </ul>
      </div>
    {/if}

    <!-- Authored Laws -->
    {#if laws.length > 0}
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">{$_('senator.authoredLaws')}</h2>
        </div>
        <ul class="divide-y divide-gray-200">
          {#each laws as law}
            <li>
              <a href="/ley/{law.id}" class="block px-6 py-3 hover:bg-gray-50">
                <p class="text-sm font-medium text-blue-600">{law.boletin}</p>
                <p class="text-xs text-gray-500 mt-1">{law.title}</p>
              </a>
            </li>
          {/each}
        </ul>
      </div>
    {/if}
  </div>
</div>
