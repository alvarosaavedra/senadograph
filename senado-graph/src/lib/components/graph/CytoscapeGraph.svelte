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
        'label': 'data(label)',
        'font-size': '12px',
        'text-valign': 'bottom',
        'text-halign': 'center',
        'text-background-color': '#ffffff',
        'text-background-opacity': 0.9,
        'text-background-padding': '3px',
        'text-margin-y': 5,
        'border-width': 2,
        'border-color': '#ffffff',
        'border-opacity': 0.8,
        'transition-property': 'width, height, border-width, border-color',
        'transition-duration': '0.2s'
      }
    },
    {
      selector: 'node[type="senator"]',
      style: {
        'shape': 'ellipse',
        'width': 45,
        'height': 45,
        'background-color': 'data(color)',
        'background-blacken': 0
      }
    },
    {
      selector: 'node[type="senator"]:hover',
      style: {
        'width': 52,
        'height': 52,
        'border-width': 4,
        'border-color': '#fbbf24',
        'border-opacity': 1,
        'box-shadow': '0 0 20px rgba(251, 191, 36, 0.5)'
      }
    },
    {
      selector: 'node[type="law"]',
      style: {
        'shape': 'roundrectangle',
        'width': 50,
        'height': 35,
        'background-color': (ele: cytoscape.NodeSingular) => {
          const status = ele.data('status');
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
      }
    },
    {
      selector: 'node[type="law"]:hover',
      style: {
        'width': 58,
        'height': 40,
        'border-width': 4,
        'border-color': '#fbbf24',
        'border-opacity': 1
      }
    },
    {
      selector: 'node[type="party"]',
      style: {
        'shape': 'diamond',
        'width': 60,
        'height': 60,
        'background-color': 'data(color)',
        'border-width': 3,
        'border-color': '#ffffff',
        'font-size': '14px',
        'font-weight': 'bold'
      }
    },
    {
      selector: 'node[type="party"]:hover',
      style: {
        'width': 70,
        'height': 70,
        'border-width': 5,
        'border-color': '#fbbf24',
        'border-opacity': 1
      }
    },
    {
      selector: 'node[type="committee"]',
      style: {
        'shape': 'hexagon',
        'width': 40,
        'height': 40,
        'background-color': '#8b5cf6',
        'background-gradient-stop-colors': '#8b5cf6, #ec4899',
        'background-gradient-direction': 'to-bottom'
      }
    },
    {
      selector: 'node[type="committee"]:hover',
      style: {
        'width': 48,
        'height': 48,
        'border-width': 4,
        'border-color': '#fbbf24',
        'border-opacity': 1
      }
    },
    {
      selector: 'node[type="lobbyist"]',
      style: {
        'shape': 'ellipse',
        'width': 30,
        'height': 30,
        'background-color': (ele: cytoscape.NodeSingular) => {
          const type = ele.data('lobbyistType');
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
      }
    },
    {
      selector: 'node[type="lobbyist"]:hover',
      style: {
        'width': 36,
        'height': 36,
        'border-width': 3,
        'border-color': '#fbbf24',
        'border-opacity': 1
      }
    },
    {
      selector: 'edge',
      style: {
        'width': 1.5,
        'line-color': '#94a3b8',
        'target-arrow-color': '#94a3b8',
        'curve-style': 'bezier',
        'opacity': 0.5,
        'transition-property': 'width, opacity, line-color',
        'transition-duration': '0.2s'
      }
    },
    {
      selector: 'edge[type="authored"]',
      style: {
        'width': 2.5,
        'line-color': '#3b82f6',
        'target-arrow-color': '#3b82f6',
        'target-arrow-shape': 'triangle',
        'opacity': 0.7
      }
    },
    {
      selector: 'edge[type="member_of"]',
      style: {
        'width': 1.5,
        'line-color': '#8b5cf6',
        'line-style': 'dashed',
        'line-dash-pattern': [6, 3],
        'opacity': 0.6
      }
    },
    {
      selector: 'edge[type="belongs_to"]',
      style: {
        'width': 1,
        'line-color': '#94a3b8',
        'opacity': 0.4
      }
    },
    {
      selector: 'edge[type="lobby"]',
      style: {
        'width': 2,
        'line-color': '#f97316',
        'line-style': 'dotted',
        'line-dash-pattern': [2, 2],
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
        'line-color': (ele: cytoscape.EdgeSingular) => {
          const agreement = ele.data('agreement') || 0.5;
          if (agreement > 0.8) return '#10b981';
          if (agreement > 0.6) return '#3b82f6';
          if (agreement > 0.4) return '#f59e0b';
          return '#ef4444';
        },
        'opacity': (ele: cytoscape.EdgeSingular) => {
          const agreement = ele.data('agreement') || 0.5;
          return 0.2 + agreement * 0.5;
        }
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
    },
    {
      selector: '.dimmed',
      style: {
        'opacity': 0.3
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
      minZoom: 0.15,
      maxZoom: 3,
      wheelSensitivity: 0.25
    });

    // Add click handler
    cy.on('tap', 'node', (evt) => {
      const node = evt.target;
      onNodeClick(node.id(), node.data('type'));
    });

    // Add hover handlers for highlighting connections
    cy.on('mouseover', 'node', (evt) => {
      const node = evt.target;
      highlightConnections(node.id());
    });

    cy.on('mouseout', 'node', () => {
      clearHighlight();
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
      animationDuration: 1500,
      animationEasing: 'ease-out',
      fit: true,
      padding: 50,
      nodeRepulsion: 8000,
      idealEdgeLength: 100,
      edgeElasticity: 0.45,
      gravity: 0.1,
      numIter: 2500,
      randomize: true,
      componentSpacing: 150,
      nestingFactor: 0.1,
      nodeOverlap: 10,
      initialTemp: 200,
      coolingFactor: 0.95
    });

    layout.run();
  }

  function highlightConnections(nodeId: string) {
    if (!cy) return;

    const node = cy.getElementById(nodeId);
    const neighborhood = node.neighborhood().add(node);

    cy.elements().addClass('dimmed');
    neighborhood.removeClass('dimmed');
  }

  function clearHighlight() {
    if (!cy) return;
    cy.elements().removeClass('dimmed');
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
