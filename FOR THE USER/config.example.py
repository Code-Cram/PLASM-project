# PLASM Configuration Template
# Copy this file to 'config.py' and add your API keys

# API Keys (get your own from the respective platforms)
TMDB_API_KEY = "your_tmdb_api_key_here"  # Get from: https://www.themoviedb.org/settings/api
GOOGLE_BOOKS_API_KEY = "your_google_books_key_here"  # Get from: https://console.cloud.google.com/apis/credentials
# Jikan API is public - no key needed

# Database configuration
DB_PATH = "plasm.db"

# Directory paths
POSTERS_DIR = "data/posters/"
EXPORTS_DIR = "data/exports/"
LOGS_DIR = "data/logs/"

# Content type definitions
CONTENT_TYPES = {
    "film": {"api": "tmdb", "label": "Film"},
    "series": {"api": "tmdb", "label": "Series"},
    "anime": {"api": "jikan", "label": "Anime"},
    "manga": {"api": "jikan", "label": "Manga"},
    "book": {"api": "googlebooks", "label": "Book"}
}

# Analytic review weights (by content type)
ANALYTIC_WEIGHTS = {
    "film": {
        "direction": 0.20,
        "writing": 0.20,
        "acting": 0.15,
        "technical": 0.15,
        "emotional_impact": 0.30
    },
    "series": {
        "direction": 0.15,
        "writing": 0.25,
        "acting": 0.15,
        "pacing": 0.15,
        "emotional_impact": 0.30
    },
    "anime": {
        "animation": 0.20,
        "writing": 0.25,
        "characters": 0.20,
        "soundtrack": 0.15,
        "emotional_impact": 0.20
    },
    "manga": {
        "art": 0.25,
        "writing": 0.30,
        "characters": 0.20,
        "pacing": 0.25
    },
    "book": {
        "writing": 0.35,
        "plot": 0.25,
        "characters": 0.20,
        "emotional_impact": 0.20
    }
}

# API retry configuration
MAX_RETRIES = 3
RETRY_TIMEOUT = 5  # seconds
BACKOFF_FACTOR = 1.5

# Default values
DEFAULT_STATUS = "visto"
DEFAULT_WATCH_CONTEXT = "home"
