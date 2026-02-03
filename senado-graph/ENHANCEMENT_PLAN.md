# SenadoGraph Visual & Feature Enhancement Plan

## Phase 1: Theme & Visual Design Foundation

### 1.1 Create Custom Tailwind Theme

- Configure custom color palette with vibrant gradients:
  - Primary: Purple-to-pink gradient (#8b5cf6 → #ec4899)
  - Secondary: Cyan-to-blue gradient (#06b6d4 → #3b82f6)
  - Accent: Amber-to-orange gradient (#f59e0b → #f97316)
  - Success: Emerald gradient (#10b981 → #34d399)
  - Background: Off-white with subtle gradient (#f8fafc → #f1f5f9)
- Add custom animations (fade-in, slide-up, pulse, bounce)
- Add glassmorphism utility classes
- Add custom shadows and glow effects

### 1.2 Update Layout with Dashboard Style

- Create animated stats cards:
  - Senators count with party breakdown
  - Active laws with status distribution
  - Committees total
  - Total relationships/votes
- Add hover effects with scale and shadow transitions
- Add animated number counters

## Phase 2: Enhanced Graph Data Model

### 2.1 Extend Graph Query (`queries.ts`)

```typescript
// Update getInitialGraphData() to include:
- Law nodes (with status-based colors)
- Party nodes (clustering centers)
- Committee nodes
- Lobbyist nodes
- Enhanced edges with:
  - AUTHORED (senator → law)
  - MEMBER_OF (senator → committee)
  - BELONGS_TO (senator → party)
  - LOBBY (lobbyist → senator)
  - VOTED_SAME (senator → senator with agreement %)
```

### 2.2 Update Types

- Add optional properties to GraphNode:
  - `status` for laws
  - `ideology` for parties
  - `type` for lobbyists (company, union, ngo, professional_college)
- Add edge strength indicators

## Phase 3: Cytoscape Graph Enhancements

### 3.1 Enhanced Node Styling (`CytoscapeGraph.svelte`)

- **Senators:** Circular nodes (45px) with:
  - Party color background
  - White border with glow effect on hover
  - Photo display on hover (custom tooltip)
- **Laws:** Rectangular nodes (50x35px) with:
  - Status colors:
    - Approved: Green gradient (#10b981 → #34d399)
    - Rejected: Red gradient (#ef4444 → #f87171)
    - In Discussion: Blue gradient (#3b82f6 → #60a5fa)
    - Withdrawn: Gray gradient (#6b7280 → #9ca3af)
- **Parties:** Large diamond/star shapes (60px) with:
  - Party color
  - Glow effect indicating cluster center
- **Committees:** Hexagonal nodes (40px) with:
  - Purple gradient
  - Member count badge
- **Lobbyists:** Small circular nodes (30px) with:
  - Type-based colors:
    - Company: Orange
    - Union: Yellow
    - NGO: Teal
    - Professional College: Indigo

### 3.2 Enhanced Edge Styling

- **AUTHORED:** Solid blue line with arrow (2px)
- **MEMBER_OF:** Dashed purple line (1.5px)
- **BELONGS_TO:** Thin gray line to party center (1px)
- **LOBBY:** Orange dotted line with warning icon
- **VOTED_SAME:**
  - Width: 1-4px based on agreement (0.5-1.0)
  - Color: Gradient based on agreement strength
  - Opacity: 0.3-0.7
  - Add agreement label on hover

### 3.3 Interactive Features

- Click on node to show details panel (slide-in from right)
- Hover to highlight connected nodes and dim others
- Double-click to expand/collapse clusters
- Drag and drop with physics
- Smooth layout animations

## Phase 4: New Graph UI Components

### 4.1 Graph Legend Panel (`GraphLegend.svelte`)

- Floating panel with draggable position
- Toggle visibility
- Legend items for all node/edge types
- Color indicators with labels
- Entity count badges

### 4.2 Node Details Panel (`NodeDetailsPanel.svelte`)

- Slide-in panel from right side
- Shows detailed info based on node type:
  - **Senator:** Photo, party, region, committees, authored laws, voting patterns
  - **Law:** Boletin, title, status, topic, authors, description
  - **Committee:** Name, members list, related laws
  - **Party:** Ideology, members count, vote distribution
  - **Lobbyist:** Name, type, industry, connected senators
- Smooth animation with backdrop blur
- Close button and keyboard support (Escape)

### 4.3 Enhanced Filter Panel (`FilterPanel.svelte`)

- Add entity type toggles:
  - [x] Senators
  - [x] Laws
  - [x] Committees
  - [x] Lobbyists
  - [x] Party clusters
- Status filter for laws
- Agreement strength slider for voting edges
- Lobbyist type filter
- Apply/Reset buttons with animation

### 4.4 Enhanced Graph Controls (`GraphControls.svelte`)

- Update styling with vibrant gradient buttons
- Add new controls:
  - Toggle entity types
  - Auto-rotate on/off
  - Show/hide labels
  - Reset zoom & layout
- Add tooltips with animations

## Phase 5: Page Improvements

### 5.1 Home Page Dashboard (`+page.svelte`)

- Replace generic hero with stats cards grid:
  ```
  ┌─────────────┬─────────────┬─────────────┬─────────────┐
  │   43 Sen.   │    4 Parties │   12 Laws    │   8 Comms   │
  │   (breakdown)│ (distribution)│  (by status) │   (total)   │
  └─────────────┴─────────────┴─────────────┴─────────────┘
  ```
- Add animated counters (0 → target)
- Add gradient backgrounds to cards
- Enhanced search bar with glassmorphism

### 5.2 Update Senator Detail Page (`senador/[id]/+page.svelte`)

- Add mini graph showing senator's connections
- Show voting pattern visualization
- Add party-colored accents
- Add animated transitions

### 5.3 Add About/Stats Page (`sobre/+page.svelte`)

- Project description
- Data sources
- Methodology
- Interactive stats dashboard

## Phase 6: Polish & Animations

### 6.1 Add Global Animations

- Page transitions (fade-in)
- Card hover effects (scale, lift, glow)
- Graph load animation
- Number counter animations
- Skeleton loaders for data

### 6.2 Accessibility Improvements

- Keyboard navigation for graph
- ARIA labels for interactive elements
- Focus indicators
- Screen reader support

### 6.3 Responsive Design

- Mobile-optimized graph controls
- Collapsible panels on small screens
- Touch gestures for graph interaction

## Implementation Order:

1. Theme setup (Tailwind config, colors, animations)
2. Dashboard hero (stats cards, layout)
3. Data model updates (queries, types)
4. Graph styling (Cytoscape node/edge styles)
5. New components (Legend, Details Panel, Enhanced Filters)
6. Page updates (Home, Senator details)
7. Animations & polish
