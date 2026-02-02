<script lang="ts">
  import { _ } from '$lib/i18n';
  
  export let data;
  
  $: ({ law, authors } = data);
  
  function formatDate(dateString: string): string {
    return new Date(dateString).toLocaleDateString();
  }
</script>

<svelte:head>
  <title>{law.boletin} - SenadoGraph</title>
  <meta name="description" content="{law.title}" />
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

<!-- Law Header -->
<div class="bg-white rounded-lg shadow-md overflow-hidden mb-8">
  <div class="px-6 py-6">
    <div class="flex items-center justify-between mb-4">
      <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium
        {law.status === 'approved' ? 'bg-green-100 text-green-800' : 
         law.status === 'rejected' ? 'bg-red-100 text-red-800' : 
         law.status === 'withdrawn' ? 'bg-gray-100 text-gray-800' : 
         'bg-yellow-100 text-yellow-800'}">
        {$_(`status.${law.status}`)}
      </span>
      <span class="text-sm text-gray-500 font-mono">{law.boletin}</span>
    </div>
    
    <h1 class="text-2xl font-bold text-gray-900 mb-2">{law.title}</h1>
    
    {#if law.topic}
      <p class="text-sm text-gray-500 mb-4">{$_('law.topic')}: {law.topic}</p>
    {/if}
    
    <p class="text-sm text-gray-600">
      {$_('law.dateProposed')}: {formatDate(law.dateProposed)}
    </p>
  </div>
</div>

<div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
  <!-- Description -->
  {#if law.description}
    <div class="lg:col-span-2">
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">{$_('law.description')}</h2>
        </div>
        <div class="px-6 py-4">
          <p class="text-gray-700 whitespace-pre-line">{law.description}</p>
        </div>
      </div>
    </div>
  {/if}

  <!-- Sidebar -->
  <div class="space-y-6">
    <!-- Authors -->
    {#if authors.length > 0}
      <div class="bg-white rounded-lg shadow-md overflow-hidden">
        <div class="px-6 py-4 border-b border-gray-200">
          <h2 class="text-lg font-semibold text-gray-900">{$_('law.authors')}</h2>
        </div>
        <ul class="divide-y divide-gray-200">
          {#each authors as author}
            <li>
              <a href="/senador/{author.id}" class="block px-6 py-3 hover:bg-gray-50">
                <p class="text-sm font-medium text-blue-600">{author.name}</p>
                <p class="text-xs text-gray-500 mt-1">{author.party} • {author.region}</p>
              </a>
            </li>
          {/each}
        </ul>
      </div>
    {/if}
  </div>
</div>
