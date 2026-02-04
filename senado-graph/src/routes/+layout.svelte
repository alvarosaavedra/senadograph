<script lang="ts">
  import { setupI18n } from '$lib/i18n';
  import { _ } from 'svelte-i18n';
  import LanguageToggle from '$lib/components/ui/LanguageToggle.svelte';
  import '../app.css';
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

<div class="min-h-screen bg-gradient-page flex flex-col">
  <!-- Header -->
  <header class="glass-panel sticky top-0 z-30 border-b border-white/20">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-20">
        <!-- Logo -->
        <a href="/" class="flex items-center space-x-3 group">
          <div class="w-10 h-10 rounded-lg bg-gradient-primary flex items-center justify-center shadow-glow group-hover:scale-110 transition-transform duration-300">
            <svg class="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <span class="text-2xl font-bold gradient-text">SenadoGraph</span>
        </a>

        <!-- Navigation -->
        <nav class="flex items-center space-x-6">
          <a href="/" class="text-gray-700 hover:text-primary-600 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-300 hover:bg-primary-50">
            {$_('nav.home')}
          </a>
          <a href="/grafico" class="text-gray-700 hover:text-primary-600 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-300 hover:bg-primary-50">
            {$_('nav.graph')}
          </a>
          <a href="/sobre" class="text-gray-700 hover:text-primary-600 px-4 py-2 rounded-lg text-sm font-medium transition-colors duration-300 hover:bg-primary-50">
            {$_('nav.about')}
          </a>
          <LanguageToggle />
        </nav>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <slot />
  </main>

  <!-- Footer -->
  <footer class="glass-panel border-t border-white/20 mt-16">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex flex-col md:flex-row justify-between items-center space-y-6 md:space-y-0">
        <div class="flex items-center space-x-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-primary flex items-center justify-center">
            <svg class="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
            </svg>
          </div>
          <span class="text-lg font-bold gradient-text">SenadoGraph</span>
        </div>

        <div class="flex flex-col md:flex-row items-center space-y-4 md:space-y-0 md:space-x-8 text-sm text-gray-600">
          <p class="flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
            </svg>
            <span>Open Source</span>
          </p>
          <p class="flex items-center space-x-2">
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <span>Data Disclaimer</span>
          </p>
          <p>© {new Date().getFullYear()} All rights reserved</p>
        </div>
      </div>

      <div class="mt-6 pt-6 border-t border-white/20 text-center">
        <p class="text-xs text-gray-500">
          Exploring Chilean Senate's relationships through data visualization
        </p>
      </div>
    </div>
  </footer>
</div>
{/if}
