"""Configuration for the scraper module."""

import os
from dotenv import load_dotenv

load_dotenv()

# Neo4j configuration
NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USERNAME = os.getenv("NEO4J_USERNAME", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

# Scraping configuration
BASE_URL = "https://www.senado.cl"
SENATORS_URL = f"{BASE_URL}/senadores"
LAWS_URL = f"{BASE_URL}/proyectos-ley"
LOBBY_URL = f"{BASE_URL}/lobby"

# Request configuration
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 1  # Delay between requests in seconds

# Data directories
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMAGES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "static", "images", "senators"
)

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
