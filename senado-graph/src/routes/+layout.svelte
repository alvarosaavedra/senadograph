<script lang="ts">
  import { setupI18n } from '$lib/i18n';
  import '../app.css';
  
  // Setup i18n on client (updates locale from localStorage if available)
  setupI18n();
</script>

<div class="min-h-screen bg-gray-50">
  <!-- Header -->
  <header class="bg-white shadow-sm">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <a href="/" class="flex items-center space-x-2">
          <span class="text-xl font-bold text-blue-600">SenadoGraph</span>
        </a>
        
        <!-- Navigation -->
        <nav class="flex space-x-8">
          <a href="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
            Home
          </a>
          <a href="/sobre" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
            About
          </a>
        </nav>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <slot />
  </main>

  <!-- Footer -->
  <footer class="bg-white border-t mt-auto">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <div class="flex flex-col md:flex-row justify-between items-center space-y-4 md:space-y-0">
        <p class="text-sm text-gray-500">
          © {new Date().getFullYear()} SenadoGraph - Chilean Senate Relationship Visualization
        </p>
        <div class="flex space-x-4 text-sm text-gray-500">
          <span>Data Disclaimer</span>
        </div>
      </div>
    </div>
  </footer>
</div>
