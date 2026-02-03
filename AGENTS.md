# AGENTS.md - SenadoGraph Project Guidelines

## Build & Development Commands

```bash
# Development
npm run dev          # Start dev server with hot reload
npm run dev -- --open  # Start and open browser

# Build
npm run build        # Production build
npm run preview      # Preview production build locally

# Code Quality
npm run check        # TypeScript checking (svelte-check)
npm run lint         # ESLint check
npm run format       # Prettier format all files

# Testing
npm run test         # Run all tests
npm run test -- src/lib/components/SenatorCard.svelte  # Run single test file
npm run test -- --watch  # Watch mode
npm run test -- --ui     # UI mode for debugging

# Data Scraping (Python)
cd scraper && python spider.py           # Run scraper
cd scraper && python seed_neo4j.py      # Seed database
cd scraper && python -m pytest tests/    # Run scraper tests
```

## Code Style Guidelines

### Imports
- Group imports: external libs → internal modules → types
- Use `$lib/` alias for internal imports
- Import types with `type` keyword: `import type { Senator } from '$lib/types'`

### Formatting
- Use Prettier with default config
- 2 spaces indentation
- 80 character line limit
- Trailing commas in multi-line objects/arrays

### TypeScript Types
- Always define interfaces in `$lib/types/index.ts`
- Use strict typing, avoid `any`
- Props: `export let data: GraphData`
- Events: Use Svelte's `CustomEvent<PayloadType>`
- Server loads: Define return types in `+page.server.ts`

### Naming Conventions
- Components: PascalCase (`SenatorCard.svelte`)
- Functions/vars: camelCase (`getSenatorData`)
- Constants: UPPER_SNAKE_CASE (`MAX_NODES`)
- Files: kebab-case for non-components (`graph-data.ts`)
- Types/Interfaces: PascalCase (`interface SenatorData`)

### Error Handling
- Server-side: Use `try/finally` with Neo4j sessions
- Client-side: Use Svelte's `{#await}` with error slots
- Always close Neo4j sessions in `finally` blocks
- Log errors but don't expose to user (except safe messages)

### Component Structure
```svelte
<script lang="ts">
  // Types imports first
  import type { Senator } from '$lib/types';
  // Then regular imports
  import { onMount } from 'svelte';
  
  // Props with types
  export let senator: Senator;
  
  // Reactive statements
  $: fullName = `${senator.name} (${senator.party})`;
</script>

<!-- Single root element -->
<div class="card">
  <!-- Content -->
</div>

<style>
  /* Scoped styles only */
  .card {
    @apply bg-white rounded-lg shadow-md;
  }
</style>
```

### Neo4j Queries
- Place all queries in `$lib/database/queries.ts`
- Use parameterized queries (never string interpolation)
- Close sessions in `finally` blocks
- Return plain objects, not Neo4j records

### Server-Side Patterns
```typescript
// +page.server.ts
export const prerender = true; // For detail pages

export async function load({ params }) {
  const data = await getData(params.id);
  if (!data) {
    throw error(404, 'Not found');
  }
  return { data };
}
```

### Client-Side Fetching
- Use for: filter updates, search autocomplete
- Always debounce user input (300ms)
- Show loading states
- Handle errors gracefully

### i18n (Bilingual)
- Always wrap user-facing text: `{$_('key')}`
- Add translations to both `es.json` and `en.json`
- Use dot notation for nested keys: `'senator.name'`

### Graph Data Transformation
- Transform Neo4j data to Cytoscape format in `$lib/utils/graphData.ts`
- Keep graph state in component, not store (for performance)
- Use reactive statements for graph updates

### Tailwind Classes
- Use `@apply` in `<style>` blocks for component-specific styles
- Prefer utility classes directly in markup for simple cases
- Custom colors: use CSS variables from theme

### Environment Variables
- Server-only: `NEO4J_URI`, `NEO4J_PASSWORD`
- Public: `PUBLIC_*` prefix for browser access
- Never expose credentials to client

## Project-Specific Conventions

1. **Bilingual**: All UI text must support ES/EN
2. **Server-First**: Use `+page.server.ts` for initial data
3. **Pre-render**: Detail pages should be static
4. **Graph Updates**: Use `/api/graph` POST for dynamic filtering
5. **Data Disclaimer**: Include on every page with data
6. **Accessibility**: WCAG 2.1 AA compliance (alt text, keyboard nav)
7. **Performance**: Lazy load Cytoscape, optimize images

## Testing Guidelines

- Unit test utilities in `$lib/utils/`
- Component tests with Svelte Testing Library
- Mock Neo4j driver for tests
- Test both Spanish and English renders

## Common Patterns

```typescript
// Neo4j session pattern
const session = driver.session();
try {
  const result = await session.run(query, params);
  return result.records.map(r => r.toObject());
} finally {
  await session.close();
}

// Filter application
async function applyFilters() {
  loading = true;
  try {
    const res = await fetch('/api/graph', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(filters)
    });
    if (!res.ok) throw new Error('Failed to fetch');
    graphData = await res.json();
  } finally {
    loading = false;
  }
}
```

## Git Workflow & Commit Strategy

- **Commit after each phase** completion (as defined in PLAN.md)
- **Phase commit messages**:
  - `feat: Phase 1 - Foundation setup`
  - `feat: Phase 2 - Server-side pages and Neo4j queries`
  - `feat: Phase 3 - Graph visualization with Cytoscape.js`
  - `feat: Phase 4 - Client-side features and UI components`
  - `feat: Phase 5 - Polish, testing and optimization`
  - `feat: Phase 6 - Deployment and documentation`
- Write meaningful commit messages describing what was implemented
- Update PROGRESS.md after each phase

## Deployment Notes

- Vercel: Connect GitHub repo for auto-deploy
- Neo4j Aura: Use environment variables, not hardcoded
- Pre-render routes in `svelte.config.js` for static pages

## Browser Automation with agent-browser

Use `agent-browser` for web automation and testing. Run `agent-browser --help` for all commands.

### Installation
```bash
npm install -g agent-browser
agent-browser install  # Download Chromium (Linux: run `agent-browser install --with-deps` if issues)
```

### Core Workflow
1. `agent-browser open <url>` - Navigate to page
2. `agent-browser snapshot -i` - Get interactive elements with refs (@e1, @e2)
3. `agent-browser click @e1` / `fill @e2 "text"` - Interact using refs
4. Re-snapshot after page changes

### Key Commands
```bash
# Navigation
agent-browser open example.com              # Navigate
agent-browser back / forward / reload        # Navigation controls

# Interaction
agent-browser click <sel>                   # Click by ref or selector
agent-browser fill <sel> "text"             # Fill input
agent-browser type <sel> "text"             # Type into element
agent-browser press Enter                   # Press key

# Get Info
agent-browser snapshot                      # Accessibility tree with refs
agent-browser get text <sel>                # Get text content
agent-browser get html <sel>                # Get innerHTML
agent-browser get url                       # Current URL

# Actions
agent-browser screenshot page.png           # Take screenshot
agent-browser pdf output.pdf                # Save as PDF
agent-browser wait <sel>                    # Wait for element
agent-browser close                         # Close browser
```

### Options
- `--session <name>` - Isolated browser sessions
- `--profile <path>` - Persistent browser profile for cookies/storage
- `--headers <json>` - Set HTTP headers for authentication
- `--json` - Machine-readable output for agents
- `--headed` - Show browser window (vs headless)

### Sessions & Profiles
```bash
# Multiple isolated sessions
agent-browser --session agent1 open site-a.com
agent-browser --session agent2 open site-b.com

# Persistent profile (cookies, localStorage, login sessions)
agent-browser --profile ~/.myapp-profile open myapp.com
```

### For AI Agents
Use `--json` flag for programmatic interaction:
```bash
agent-browser snapshot --json      # Returns JSON with refs
agent-browser get text @e1 --json  # Returns structured data
```
