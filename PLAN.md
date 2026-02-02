# SenadoGraph - Chilean Senate Relationship Visualization

## Project Overview

A modern web application to visualize relationships between Chilean senators, including party affiliations, law authorship, voting patterns, and lobby meetings. Built with SvelteKit, Neo4j, and Cytoscape.js.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Vercel (SvelteKit)                       │
├─────────────────────────────────────────────────────────────┤
│  Server-Side (+page.server.ts)                              │
│  ├─ Initial data load (Neo4j Aura)                          │
│  ├─ Detail pages (senators, laws)                           │
│  └─ Pre-rendered at build time                              │
│                                                             │
│  Client-Side (browser)                                      │
│  ├─ Cytoscape.js graph (force-directed)                     │
│  ├─ Filter changes → fetch /api/graph                       │
│  ├─ Search autocomplete                                     │
│  └─ Graph interactions (click, drag, zoom)                  │
└─────────────────────────────────────────────────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │   Neo4j Aura DB  │
                    │  (Graph Database)│
                    └──────────────────┘
```

---

## Technology Stack

| Component | Technology |
|-----------|-----------|
| **Frontend Framework** | SvelteKit + TypeScript |
| **Styling** | Tailwind CSS |
| **Graph Visualization** | Cytoscape.js (cose layout) |
| **Database** | Neo4j Aura (Cloud) |
| **i18n** | svelte-i18n (Spanish/English) |
| **Data Scraping** | Python (BeautifulSoup) |
| **Deployment** | Vercel |

---

## Database Schema (Neo4j)

### Nodes

```cypher
(:Senator {
  id: "senator_123",
  name: "Name",
  nameEn: "English Name",
  party: "Party",
  region: "Region",
  regionEn: "Region EN",
  email: "email",
  photoUrl: "url",
  biography: "text",
  biographyEn: "text",
  startDate: "2022-03-11",
  active: true
})

(:Party {
  id: "party_rn",
  name: "Renovación Nacional",
  nameEn: "National Renewal",
  shortName: "RN",
  color: "#0054a6",
  ideology: "center-right"
})

(:Law {
  id: "law_12345",
  boletin: "12345-06",
  title: "Title ES",
  titleEn: "Title EN",
  description: "Description ES",
  descriptionEn: "Description EN",
  dateProposed: "2023-01-15",
  status: "in_discussion",  // approved, rejected, in_discussion, withdrawn
  topic: "education"
})

(:Vote {
  id: "vote_session_123",
  date: "2023-06-15",
  session: "123",
  result: "approved"
})

(:Committee {
  id: "committee_education",
  name: "Educación",
  nameEn: "Education"
})

(:Lobbyist {
  id: "lobby_company_123",
  name: "Company Name",
  type: "company",  // company, union, ngo, professional_college
  industry: "mining",
  industryEn: "mining"
})
```

### Relationships

```cypher
(:Senator)-[:BELONGS_TO]->(:Party)
(:Senator)-[:MEMBER_OF {role: "president"}]->(:Committee)
(:Senator)-[:AUTHORED {role: "principal", date: "2023-01-15"}]->(:Law)
(:Senator)-[:CO_SPONSORED]->(:Law)
(:Senator)-[:VOTED {vote: "favor", date: "2023-06-15"}]->(:Vote)-[:ON]->(:Law)
(:Senator)-[:MET_WITH {date: "2023-05-10", topic: "mining bill"}]->(:Lobbyist)
(:Senator)-[:VOTED_SAME {agreement: 0.85}]->(:Senator)
(:Senator)-[:CO_SPONSORED_WITH]->(:Senator)
```

---

## Project Structure

```
senate-relations/
├── src/
│   ├── lib/
│   │   ├── components/
│   │   │   ├── graph/
│   │   │   │   ├── CytoscapeGraph.svelte      # Force-directed graph
│   │   │   │   ├── GraphControls.svelte       # Zoom, filters, layout
│   │   │   │   └── NodeTooltip.svelte         # Hover details
│   │   │   ├── ui/
│   │   │   │   ├── SenatorCard.svelte         # Detail panels
│   │   │   │   ├── LawCard.svelte
│   │   │   │   ├── FilterPanel.svelte         # Filter UI
│   │   │   │   ├── SearchBar.svelte           # Autocomplete
│   │   │   │   └── LanguageToggle.svelte      # ES/EN switch
│   │   │   └── layout/
│   │   │       ├── Header.svelte
│   │   │       └── Footer.svelte
│   │   ├── database/
│   │   │   ├── neo4j.ts                       # Driver config
│   │   │   └── queries.ts                     # Cypher queries
│   │   ├── i18n/
│   │   │   ├── index.ts                       # svelte-i18n setup
│   │   │   ├── es.json                        # Spanish
│   │   │   └── en.json                        # English
│   │   ├── types/
│   │   │   └── index.ts                       # TypeScript types
│   │   └── utils/
│   │       └── graphData.ts                   # Data transformation
│   ├── routes/
│   │   ├── +layout.svelte                     # Root layout
│   │   ├── +layout.server.ts                  # Load parties, committees
│   │   ├── +page.server.ts                    # Home: Initial graph data
│   │   ├── +page.svelte                       # Home: Graph view
│   │   ├── api/
│   │   │   └── graph/+server.ts               # POST: Dynamic graph queries
│   │   ├── senador/
│   │   │   ├── [id]/+page.server.ts           # Load senator (prerendered)
│   │   │   └── [id]/+page.svelte
│   │   ├── ley/
│   │   │   ├── [id]/+page.server.ts           # Load law (prerendered)
│   │   │   └── [id]/+page.svelte
│   │   ├── partido/
│   │   │   ├── [id]/+page.server.ts
│   │   │   └── [id]/+page.svelte
│   │   └── sobre/
│   │       └── +page.svelte                   # About page
│   └── app.html
├── scraper/                                   # Python scraper
│   ├── config.py
│   ├── models.py
│   ├── spider.py
│   ├── seed_neo4j.py
│   ├── update_neo4j.py
│   └── requirements.txt
├── neo4j/
│   ├── schema.cypher                          # Constraints & indexes
│   └── seed_data.cypher                       # Initial data
├── static/
│   └── images/senators/                       # Cached photos
└── [config files]
```

---

## Data Flow

### Initial Page Load (Server-Side)

```typescript
// +page.server.ts
export async function load() {
  const initialData = await getInitialGraphData();
  return { initialData };
}
```

### Dynamic Updates (Client-Side)

```svelte
<script>
  async function applyFilters(filters) {
    const res = await fetch('/api/graph', {
      method: 'POST',
      body: JSON.stringify(filters)
    });
    graphData = await res.json();
  }
</script>
```

---

## API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/graph` | POST | Dynamic graph data based on filters |

---

## Implementation Phases

### Phase 1: Foundation (Week 1)

- [ ] Create SvelteKit project (TypeScript, Tailwind)
- [ ] Setup i18n (Spanish/English)
- [ ] Configure Neo4j Aura
- [ ] Create database schema
- [ ] Build scraper for senator data
- [ ] Seed Neo4j with initial data

### Phase 2: Server-Side Pages (Week 2)

- [ ] +layout.server.ts (common data)
- [ ] Home page (+page.server.ts + +page.svelte)
- [ ] Senator detail page (prerendered)
- [ ] Law detail page (prerendered)
- [ ] Neo4j queries module

### Phase 3: Graph Visualization (Week 3)

- [ ] Integrate Cytoscape.js
- [ ] Implement force-directed layout (cose)
- [ ] Node/edge styling
  - Senators: Circles, size = activity, color = party
  - Laws: Squares, size = # sponsors, color = status
- [ ] Graph interaction handlers
- [ ] /api/graph endpoint for dynamic updates

### Phase 4: Client Features (Week 4)

- [ ] Filter panel (client-side state)
- [ ] Search autocomplete
- [ ] Detail panels (SenatorCard, LawCard)
- [ ] Language toggle
- [ ] Data disclaimer

### Phase 5: Polish (Week 5)

- [ ] Responsive design
- [ ] Loading states
- [ ] Error handling
- [ ] Performance optimization
- [ ] Testing

### Phase 6: Deployment (Week 6)

- [ ] Vercel deployment
- [ ] Environment variables
- [ ] Automated data updates (GitHub Actions)
- [ ] Documentation

---

## Environment Variables

```bash
# Neo4j Aura (server-side only)
NEO4J_URI=neo4j+s://xxxx.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password

# App config
PUBLIC_APP_URL=https://senadograph.vercel.app
PUBLIC_DEFAULT_LANG=es
```

---

## Features

### Core Features

1. **Force-Directed Graph View**
   - Senators as nodes (colored by party, sized by activity)
   - Laws as nodes (colored by status, sized by sponsors)
   - Edges show relationships (authorship, voting, co-sponsorship)
   - Interactive: click, drag, zoom, filter

2. **Senator Profiles**
   - Photo, contact info, biography
   - Authored laws
   - Committee memberships
   - Voting history
   - Lobby meetings
   - Related senators (voting patterns)

3. **Law Details**
   - Title, description, status
   - Authors and co-sponsors
   - Voting breakdown
   - Related laws

4. **Advanced Filtering**
   - Party selection
   - Committee filter
   - Date range
   - Law topic
   - Relationship type toggles

5. **Search**
   - Autocomplete for senators, laws, parties
   - Quick navigation

6. **Bilingual Support**
   - Spanish (default) and English
   - URL-based language switching
   - Persistent preference

---

## Data Sources

- **senado.cl** - Official Chilean Senate website
  - Senator list and details
  - Legislative projects
  - Voting records
  - Lobby registry
  - Committee information

---

## Technical Decisions

### Why SvelteKit?

- Excellent performance (smaller bundles)
- Server-side rendering out of the box
- TypeScript support
- Simple, clean syntax

### Why Neo4j?

- Purpose-built for graph relationships
- Native Cypher query language
- Excellent for complex network analysis
- Cloud offering (Neo4j Aura) with free tier

### Why Cytoscape.js?

- Built for graph visualization
- Force-directed layouts (cose)
- Good performance for medium-sized graphs
- Easy Svelte integration

### Minimal API Approach

- Most data loaded server-side (+page.server.ts)
- Only 1 API endpoint for dynamic graph updates
- Pre-rendered detail pages for SEO and performance

---

## Future Extensions

- [ ] Historical senate periods (2014, 2022, etc.)
- [ ] Chamber of Deputies integration
- [ ] Advanced analytics (influence metrics, clustering)
- [ ] Export to PNG/PDF
- [ ] Mobile app
- [ ] Real-time updates (WebSocket)

---

## Disclaimer

**Data Source**: This project uses publicly available data from [senado.cl](https://www.senado.cl). All information is sourced from official Chilean government transparency portals. Data accuracy depends on the official sources and is updated periodically.

---

## License

MIT License - Open source project for political transparency.

---

*Last Updated: February 2026*
