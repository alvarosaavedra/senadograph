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
  let isInitializing = false;

   function initCytoscape() {
     if (!container || !graphData || isInitialized || isInitializing) {
       console.log('Cytoscape: init skipped', { container: !!container, graphData: !!graphData, isInitialized, isInitializing });
       return;
     }

     if (!graphData.nodes || graphData.nodes.length === 0) {
       console.warn('Cytoscape: No nodes to render');
       return;
     }

     isInitializing = true;
     console.log('Cytoscape: Initializing with', graphData.nodes.length, 'nodes and', graphData.edges?.length || 0, 'edges');

      try {
        console.log('Cytoscape: Initializing without styles first');

        const elements = {
          nodes: graphData.nodes.map(n => ({
            data: {
              ...n.data
            }
          })),
          edges: graphData.edges || []
        };

        console.log('Cytoscape: elements count:', elements.nodes.length, 'nodes,', elements.edges.length, 'edges');
        console.log('Cytoscape: voted_same edges on init:', elements.edges.filter(e => e.data?.type === 'voted_same').length);

        try {
          cy = cytoscape({
            container,
            elements,
            layout: { name: 'preset' },
            minZoom: 0.15,
            maxZoom: 3,
            wheelSensitivity: 0.25,
            style: [
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
                  'transition-duration': 200
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
                  'border-opacity': 1
                }
              },
              {
                selector: 'node[type="law"]',
                style: {
                  'shape': 'roundrectangle',
                  'width': 50,
                  'height': 35,
                  'background-color': '#3b82f6'
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
                  'background-color': '#cccccc',
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
                  'background-color': '#8b5cf6'
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
                  'background-color': '#94a3b8'
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
                  'transition-duration': 200,
                  'label': '',
                  'font-size': '10px',
                  'text-background-color': '#ffffff',
                  'text-background-opacity': 0.8,
                  'text-background-padding': '2px',
                  'text-margin-y': -10
                }
              },
              {
                selector: 'edge:hover',
                style: {
                  'width': 3,
                  'opacity': 0.9,
                  'label': 'data(type)',
                  'color': '#374151',
                  'font-weight': 'bold'
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
                selector: 'edge[type="authored"]:hover',
                style: {
                  'width': 4,
                  'opacity': 1,
                  'line-color': '#2563eb'
                }
              },
              {
                selector: 'edge[type="member_of"]',
                style: {
                  'width': 1.5,
                  'line-color': '#8b5cf6',
                  'line-style': 'dashed',
                  'opacity': 0.6
                }
              },
              {
                selector: 'edge[type="member_of"]:hover',
                style: {
                  'width': 3,
                  'opacity': 1,
                  'line-color': '#7c3aed'
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
                selector: 'edge[type="belongs_to"]:hover',
                style: {
                  'width': 2.5,
                  'opacity': 0.8,
                  'line-color': '#64748b'
                }
              },
              {
                selector: 'edge[type="lobby"]',
                style: {
                  'width': 2,
                  'line-color': '#f97316',
                  'line-style': 'dotted',
                  'opacity': 0.6
                }
              },
              {
                selector: 'edge[type="lobby"]:hover',
                style: {
                  'width': 3.5,
                  'opacity': 1,
                  'line-color': '#ea580c'
                }
              },
              {
                selector: 'edge[type="voted_same"]',
                style: {
                  'width': 2.5,
                  'line-color': '#10b981',
                  'opacity': 0.5
                }
              },
              {
                selector: 'edge[type="voted_same"]:hover',
                style: {
                  'width': 4,
                  'opacity': 1,
                  'line-color': '#059669'
                }
              },
              {
                selector: 'edge[type="voted_on"]',
                style: {
                  'width': 3,
                  'line-color': '#6b7280',
                  'target-arrow-shape': 'triangle',
                  'target-arrow-color': '#6b7280',
                  'opacity': 0.7
                }
              },
              {
                selector: 'edge[type="voted_on"][vote="favor"]',
                style: {
                  'line-color': '#22c55e',
                  'target-arrow-color': '#22c55e'
                }
              },
              {
                selector: 'edge[type="voted_on"][vote="against"]',
                style: {
                  'line-color': '#ef4444',
                  'target-arrow-color': '#ef4444'
                }
              },
              {
                selector: 'edge[type="voted_on"][vote="abstained"]',
                style: {
                  'line-color': '#eab308',
                  'target-arrow-color': '#eab308'
                }
              },
              {
                selector: 'edge[type="voted_on"][vote="absent"]',
                style: {
                  'line-color': '#6b7280',
                  'target-arrow-color': '#6b7280'
                }
              },
              {
                selector: 'edge[type="voted_on"]:hover',
                style: {
                  'width': 4,
                  'opacity': 1
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
            ]
          });
          console.log('Cytoscape: initialized successfully');
        } catch (e) {
          console.error('Cytoscape init error:', e);
          throw e;
        }

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
     } catch (err) {
       console.error('Cytoscape: Failed to initialize', err);
     } finally {
       isInitializing = false;
     }
   }
  
   function runLayout() {
     if (!cy) return;

     // Use concentric layout for better visual separation
     layout = cy.layout({
       name: 'concentric',
       animate: true,
       animationDuration: 1500,
       animationEasing: 'ease-out',
       fit: true,
       padding: 150,
       minNodeSpacing: 80,
       concentric: function(node) {
         // Prioritize by type: parties in center, senators next, then others
         const type = node.data('type');
         if (type === 'party') return 4;
         if (type === 'senator') return 3;
         if (type === 'committee') return 2;
         if (type === 'law') return 1;
         return 0; // lobbyists outer ring
       },
       levelWidth: function(nodes) {
         return 2; // Width of each concentric level
       },
       nodeDimensionsIncludeLabels: true
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
    
    console.log('Cytoscape: updateGraph called with', graphData.nodes.length, 'nodes and', graphData.edges?.length || 0, 'edges');
    console.log('Cytoscape: voted_same edges:', graphData.edges?.filter(e => e.data.type === 'voted_same').length || 0);
    
    // Remove old elements
    cy.elements().remove();
    
    // Add new elements
    cy.add(graphData.nodes);
    cy.add(graphData.edges);
    
    console.log('Cytoscape: Elements added, total:', cy.elements().length, 'nodes:', cy.nodes().length, 'edges:', cy.edges().length);
    
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
     if (container) {
       container.id = 'cytoscape-container';
     }
   });
  
  onDestroy(() => {
    if (layout) {
      layout.stop();
    }
    if (cy) {
      cy.destroy();
    }
  });
  
    // Watch for graph data changes - only init if not already initialized
    $: if (graphData && container && !isInitialized && graphData.nodes?.length > 0) {
     console.log('Cytoscape: Reactive init triggered');
     initCytoscape();
   }

    // Update graph when data changes (if already initialized)
    $: if (graphData && container && isInitialized && cy && graphData.nodes?.length > 0) {
     console.log('Cytoscape: Reactive update triggered');
     updateGraph();
   }
</script>

<div bind:this={container} class="w-full h-full min-h-[500px]"></div>
