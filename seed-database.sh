#!/bin/bash

echo "=== Seeding Neo4j Database ==="

cd /home/radbug/Work/relations/senado-graph/scraper

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating Python virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install neo4j python-dotenv -q

# Run seed script
echo "🌱 Seeding database with mock data..."
python seed_neo4j.py

echo ""
echo "✅ Done! Database is ready."
echo "   You can now run: cd /home/radbug/Work/relations/senado-graph && npm run dev"
