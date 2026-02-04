# Clustering Proposals for SenadoGraph

This document outlines proposed clustering approaches for analyzing the Chilean Senate graph data.

## Current Graph Foundation

The system already has:
- **5 node types**: Senators, Parties, Laws, Committees, Lobbyists
- **6 relationship types**: AUTHORED, BELONGS_TO, MEMBER_OF, LOBBY, VOTED_SAME, VOTED_ON
- **Voting similarity** calculated using Jaccard index
- **Cytoscape.js** visualization with concentric layout
- **5 filter presets** for different views

## Proposed Clustering Approaches

### 1. Voting Pattern Clusters (Priority)

Enhance existing VOTED_SAME relationships to identify voting blocs:

**Algorithms to implement:**
- **Louvain/ Leiden community detection** - Identify natural voting communities
- **Hierarchical clustering** - Show nested voting blocs within parties
- **Dimensionality reduction** - Use t-SNE or UMAP to visualize senators in 2D voting space
- **Temporal clustering** - Track how voting blocs shift across legislative sessions

**Use cases:**
- Identify cross-party alliances
- Detect party defectors
- Find consensus builders vs. ideological purists
- Visualize polarization over time

### 2. Legislative Collaboration Networks

Focus on bill authorship patterns:

**Clustering methods:**
- **Co-authorship clustering** - Group senators who frequently co-author bills
- **Committee influence networks** - Weight by seniority + bill success rate
- **Cross-committee bridges** - Identify senators serving as connectors between committees

**Edge weights:**
- Number of co-authored bills
- Success rate of co-authored bills
- Committee overlap

### 3. Interest Group Clusters

Analyze lobbyist and funding patterns:

**Clustering dimensions:**
- **Industry alignment** - Group senators by lobbyist industry interactions
- **Funding correlation** - Connect senators receiving funding from same sources
- **Geographic clustering** - Regional voting patterns vs. party loyalty

**Potential insights:**
- Industry-specific voting blocs
- Regional vs. national party alignment
- Influence network visualization

### 4. Dynamic Temporal Clusters

Add time dimension to clustering:

**Temporal analyses:**
- **Session-by-session animation** - Watch cluster formation/breakdown over time
- **Issue-based clustering** - Cluster on specific topics (health, education, economy)
- **Predictive clustering** - ML-based prediction of future alliances

**Visualizations:**
- Animated graph showing cluster evolution
- Timeline with cluster transitions
- Heatmaps of voting similarity over time

### 5. Multi-dimensional Clustering

Combine multiple relationship types:

**Composite approaches:**
- **Integrated similarity score** - Combine voting + co-authorship + committee overlap
- **Role-based clustering** - Identify: Leaders, Mediators, Party Loyalists, Independents
- **Bipartisanship index** - Cluster by cross-party voting tendency

**Algorithms:**
- Weighted graph clustering
- Multi-view clustering (combining different relationship matrices)
- Spectral clustering on composite adjacency matrix

## Implementation Priority

### Phase 1: Voting Pattern Enhancement
1. Implement Louvain community detection on VOTED_SAME graph
2. Add cluster coloring to Cytoscape visualization
3. Create cluster statistics panel (size, cohesion, party breakdown)

### Phase 2: Collaboration Networks
1. Build co-authorship network analysis
2. Add committee influence metrics
3. Identify bridge senators (high betweenness centrality)

### Phase 3: Temporal Analysis
1. Add time filtering controls
2. Implement session-by-session clustering
3. Create cluster transition visualizations

### Phase 4: Advanced Clustering
1. Multi-dimensional similarity calculation
2. Role identification algorithms
3. Predictive clustering models

## Technical Considerations

**Libraries:**
- `community` (python-louvain) for Louvain algorithm
- `scikit-learn` for hierarchical clustering, t-SNE, UMAP
- `networkx` for graph algorithms (centrality, bridges)
- Cytoscape.js cola or dagre layouts for cluster visualization

**Performance:**
- Pre-compute cluster assignments for common thresholds
- Cache similarity matrices
- Use Web Workers for heavy calculations

**Data requirements:**
- All relationships already exist in Neo4j
- Vote dates available for temporal analysis
- Bill topics available for issue-based clustering

## Success Metrics

- **Cluster coherence** - High intra-cluster voting similarity
- **Cluster interpretability** - Clusters align with known political groups
- **Actionable insights** - Identify unexpected alliances and influence patterns
- **Visual clarity** - Clusters are visually distinct and meaningful
