# Graph Connections Enhancement Plan

## Goal
Transform the current graph visualization from showing disconnected nodes to a rich, interconnected network that reveals meaningful relationships between senators, laws, parties, committees, and lobbyists.

## Current State
- **Nodes shown:** Senators, Laws (disconnected)
- **Edges shown:** Only `voted_same` between senators (100 limit)
- **Missing:** Party, Committee, Lobbyist nodes and all their connections

## Target State
- **All node types:** Senators, Laws, Parties, Committees, Lobbyists
- **All edge types:** voted_same, authored, belongs_to, member_of, lobby
- **Toggle controls:** Users can show/hide specific connection types
- **Reduced data:** Better performance with focused, meaningful data

---

## Phase 1: Database Queries Enhancement

### Tasks:
1. [ ] **Update `getInitialGraphData()` in `queries.ts`**
   - Reduce law limit from 200 → 50
   - Reduce voted_same edges from 100 → 50
   - Add Party node query with member counts
   - Add Committee node query
   - Add Lobbyist node query (limit 30)
   - Add AUTHORED edge query (senator → law)
   - Add BELONGS_TO edge query (senator → party)
   - Add MEMBER_OF edge query (senator → committee)
   - Add LOBBY edge query (lobbyist → senator)

2. [ ] **Update `getFilteredGraphData()` in `graphData.ts`**
   - Implement same node/edge fetching as initial query
   - Add edge type filtering based on `relationshipTypes` parameter
   - Respect all existing filters (parties, committees, law statuses, etc.)

**Files to modify:**
- `/home/radbug/Work/relations/senado-graph/src/lib/database/queries.ts`
- `/home/radbug/Work/relations/senado-graph/src/lib/utils/graphData.ts`

---

## Phase 2: Type System Updates

### Tasks:
3. [ ] **Update `GraphFilters` interface in `types/index.ts`**
   - Add `relationshipTypes?: EdgeType[]` field
   - This will control which edge types are visible

**Files to modify:**
- `/home/radbug/Work/relations/senado-graph/src/lib/types/index.ts`

---

## Phase 3: Filter Panel UI Enhancement

### Tasks:
4. [ ] **Add Connection Type Toggles to FilterPanel**
   - New section "Show Connection Types"
   - 5 toggle buttons with icons/colors matching edge styles:
     - ✅ **Authored** (blue) - Senators → Laws
     - ✅ **Belongs to** (gray) - Senators → Parties  
     - ✅ **Member of** (purple dashed) - Senators → Committees
     - ✅ **Lobby** (orange dotted) - Lobbyists → Senators
     - ✅ **Voting agreement** (green) - Senators ↔ Senators
   - All enabled by default
   - Click to toggle on/off

5. [ ] **Update FilterPanel state management**
   - Add `selectedRelationshipTypes` array
   - Sync with `currentFilters.relationshipTypes`
   - Include in `handleApply()` and `handleClear()`

**Files to modify:**
- `/home/radbug/Work/relations/senado-graph/src/lib/components/ui/FilterPanel.svelte`

---

## Phase 4: Main Page Integration

### Tasks:
6. [ ] **Update `+page.svelte`**
   - Initialize `currentFilters` with default `relationshipTypes` (all 5 types)
   - Pass `relationshipTypes` to FilterPanel
   - Update `handleApplyFilters()` to include edge type filtering
   - Ensure edge counts reflect visible edges only

7. [ ] **Update server load function**
   - Modify `+page.server.ts` to pass initial filters with all relationship types enabled

**Files to modify:**
- `/home/radbug/Work/relations/senado-graph/src/routes/+page.svelte`
- `/home/radbug/Work/relations/senado-graph/src/routes/+page.server.ts`

---

## Phase 5: Graph Visualization Improvements

### Tasks:
8. [ ] **Update `CytoscapeGraph.svelte`**
   - Add edge labels showing connection type (on hover or always visible)
   - Adjust COSE layout parameters for better spacing:
     - Increase `idealEdgeLength` (100 → 150)
     - Adjust `nodeRepulsion` (8000 → 10000)
     - Increase `componentSpacing` (150 → 200)
   - Ensure edge filtering works correctly with toggle changes

9. [ ] **Edge styling verification**
   - Confirm all edge types have distinct visual styles:
     - `authored`: Blue, solid, arrow
     - `belongs_to`: Gray, thin solid
     - `member_of`: Purple, dashed
     - `lobby`: Orange, dotted
     - `voted_same`: Green, solid

**Files to modify:**
- `/home/radbug/Work/relations/senado-graph/src/lib/components/graph/CytoscapeGraph.svelte`

---

## Phase 6: Legend & Visual Feedback

### Tasks:
10. [ ] **Update `GraphLegend.svelte`**
    - Ensure all edge types are properly documented
    - Show counts for each edge type (passed from parent)
    - Add visual indicators matching the toggle colors

**Files to modify:**
- `/home/radbug/Work/relations/senado-graph/src/lib/components/graph/GraphLegend.svelte`

---

## Phase 7: API Endpoint Updates

### Tasks:
11. [ ] **Update `/api/graph` endpoint**
    - Modify `+server.ts` to handle `relationshipTypes` filter
    - Pass filter to `getFilteredGraphData()`
    - Return filtered edges based on selected types

**Files to modify:**
- `/home/radbug/Work/relations/senado-graph/src/routes/api/graph/+server.ts`

---

## Data Limits Summary

| Entity | Current Limit | New Limit | Reason |
|--------|--------------|-----------|---------|
| Laws | 200 | 50 | Reduce clutter, faster rendering |
| Voted Same edges | 100 | 50 | Focus on strongest relationships |
| Lobbyists | N/A | 30 | New data, prevent overcrowding |
| Senators | All active | All active | Core entity, show all |
| Parties | N/A | All | Few in number, show all |
| Committees | N/A | All | Few in number, show all |

---

## Edge Types Reference

| Type | Color | Style | Source → Target | Description |
|------|-------|-------|-----------------|-------------|
| `authored` | #3b82f6 (blue) | Solid, arrow | Senator → Law | Senator authored/proposed law |
| `belongs_to` | #94a3b8 (gray) | Thin solid | Senator → Party | Party membership |
| `member_of` | #8b5cf6 (purple) | Dashed | Senator → Committee | Committee membership |
| `lobby` | #f97316 (orange) | Dotted | Lobbyist → Senator | Lobbying relationship |
| `voted_same` | #10b981 (green) | Solid | Senator ↔ Senator | >70% voting agreement |

---

## Testing Checklist

- [ ] All 5 node types render correctly
- [ ] All 5 edge types render with correct styling
- [ ] Edge toggles work (show/hide specific connection types)
- [ ] Filters apply correctly with edge type selections
- [ ] Graph layout adjusts well with varying edge combinations
- [ ] Edge labels display correctly
- [ ] Legend updates with correct counts
- [ ] Mock data fallback works when Neo4j unavailable
- [ ] Performance is acceptable with reduced limits
- [ ] Hover highlighting works for all node/edge types

---

## Progress Tracking

Use this section to mark tasks as completed:

**Phase 1: Database Queries** □  
**Phase 2: Type System** □  
**Phase 3: Filter Panel** □  
**Phase 4: Main Page** □  
**Phase 5: Graph Visualization** □  
**Phase 6: Legend** □  
**Phase 7: API Endpoint** □  
**Testing** □  

---

## Notes

- Mock data already contains all edge types - no changes needed there
- The CytoscapeGraph component already has styling for all edge types
- NodeDetailsPanel already supports showing connected entities with edge types
- FilterPanel already has entity type toggles - we're adding relationship type toggles

## Estimated Impact

**Before:** ~50 senators + 200 disconnected law nodes + 100 voting edges  
**After:** ~50 senators + 50 laws + parties + committees + lobbyists + all connections (potentially 200+ edges)

The toggle system allows users to control complexity and focus on specific relationship types.
