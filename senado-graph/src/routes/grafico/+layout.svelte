<script lang="ts">
  import { setupI18n } from '$lib/i18n';
  import { _ } from 'svelte-i18n';
  import LanguageToggle from '$lib/components/ui/LanguageToggle.svelte';
  import '../../app.css';
  import { onMount } from 'svelte';

  let isReady = false;

  onMount(async () => {
    await setupI18n();
    isReady = true;
  });
</script>

{#if !isReady}
  <div class="min-h-screen flex items-center justify-center bg-gradient-page">
    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
  </div>
{:else}

<div class="h-screen flex flex-col overflow-hidden">
  <!-- Header -->
  <header class="glass-panel sticky top-0 z-30 border-b border-white/20 flex-shrink-0">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <a href="/" class="flex items-center space-x-3 group">
          <div class="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
            <svg class="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <span class="text-xl font-bold gradient-text">SenadoGraph</span>
        </a>

        <!-- Navigation -->
        <nav class="flex items-center space-x-6">
          <a href="/" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-300 hover:bg-primary-50">
            {$_('nav.home')}
          </a>
          <a href="/grafico" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-300 hover:bg-primary-50">
            {$_('nav.graph')}
          </a>
          <a href="/sobre" class="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-300 hover:bg-primary-50">
            {$_('nav.about')}
          </a>
          <LanguageToggle />
        </nav>
      </div>
    </div>
  </header>

  <!-- Main Content - Full height minus header -->
  <main class="flex-1 overflow-hidden relative">
    <slot />
  </main>
</div>
{/if}
