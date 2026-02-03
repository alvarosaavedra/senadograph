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
SENATORS_URL = f"{BASE_URL}/appsenado/index.php?mo=senadores&ac=listado"
LAWS_API_URL = "https://tramitacion.senado.cl/wspublico/tramitacion.php"
LAWS_URL = f"{BASE_URL}/appsenado/index.php?mo=tramitacion&ac=busquedaTramitacion"
LOBBY_URL = f"{BASE_URL}/appsenado/index.php?mo=lobby"
LOBBY_API_BASE = "https://tramitacion.senado.cl/appsenado/index.php"
LOBBY_LOBBYISTS_URL = f"{LOBBY_API_BASE}?mo=lobby&ac=GetLobistas"
LOBBY_TRIPS_URL = f"{LOBBY_API_BASE}?mo=lobby&ac=GetViajes"
LOBBY_DONATIONS_URL = f"{LOBBY_API_BASE}?mo=lobby&ac=GetDonativos"

# Request configuration
REQUEST_TIMEOUT = 30
REQUEST_DELAY = 1  # Delay between requests in seconds

# Retry configuration (exponential backoff)
MAX_RETRIES = 0
INITIAL_BACKOFF = 1.0  # Initial wait time in seconds
MAX_BACKOFF = 60.0  # Maximum wait time in seconds

# Data directories
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
IMAGES_DIR = os.path.join(
    os.path.dirname(__file__), "..", "static", "images", "senators"
)

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)
