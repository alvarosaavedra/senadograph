#!/bin/bash

echo "=== Setting up Neo4j for SenadoGraph ==="

# Check if Docker is running
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running. Starting Docker..."
    sudo systemctl start docker
    sleep 2
fi

# Check if container already exists
if docker ps -a | grep -q neo4j-senado; then
    echo "🔄 Neo4j container exists. Starting it..."
    docker start neo4j-senado
else
    echo "🚀 Creating Neo4j container (this may take a few minutes)..."
    docker run \
        --name neo4j-senado \
        -p 7474:7474 \
        -p 7687:7687 \
        -e NEO4J_AUTH=neo4j/password \
        -d neo4j:latest
fi

# Wait for Neo4j to be ready
echo "⏳ Waiting for Neo4j to start (about 30 seconds)..."
sleep 30

# Check if running
if docker ps | grep -q neo4j-senado; then
    echo "✅ Neo4j is running!"
    echo ""
    echo "📊 Neo4j Browser: http://localhost:7474"
    echo "   Username: neo4j"
    echo "   Password: password"
    echo ""
    echo "🔌 Bolt URI: bolt://localhost:7687"
else
    echo "❌ Neo4j failed to start. Check logs: docker logs neo4j-senado"
    exit 1
fi
