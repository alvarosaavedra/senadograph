# Filter Presets Implementation Plan

## Overview
Create a preset system for graph filters to enable users to quickly find interesting relationships between nodes in the senator network graph.

## Goals
- Provide 5 pre-configured filter presets covering different relationship aspects
- Enable one-click preset application
- Support bilingual (ES/EN) preset descriptions
- Maintain existing filter functionality

## Proposed Presets

### 1. Partisan Polarization (党派极化 / Polarización Partidista)
**Purpose**: Visualize how parties vote differently and identify party boundaries

**Filters**:
- Entity Types: Senators, Parties
- Relationships: belongs_to, voted_same
- Agreement Range: 0-60% (showing low agreement = polarization)
- Active Only: true

**Expected Insights**: See which senators/parties rarely agree, visualize party voting blocs

---

### 2. Cross-Party Allies (跨党派盟友 / Alianzas Transpartidistas)
**Purpose**: Find senators who collaborate across party lines despite different affiliations

**Filters**:
- Entity Types: Senators, Parties
- Relationships: belongs_to, voted_same
- Agreement Range: 70-100% (high agreement)
- Show edges only between different parties
- Active Only: true

**Expected Insights**: Identify unexpected collaborations, moderate senators, potential bridges

---

### 3. Power Brokers (权力掮客 / Mediadores de Poder)
**Purpose**: Identify most influential senators through authored laws, committees, and connections

**Filters**:
- Entity Types: Senators, Laws, Committees, Parties
- Relationships: authored, member_of, belongs_to
- Law Statuses: approved (successful legislation)
- Active Only: true

**Expected Insights**: See which senators are most productive, their party connections, committee roles

---

### 4. Industry Influence (行业影响力 / Influencia Industrial)
**Purpose**: Reveal which industries/lobbyists influence which senators

**Filters**:
- Entity Types: Senators, Lobbyists
- Relationships: lobby
- Lobbyist Types: All (with type visible in UI)
- Active Only: true

**Expected Insights**: Map lobbyist networks, see industry connections, identify potential conflicts

---

### 5. Legislative Collaboration (立法合作 / Colaboración Legislativa)
**Purpose**: Show collaboration patterns through law authorship and voting patterns

**Filters**:
- Entity Types: Senators, Laws, Parties
- Relationships: authored, voted_on, voted_same, belongs_to
- Agreement Range: 60-100%
- Law Statuses: approved, in_discussion
- Active Only: true

**Expected Insights**: Understand legislative dynamics, see who works together on laws

---

## Implementation Phases

### Phase 1: Preset System Structure
**Tasks**:
1. Define `FilterPreset` type in `$lib/types/index.ts`
2. Create `$lib/config/presets.ts` configuration file
3. Add i18n keys for preset names and descriptions

**Type Definition**:
```typescript
export interface FilterPreset {
  id: string;
  nameEs: string;
  nameEn: string;
  descriptionEs: string;
  descriptionEn: string;
  filters: GraphFilters;
}
```

**Deliverable**: Type definitions and preset data structure

---

### Phase 2: Preset Configuration
**Tasks**:
1. Implement all 5 presets in `presets.ts`
2. Ensure filter configurations match expected GraphFilters interface
3. Add utility function `applyPreset(id: string): GraphFilters`

**Deliverable**: Complete preset configurations

---

### Phase 3: UI Integration
**Tasks**:
1. Create `PresetSelector.svelte` component
2. Add preset dropdown/selector above FilterPanel in `+page.svelte`
3. Implement one-click preset application
4. Add "Reset to Default" button
5. Show preset description when selected

**Component Structure**:
```svelte
<script lang="ts">
  import { presets } from '$lib/config/presets';
  export let onApplyPreset: (presetId: string) => void;
  export let onReset: () => void;
</script>

<select on:change={(e) => onApplyPreset(e.target.value)}>
  <option value="">-- Select Preset --</option>
  {#each presets as preset}
    <option value={preset.id}>{presets.name}</option>
  {/each}
</select>
```

**Deliverable**: Functional preset selector UI

---

### Phase 4: i18n Integration
**Tasks**:
1. Add preset translations to `src/lib/i18n/es.json`
2. Add preset translations to `src/lib/i18n/en.json`
3. Update PresetSelector to use i18n

**Translation Keys**:
```json
{
  "presets": {
    "polarization": {
      "name": "Polarización Partidista",
      "description": "Visualice cómo los partidos votan de manera diferente"
    },
    // ... other presets
  }
}
```

**Deliverable**: Bilingual preset support

---

### Phase 5: Testing & Polish
**Tasks**:
1. Test each preset application
2. Verify filter combinations work correctly
3. Check UI in both languages
4. Add hover tooltips for preset descriptions
5. Ensure responsive design

**Deliverable**: Tested, polished feature

---

## Files to Create/Modify

### New Files
- `src/lib/config/presets.ts` - Preset configurations
- `src/lib/components/ui/PresetSelector.svelte` - Preset selection UI

### Modified Files
- `src/lib/types/index.ts` - Add FilterPreset type
- `src/routes/+page.svelte` - Integrate PresetSelector
- `src/lib/i18n/es.json` - Spanish translations
- `src/lib/i18n/en.json` - English translations

---

## Testing Checklist

- [ ] Each preset applies correct filters
- [ ] Preset selector appears above filter panel
- [ ] "Reset to Default" clears preset and restores defaults
- [ ] Preset descriptions display correctly in ES and EN
- [ ] Filter panel updates when preset is applied
- [ ] Graph refreshes with filtered data
- [ ] No console errors in browser
- [ ] Works on mobile/tablet (responsive)

---

## Future Enhancements

- Custom preset creation (save current filters as preset)
- Preset sharing (URL parameters)
- Preset analytics (which presets are most used)
- Additional topic-based presets
- Dynamic preset suggestions based on user behavior
