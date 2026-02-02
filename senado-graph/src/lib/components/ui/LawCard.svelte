<script lang="ts">
  import type { Law, LawStatus } from '$lib/types';

  export let law: Law;
  export let compact: boolean = false;

  $: displayTitle = law.titleEn || law.title;

  function getStatusColor(status: LawStatus): string {
    switch (status) {
      case 'approved':
        return 'bg-green-100 text-green-800';
      case 'rejected':
        return 'bg-red-100 text-red-800';
      case 'in_discussion':
        return 'bg-yellow-100 text-yellow-800';
      case 'withdrawn':
        return 'bg-gray-100 text-gray-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }

  function getStatusLabel(status: LawStatus): string {
    const labels: Record<LawStatus, string> = {
      approved: 'Approved',
      rejected: 'Rejected',
      in_discussion: 'In Discussion',
      withdrawn: 'Withdrawn'
    };
    return labels[status] || status;
  }
</script>

{#if compact}
  <div class="p-3 bg-white rounded-lg border border-gray-200 hover:border-blue-300 transition-colors">
    <div class="flex items-start justify-between gap-2">
      <div class="flex-1 min-w-0">
        <p class="text-sm font-medium text-gray-900 truncate">{displayTitle}</p>
        <p class="text-xs text-gray-500 mt-0.5">{law.boletin}</p>
      </div>
      <span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium whitespace-nowrap {getStatusColor(law.status)}">
        {getStatusLabel(law.status)}
      </span>
    </div>
  </div>
{:else}
  <div class="bg-white rounded-lg shadow-md overflow-hidden border border-gray-200">
    <div class="p-4">
      <div class="flex items-start justify-between gap-3 mb-3">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium bg-blue-100 text-blue-800">
          {law.boletin}
        </span>
        <span class="inline-flex items-center px-2.5 py-0.5 rounded text-xs font-medium {getStatusColor(law.status)}">
          {getStatusLabel(law.status)}
        </span>
      </div>
      <h3 class="text-lg font-semibold text-gray-900 mb-2">{displayTitle}</h3>
      {#if law.description || law.descriptionEn}
        <p class="text-sm text-gray-600 mb-3 line-clamp-3">
          {law.descriptionEn || law.description}
        </p>
      {/if}
      <div class="flex flex-wrap gap-4 text-sm text-gray-500">
        <span>
          <span class="font-medium">Date Proposed:</span>
          {new Date(law.dateProposed).toLocaleDateString('en-US')}
        </span>
        {#if law.topic}
          <span>
            <span class="font-medium">Topic:</span>
            {law.topic}
          </span>
        {/if}
      </div>
    </div>
  </div>
{/if}

<style>
  .line-clamp-3 {
    display: -webkit-box;
    display: box;
    -webkit-line-clamp: 3;
    line-clamp: 3;
    -webkit-box-orient: vertical;
    box-orient: vertical;
    overflow: hidden;
  }
</style>
