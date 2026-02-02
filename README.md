# SenadoGraph 🇨🇱

A modern web application to visualize and explore the relationships between Chilean senators, their legislative activities, party affiliations, and connections with lobbyists.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![SvelteKit](https://img.shields.io/badge/SvelteKit-4.0-orange.svg)
![Neo4j](https://img.shields.io/badge/Neo4j-Graph%20Database-brightgreen.svg)

## 🌟 Features

- **Interactive Force-Directed Graph**: Visualize senators, laws, parties, and their relationships
- **Senator Profiles**: Detailed information including authored laws, voting history, committee memberships
- **Law Explorer**: Track legislative projects, sponsors, and voting patterns
- **Lobby Transparency**: View meetings between senators and interest groups
- **Bilingual Support**: Full Spanish and English interface
- **Real-time Filtering**: Dynamic graph updates without page reloads
- **Mobile Responsive**: Optimized for all devices

## 🏛️ Data Sources

All data is sourced from official Chilean government transparency portals:
- [Senado.cl](https://www.senado.cl) - Official Senate website
- Legislative project database
- Lobby registry (Ley 20.730)
- Voting records and committee information

## 🚀 Tech Stack

- **Frontend**: [SvelteKit](https://kit.svelte.dev/) + TypeScript + Tailwind CSS
- **Visualization**: [Cytoscape.js](https://js.cytoscape.org/) (force-directed graph layout)
- **Database**: [Neo4j Aura](https://neo4j.com/cloud/aura/) (cloud graph database)
- **i18n**: svelte-i18n (bilingual ES/EN)
- **Deployment**: [Vercel](https://vercel.com)

## 🛠️ Development Setup

### Prerequisites

- Node.js 18+
- npm or pnpm
- Python 3.8+ (for data scraper)
- Neo4j Aura account (free tier available)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/senadograph.git
cd senadograph

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your Neo4j credentials

# Seed the database with initial data
cd scraper
pip install -r requirements.txt
python seed_neo4j.py

# Start development server
cd ..
npm run dev
```

### Environment Variables

Create a `.env` file in the root directory:

```bash
# Neo4j Aura (server-side only)
NEO4J_URI=neo4j+s://your-instance-id.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password-here

# App Configuration
PUBLIC_APP_URL=http://localhost:5173
PUBLIC_DEFAULT_LANG=es
```

## 📖 Available Scripts

```bash
# Development
npm run dev              # Start dev server
npm run dev -- --open    # Start and open browser

# Build
npm run build            # Production build
npm run preview          # Preview production build

# Code Quality
npm run check            # TypeScript checking (svelte-check)
npm run lint             # ESLint check
npm run format           # Prettier format all files

# Testing
npm run test             # Run all tests
npm run test -- --watch  # Watch mode
npm run test -- --ui     # UI mode for debugging

# Data Scraping
python scraper/spider.py          # Run scraper
python scraper/seed_neo4j.py      # Seed database
python scraper/update_neo4j.py    # Incremental updates
```

## 🗺️ Project Structure

```
senate-relations/
├── src/
│   ├── lib/
│   │   ├── components/        # Svelte components
│   │   │   ├── graph/         # Graph visualization
│   │   │   ├── ui/            # UI components
│   │   │   └── layout/        # Layout components
│   │   ├── database/          # Neo4j connection & queries
│   │   ├── i18n/              # Translations (es/en)
│   │   ├── types/             # TypeScript types
│   │   └── utils/             # Utility functions
│   └── routes/                # SvelteKit routes
├── scraper/                   # Python data scraper
├── neo4j/                     # Database schema
└── static/                    # Static assets
```

## 🌐 Deployment

### Vercel (Recommended)

1. Connect your GitHub repository to Vercel
2. Add environment variables in Vercel dashboard
3. Deploy automatically on every push to main

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

### Neo4j Aura

1. Create a free account at [neo4j.com/aura](https://neo4j.com/aura/)
2. Create a new database instance
3. Copy the connection URI and credentials to your `.env` file

## 📊 Graph Schema

The application uses Neo4j graph database with the following structure:

**Nodes:**
- `Senator` - Chilean senators with party, region, contact info
- `Party` - Political parties with colors and ideology
- `Law` - Legislative projects with status and topics
- `Committee` - Senate committees
- `Lobbyist` - Companies and organizations

**Relationships:**
- `BELONGS_TO` - Senator → Party
- `MEMBER_OF` - Senator → Committee
- `AUTHORED` - Senator → Law
- `VOTED` - Senator → Vote → Law
- `MET_WITH` - Senator → Lobbyist

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This project uses publicly available data from official Chilean government sources. Data accuracy depends on the source websites and is updated periodically. This is an independent project for transparency and educational purposes.

## 🙏 Acknowledgments

- Data sourced from [Senado de Chile](https://www.senado.cl)
- Built with [SvelteKit](https://kit.svelte.dev) and [Neo4j](https://neo4j.com)
- Graph visualization powered by [Cytoscape.js](https://js.cytoscape.org)

---

**Made with ❤️ for political transparency in Chile**
