<script lang="ts">
  import { onMount, onDestroy } from 'svelte';
  import cytoscape from 'cytoscape';
  import type { GraphData } from '$lib/types';
  
  export let graphData: GraphData;
  export let onNodeClick: (nodeId: string, type: string) => void = () => {};
  
  let container: HTMLElement;
  let cy: cytoscape.Core;
  let layout: cytoscape.Layouts;
  let isInitialized = false;
  
  const style = [
    {
      selector: 'node',
      style: {
        'background-color': 'data(color)',
        'label': 'data(label)',
        'width': 40,
        'height': 40,
        'font-size': '12px',
        'text-valign': 'bottom',
        'text-halign': 'center',
        'text-background-color': '#ffffff',
        'text-background-opacity': 0.8,
        'text-background-padding': '2px',
        'text-margin-y': 4,
        'border-width': 2,
        'border-color': '#ffffff'
      }
    },
    {
      selector: 'node[type="senator"]',
      style: {
        'shape': 'ellipse',
        'width': 45,
        'height': 45
      }
    },
    {
      selector: 'node[type="law"]',
      style: {
        'shape': 'rectangle',
        'width': 35,
        'height': 35
      }
    },
    {
      selector: 'edge',
      style: {
        'width': 2,
        'line-color': '#94a3b8',
        'target-arrow-color': '#94a3b8',
        'target-arrow-shape': 'none',
        'curve-style': 'bezier',
        'opacity': 0.6
      }
    },
    {
      selector: 'edge[type="voted_same"]',
      style: {
        'width': (ele: cytoscape.EdgeSingular) => {
          const agreement = ele.data('agreement') || 0.5;
          return 1 + agreement * 3;
        },
        'line-color': '#64748b',
        'opacity': 0.4
      }
    },
    {
      selector: ':selected',
      style: {
        'border-width': 4,
        'border-color': '#fbbf24',
        'border-opacity': 1
      }
    },
    {
      selector: '.highlighted',
      style: {
        'border-width': 4,
        'border-color': '#fbbf24',
        'border-opacity': 1
      }
    }
  ];
  
  function initCytoscape() {
    if (!container || !graphData || isInitialized) return;
    
    cy = cytoscape({
      container,
      elements: {
        nodes: graphData.nodes,
        edges: graphData.edges
      },
      style: style as any,
      layout: { name: 'preset' },
      minZoom: 0.2,
      maxZoom: 3,
      wheelSensitivity: 0.3
    });
    
    // Add click handler
    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      onNodeClick(node.id(), node.data('type'));
    });
    
    isInitialized = true;
    
    // Run force-directed layout
    runLayout();
  }
  
  function runLayout() {
    if (!cy) return;
    
    layout = cy.layout({
      name: 'cose',
      animate: true,
      animationDuration: 1000,
      fit: true,
      padding: 30,
      nodeRepulsion: 4500,
      idealEdgeLength: 80,
      edgeElasticity: 0.45,
      gravity: 0.25,
      numIter: 2500,
      randomize: true,
      componentSpacing: 100,
      nestingFactor: 0.1
    });
    
    layout.run();
  }
  
  function updateGraph() {
    if (!cy || !graphData) return;
    
    // Remove old elements
    cy.elements().remove();
    
    // Add new elements
    cy.add(graphData.nodes);
    cy.add(graphData.edges);
    
    // Re-run layout
    runLayout();
  }
  
  export function zoomIn() {
    if (cy) {
      cy.zoom(cy.zoom() * 1.2);
    }
  }
  
  export function zoomOut() {
    if (cy) {
      cy.zoom(cy.zoom() * 0.8);
    }
  }
  
  export function fit() {
    if (cy) {
      cy.fit(undefined, 50);
    }
  }
  
  export function resetLayout() {
    runLayout();
  }
  
  onMount(() => {
    // Small delay to ensure container is ready and data is available
    setTimeout(() => {
      initCytoscape();
    }, 100);
  });
  
  onDestroy(() => {
    if (layout) {
      layout.stop();
    }
    if (cy) {
      cy.destroy();
    }
  });
  
  // Watch for graph data changes
  $: if (container && graphData) {
    if (!isInitialized) {
      initCytoscape();
    } else if (cy) {
      updateGraph();
    }
  }
</script>

<div bind:this={container} class="w-full h-full min-h-[500px]"></div>
