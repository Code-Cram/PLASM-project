# PLASM

**Personal Library and Streaming Manager**

**Marc Martínez Arias**

- GitHub: [@Code-Cram](https://github.com/Code-Cram)
- Project: [PLASM-project](https://github.com/Code-Cram/PLASM-project)

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**TL;DR:** You can use, modify, and distribute this software freely, even commercially, as long as you include the original copyright and license notice.


![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Status](https://img.shields.io/badge/status-in%20development-yellow.svg)
![PostgreSQL](https://img.shields.io/badge/database-PostgreSQL-336791.svg)

---

PLASM was born from the idea of merging **IMDb, Goodreads, Letterboxd, MyAnimeList** and similar apps into one unified platform. The main problem with existing services is the fragmentation: you need different apps for different content types, each with their own limitations, data silos, and lack of customization.

PLASM (Películas,libros,anime,series,manga) is made by me to be a open-source space where you can:Comment, judge, and review **all types of content** (films, series, anime, manga, books). Use your **own rating system** (analytic multi-dimensional or quick subjective). **Own your data** completely (local PostgreSQL + JSON exports). And customize everything to your preferences

---

## Key Features

### Phase 1 (Current - CLI Application)

**Multi-Content Support**
- Films, Series, Anime, Manga, Books - all in one database

**Dual Rating System**
- **Analytic Mode**: Rate across multiple dimensions with custom weights
  - Films: Direction, Writing, Acting, Technical, Emotional Impact
  - Series: Direction, Writing, Acting, Pacing, Emotional Impact
  - Anime: Animation, Writing, Characters, Soundtrack, Emotional Impact
  - Manga: Art, Writing, Characters, Pacing
  - Books: Writing, Plot, Characters, Emotional Impact
- **Subjective Mode**: Quick 0-10 overall rating

**Automatic Metadata Enrichment**
- Fetch posters, ratings, cast, crew from APIs
- TMDb (films/series), Jikan (anime/manga), Google Books (books)

**Local-First Architecture**
- PostgreSQL database: Your data stays on your machine
- JSON exports: Portable backups prevent vendor lock-in
- No cloud dependency (optional sync in future phases)

**Rich Review Features**
- Free-form text reviews
- Rewatch/re-read tracking
- Consumption context (cinema/home/streaming)
- Status tracking (completed/in-progress/pending/dropped)

### Phase 2+ in a future

Streamlit dashboard with analytics and visualizations  
Batch imports from Letterboxd, Goodreads, MyAnimeList  
Web interface with FastAPI backend  
Mobile app  
ML-powered recommendations  

---

## System Architecture

```
┌─────────────────────────────────────────────────────┐
│              CLI Interface (Phase 1)                │
│         Streamlit Dashboard (Phase 2+)              │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                 Python Backend                      │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐   │
│  │ API        │  │ Content    │  │ Data Fusion  │   │
│  │ Manager    │→ │ Handler    │→ │ & Validation │   │
│  │ (TMDb,     │  │ (User      │  │              │   │
│  │ Jikan,     │  │ Input)     │  │              │   │
│  │ Google     │  │            │  │              │   │
│  │ Books)     │  │            │  │              │   │
│  └────────────┘  └────────────┘  └──────────────┘   │
│           │              │               │          │
│  ┌────────▼──────────────▼───────────────▼───────┐  │
│  │   Preprocessing & Normalization               │  │
│  │   (Unified schema across all content types)   │  │
│  └────────────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────────┘
                        │
┌───────────────────────▼─────────────────────────────┐
│                 Storage Layer                       │
│  ┌──────────────────┐      ┌──────────────────┐    │
│  │   PostgreSQL     │  +   │   JSON Exports   │    │
│  │   Database       │      │   (Backups)      │    │
│  └──────────────────┘      └──────────────────┘    │
└─────────────────────────────────────────────────────┘
```

**15-Stage Workflow:**  
User Input → API Search → Selection → API Fetch → Preprocessing → Display → Review Type Choice → Ratings Capture → Common Data → Merge → Validation → SQL Save → JSON Export → Success → Confirmation

**See [docs/PLASM_workflow.md](docs/PLASM_workflow.md) for complete stage-by-stage documentation.**

---

### Core Technologies

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Language** | Python | 3.9+ | Backend logic |
| **Database** | PostgreSQL | 12+ | Primary data storage |
| **HTTP Client** | requests | 2.28+ | API calls |
| **CLI** | Python `input()` | Built-in | Phase 1 interface |

### External APIs

- **TMDb API**: Films & series metadata
- **Jikan API v4**: Anime & manga data (MyAnimeList unofficial API)
- **Google Books API**: Book metadata

### Future Stack (Phase 2+)

- **pandas**: Data analysis
- **Streamlit**: Interactive dashboard
- **Plotly**: Visualizations
- **FastAPI**: REST API (Phase 3)
- **React**: Web frontend (Phase 4)

---

##  Installation

### Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **PostgreSQL 12+** ([Download](https://www.postgresql.org/download/))
- **Git** ([Download](https://git-scm.com/downloads))
- **pip** (comes with Python)

### Step 1: Clone the Repository

```bash
git clone https://github.com/Code-Cram/PLASM-project.git
cd PLASM-project
```

### Step 2: Set Up PostgreSQL Database

**Option A: Using psql (Command Line)**

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database and user
CREATE DATABASE plasm_db;
CREATE USER plasm_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE plasm_db TO plasm_user;
\q
```

**Option B: Using pgAdmin (GUI)**

1. Open pgAdmin
2. Right-click "Databases" → Create → Database
3. Name: `plasm_db`
4. Right-click "Login/Group Roles" → Create → Login/Group Role
5. Name: `plasm_user`, set password

### Step 3: Python Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `requests` - HTTP client for API calls
- `psycopg2-binary` - PostgreSQL adapter

### Step 5: Configure API Keys

```bash
# Copy the example config
cp config.example.py config.py

# Edit config.py with your favorite editor
nano config.py  # or vim, code, etc.
```

**Add your API keys:**

```python
TMDB_API_KEY = "your_actual_tmdb_key"
GOOGLE_BOOKS_API_KEY = "your_actual_google_books_key"

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "plasm_db"
DB_USER = "plasm_user"
DB_PASSWORD = "your_secure_password"
```

**Get API keys:**
- **TMDb**: https://www.themoviedb.org/settings/api (free, requires account)
- **Google Books**: https://console.cloud.google.com/apis/credentials (free, requires Google Cloud project)
- **Jikan**: No key needed (public API)

### Step 6: Initialize Database

```bash
# Run database setup script
python setup_database.py
```

This creates the necessary tables and schema.

### Step 7: Run PLASM

```bash
python main.py
```

**You're ready to start reviewing content!**
We are working to gave to you a personal database with your reviews.
---

## Usage Guide

### Basic Workflow

1. **Launch the app:**
   ```bash
   python main.py
   ```

2. **Main menu:**
   ```
   ===== PLASM - Personal Library and Streaming Manager =====
   1. Add new review
   2. View my reviews
   3. Search database
   4. Export to JSON
   5. Exit
   ```

3. **Add a review:**
   - Select content type (Film/Series/Anime/Manga/Book)
   - Search by title (e.g., "The Matrix")
   - Choose from results
   - Confirm metadata (title, year, director/author, etc.)

4. **Choose rating type:**
   - **Analytic**: Multi-dimensional rating (~3 min)
   - **Subjective**: Quick overall score (~10 sec)

5. **Rate the content:**

   **Example - Analytic rating for a film:**
   ```
   Direction (20% weight): 9/10
   Writing (20% weight): 8/10
   Acting (15% weight): 9/10
   Technical (15% weight): 10/10
   Emotional Impact (30% weight): 9/10
   
   → Final Score: 9.05/10 (auto-calculated)
   ```

6. **Add optional details:**
   - Review text (your thoughts)
   - Would you rewatch? (y/n)
   - Context (cinema/home/streaming)
   - Status (completed/in-progress/pending/dropped)

7. **Save:** Review stored in PostgreSQL + JSON export created

### Example Output

```json
{
  "content_type": "film",
  "source_api": "tmdb",
  "api_id": "tmdb_603",
  "title": "The Matrix",
  "year": 1999,
  "director": "Lana Wachowski, Lilly Wachowski",
  "runtime": 136,
  "genres": ["Action", "Science Fiction"],
  "api_rating": 8.7,
  "review_type": "analytic",
  "analytic_ratings": {
    "direction": 9,
    "writing": 8,
    "acting": 9,
    "technical": 10,
    "emotional_impact": 9,
    "final_score": 9.05
  },
  "review_text": "Revolutionary sci-fi...",
  "would_rewatch": true,
  "watch_context": "cinema",
  "status": "completed",
  "date_added": "2026-02-01T19:30:00"
}
```

---

## Project Structure

```
PLASM-project/
│
├── README.md                      # You are here
├── LICENSE                        # MIT License
├── CHANGELOG.md                   # Version history
├── requirements.txt               # Python dependencies
├── .gitignore                     # Files to ignore in Git
├── config.example.py              # Configuration template
├── config.py                      # Your config (not in Git)
│
├── docs/                          # Complete documentation
│   ├── PLASM_project_idea.md         # Concept and vision
│   ├── PLASM_architecture.md         # Technical architecture
│   ├── PLASM_workflow.md             # 15-stage workflow details
│   └── files_structure.md            # Module responsibilities
│
├── src/                           # Python source code
│   ├── main.py                       # Entry point
│   ├── content_handler.py            # User interaction logic
│   ├── api_manager.py                # API integration
│   ├── data_fusion.py                # Data consolidation
│   │
│   ├── preprocessing/                # API response normalization
│   │   ├── __init__.py
│   │   ├── tmdb_preprocessor.py
│   │   ├── jikan_preprocessor.py
│   │   └── googlebooks_preprocessor.py
│   │
│   ├── storage/                      # Database & exports
│   │   ├── __init__.py
│   │   ├── postgres_handler.py
│   │   └── json_handler.py
│   │
│   └── utils/                        # Helper utilities
│       ├── __init__.py
│       ├── validators.py
│       └── formatters.py
│
└── data/                          # Generated data (ignored by Git)
    ├── posters/                      # Downloaded posters
    ├── exports/                      # JSON backups
    └── logs/                         # Application logs
```

### File Descriptions

- main.py - Application entry point, orchestrates workflow (In Progress).
- content_handler.py - Handles user input, CLI interaction, menu system (In Progress). 
- api_manager.py - Manages API calls to TMDb, Jikan, Google Books (In Progress). 
- data_fusion.py - Merges API data with user reviews, validates (In Progress). 
- preprocessing/ - Normalizes different API responses to unified schema (In Progress). 
- storage/postgres_handler.py - PostgreSQL CRUD operations (In Progress). storage/
- json_handler.py - JSON export/backup functionality (In Progress). utils/
- validators.py - Input validation (ratings 0-10, dates, etc.) (In Progress). utils/
- formatters.py - Display formatting for CLI output (In Progress). 

---

## Development Roadmap

### Phase 0: Planning (Completed - Jan 2026)
- [x] Project concept finalized
- [x] Architecture designed
- [x] Workflow documented (15 stages)
- [x] Database schema planned
- [x] GitHub repository created
- [x] Documentation written

### Phase 1: Core Functionality (Current)
**Goal:** Functional CLI application

- [x] Architecture design
- [x] Documentation complete
- [ ] Python modules implemented
- [ ] API integration (TMDb, Jikan, Google Books)
- [ ] PostgreSQL schema created
- [ ] CLI interface working
- [ ] Complete review workflow functional
- [ ] JSON export system
- [ ] Unit testing

**Completion Criteria:** User can add a complete review via terminal with automatic API enrichment and dual persistence (PostgreSQL + JSON).

---

###  Phase 2: Analytics Dashboard 
**Goal:** Streamlit dashboard for data visualization

- [ ] Streamlit setup
- [ ] Rating distribution charts
- [ ] Genre analysis
- [ ] Completion rates tracking
- [ ] Top-rated content rankings
- [ ] Temporal trends (ratings over time)
- [ ] Director/author analysis
- [ ] Advanced search and filtering
- [ ] CSV export functionality

---

### Phase 3: Enhanced Features (Q3 2026)
**Goal:** Advanced functionality and data portability

- [ ] Batch import from Letterboxd CSV
- [ ] Batch import from Goodreads CSV
- [ ] Batch import from MyAnimeList
- [ ] Offline mode with delayed enrichment
- [ ] Custom fields support
- [ ] Review templates
- [ ] Fuzzy duplicate detection
- [ ] Automatic backups to cloud (optional)

---

### Phase 4: Web Platform (2027+)
**Goal:** Public web application

- [ ] FastAPI REST API
- [ ] React frontend
- [ ] User authentication
- [ ] PostgreSQL optimization
- [ ] Cloud deployment (optional)
- [ ] Social features (sharing, following)
- [ ] Recommendation system

---

### Phase 5: Ecosystem Expansion (2027+)
**Goal:** Full multi-platform ecosystem

- [ ] Mobile app (React Native)
- [ ] ML-powered recommendations
- [ ] Newsletter integration
- [ ] Annual wrap-up feature (like Spotify Wrapped)
- [ ] Community features
- [ ] Public API for third-party integrations

---

## Contributing

PLASM is open source! Contributions are welcome once Phase 1 is stable.

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch:**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Make your changes** (follow PEP 8 style)
4. **Add tests** for new features
5. **Commit your changes:**
   ```bash
   git commit -m "Add: Brief description"
   ```
6. **Push to your fork:**
   ```bash
   git push origin feature/amazing-feature
   ```
7. **Open a Pull Request** with detailed description


## Acknowledgments

- **TMDb** for comprehensive film and series metadata
- **Jikan** for MyAnimeList API access
- **Google Books API** for book metadata
- Open source community for tools and inspiration

## 🚀 Quick Start (TL;DR)

```bash
# 1. Clone
git clone https://github.com/Code-Cram/PLASM-project.git
cd PLASM-project

# 2. Create PostgreSQL database
psql -U postgres -c "CREATE DATABASE plasm_db;"

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure
cp config.example.py config.py
# Edit config.py with your API keys

# 5. Initialize database
python setup_database.py

# 6. Run
python main.py
```

**Need help?** Open an issue: https://github.com/Code-Cram/PLASM-project/issues
