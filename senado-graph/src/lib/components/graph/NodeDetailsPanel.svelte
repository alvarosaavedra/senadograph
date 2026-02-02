<script lang="ts">
  import type { NodeType, EdgeType } from '$lib/types';

  export let isOpen: boolean = false;
  export let nodeData: {
    id: string;
    label: string;
    type: NodeType;
    color?: string;
    status?: string;
    ideology?: string;
    lobbyistType?: string;
    party?: string;
    region?: string;
    agreement?: number;
    memberCount?: number;
    topic?: string;
    industry?: string;
    email?: string;
    biography?: string;
  } | null = null;
  export let connectedNodes: Array<{
    id: string;
    label: string;
    type: NodeType;
    edgeType: EdgeType;
  }> = [];
  export let onClose: () => void = () => {};

  $: initials = nodeData?.label.split(' ').map(n => n[0]).join('').slice(0, 2) || '';
  $: typeColor = getNodeColor(nodeData?.type);
  $: typeIcon = getNodeIcon(nodeData?.type);

  function getNodeColor(type?: NodeType): string {
    switch (type) {
      case 'senator':
        return nodeData?.color || '#3b82f6';
      case 'law':
        return getStatusColor(nodeData?.status);
      case 'party':
        return nodeData?.color || '#8b5cf6';
      case 'committee':
        return '#8b5cf6';
      case 'lobbyist':
        return getLobbyistColor(nodeData?.lobbyistType);
      default:
        return '#94a3b8';
    }
  }

  function getStatusColor(status?: string): string {
    switch (status) {
      case 'approved':
        return '#10b981';
      case 'rejected':
        return '#ef4444';
      case 'in_discussion':
        return '#3b82f6';
      case 'withdrawn':
        return '#6b7280';
      default:
        return '#94a3b8';
    }
  }

  function getLobbyistColor(type?: string): string {
    switch (type) {
      case 'company':
        return '#f97316';
      case 'union':
        return '#fbbf24';
      case 'ngo':
        return '#14b8a6';
      case 'professional_college':
        return '#6366f1';
      default:
        return '#94a3b8';
    }
  }

  function getNodeIcon(type?: NodeType) {
    switch (type) {
      case 'senator':
        return 'person';
      case 'law':
        return 'document';
      case 'party':
        return 'group';
      case 'committee':
        return 'users';
      case 'lobbyist':
        return 'building';
      default:
        return 'circle';
    }
  }
</script>

{#if isOpen}
  <div
    class="overlay"
    class:open={isOpen}
    on:click={onClose}
  ></div>

  <div
    class="slide-in-right overflow-y-auto animate-slide-in-right"
    class:open={isOpen}
  >
    {#if nodeData}
      <div class="sticky top-0 glass-panel border-b border-white/20 px-6 py-4 z-10 flex items-center justify-between">
        <h2 class="text-xl font-bold gradient-text">{nodeData.label}</h2>
        <button
          on:click={onClose}
          class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
          aria-label="Close panel"
        >
          <svg class="w-6 h-6 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
          </svg>
        </button>
      </div>

      <div class="p-6 space-y-6">
        <!-- Header -->
        <div class="flex items-start gap-4">
          <div class="flex-shrink-0 w-16 h-16 rounded-xl flex items-center justify-center shadow-lg" style="background-color: {typeColor};">
            <svg class="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              {#if nodeData.type === 'senator'}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              {:else if nodeData.type === 'law'}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              {:else if nodeData.type === 'party'}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
              {:else if nodeData.type === 'committee'}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
              {:else if nodeData.type === 'lobbyist'}
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
              {/if}
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <p class="text-sm text-gray-500 capitalize font-medium">{nodeData.type}</p>
            <p class="text-xs text-gray-400 mt-1">ID: {nodeData.id}</p>
          </div>
        </div>

        <!-- Details based on type -->
        <div class="space-y-4">
          {#if nodeData.type === 'senator'}
            <div class="glass-panel rounded-xl p-4 space-y-3">
              <div class="flex items-center gap-2 text-sm">
                <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span class="font-medium">Party:</span>
                <span class="text-gray-700">{nodeData.party || 'N/A'}</span>
              </div>
              <div class="flex items-center gap-2 text-sm">
                <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span class="font-medium">Region:</span>
                <span class="text-gray-700">{nodeData.region || 'N/A'}</span>
              </div>
              {#if nodeData.email}
                <div class="flex items-center gap-2 text-sm">
                  <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span class="font-medium">Email:</span>
                  <a href="mailto:{nodeData.email}" class="text-primary-600 hover:underline">{nodeData.email}</a>
                </div>
              {/if}
              {#if nodeData.agreement}
                <div class="flex items-center gap-2 text-sm">
                  <svg class="w-4 h-4 text-success-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span class="font-medium">Voting Agreement:</span>
                  <span class="font-semibold text-success-600">{(nodeData.agreement * 100).toFixed(1)}%</span>
                </div>
              {/if}
            </div>
          {:else if nodeData.type === 'law'}
            <div class="glass-panel rounded-xl p-4 space-y-3">
              <div class="flex items-center gap-2 text-sm">
                <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                <span class="font-medium">Status:</span>
                <span class="px-2 py-0.5 text-xs font-semibold rounded-full" style="background-color: {getStatusColor(nodeData.status)}20; color: {getStatusColor(nodeData.status)};">
                  {nodeData.status?.replace('_', ' ') || 'N/A'}
                </span>
              </div>
              {#if nodeData.topic}
                <div class="flex items-center gap-2 text-sm">
                  <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                  </svg>
                  <span class="font-medium">Topic:</span>
                  <span class="text-gray-700 capitalize">{nodeData.topic}</span>
                </div>
              {/if}
            </div>
          {:else if nodeData.type === 'party'}
            <div class="glass-panel rounded-xl p-4 space-y-3">
              <div class="flex items-center gap-2 text-sm">
                <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span class="font-medium">Ideology:</span>
                <span class="text-gray-700 capitalize">{nodeData.ideology || 'N/A'}</span>
              </div>
              {#if nodeData.memberCount}
                <div class="flex items-center gap-2 text-sm">
                  <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z" />
                  </svg>
                  <span class="font-medium">Members:</span>
                  <span class="text-gray-700">{nodeData.memberCount}</span>
                </div>
              {/if}
            </div>
          {:else if nodeData.type === 'committee'}
            <div class="glass-panel rounded-xl p-4">
              <p class="text-sm text-gray-600">Legislative committee for specialized law review and discussion.</p>
            </div>
          {:else if nodeData.type === 'lobbyist'}
            <div class="glass-panel rounded-xl p-4 space-y-3">
              <div class="flex items-center gap-2 text-sm">
                <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                </svg>
                <span class="font-medium">Type:</span>
                <span class="text-gray-700 capitalize">{nodeData.lobbyistType?.replace('_', ' ') || 'N/A'}</span>
              </div>
              {#if nodeData.industry}
                <div class="flex items-center gap-2 text-sm">
                  <svg class="w-4 h-4 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                  <span class="font-medium">Industry:</span>
                  <span class="text-gray-700">{nodeData.industry}</span>
                </div>
              {/if}
            </div>
          {/if}

          {#if nodeData.biography}
            <div class="glass-panel rounded-xl p-4">
              <h3 class="font-semibold text-gray-900 mb-2">Biography</h3>
              <p class="text-sm text-gray-700">{nodeData.biography}</p>
            </div>
          {/if}

          <!-- Connected Nodes -->
          {#if connectedNodes.length > 0}
            <div>
              <h3 class="font-semibold text-gray-900 mb-3 flex items-center gap-2">
                <svg class="w-5 h-5 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                </svg>
                Connected Entities ({connectedNodes.length})
              </h3>
              <div class="space-y-2">
                {#each connectedNodes as connection}
                  <div class="glass-panel rounded-lg p-3 flex items-center justify-between hover:bg-white/50 transition-colors cursor-pointer">
                    <div class="flex items-center gap-3">
                      <div class="w-8 h-8 rounded-lg flex items-center justify-center text-xs font-bold text-white" style="background-color: {getNodeColor(connection.type)};">
                        {connection.label.split(' ').map(n => n[0]).join('').slice(0, 2)}
                      </div>
                      <div>
                        <p class="text-sm font-medium text-gray-900">{connection.label}</p>
                        <p class="text-xs text-gray-500 capitalize">{connection.type}</p>
                      </div>
                    </div>
                    <span class="text-xs px-2 py-1 rounded-full bg-gray-100 text-gray-600 capitalize">
                      {connection.edgeType.replace('_', ' ')}
                    </span>
                  </div>
                {/each}
              </div>
            </div>
          {/if}
        </div>
      </div>
    {/if}
  </div>
{/if}
