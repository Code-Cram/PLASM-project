# PLASM Project - Internal Documentation for Perplexity AI

**Last Updated:** January 30, 2026, 4:23 PM CET  
**User:** Marc Martínez (Data Science student, UAM, Tarragona)  
**Project Status:** Architecture & Planning Phase (not yet coded)

---

## 📋 EXECUTIVE SUMMARY

**PLASM** is a personal content review management system designed for Marc Martínez—a Data Science student at UAM with advanced analytical skills in Python, SQL, and data manipulation.

**Core Purpose:**
- Centralized system to review and rate films, series, anime, manga, and books
- Structured analysis using weighted rating dimensions (for analytical reviews)
- Local-first, single-user system with SQLite backend + JSON exports
- Integration with public APIs (TMDb, Jikan, Google Books) for metadata enrichment
- Future Streamlit dashboard for analytics and visualization

**Technology Stack (Decided):**
- **Backend:** SQLite (not MongoDB) with JSON columns
- **Language:** Python 3.8+
- **APIs:** TMDb, Jikan API, Google Books API
- **Data Format:** JSON for exports, normalized across all content types
- **Frontend (Future):** Streamlit dashboard
- **Storage:** Local filesystem + SQLite database

---

## 👤 USER PROFILE (Marc Martínez Context)

### Personality & Work Style
- **Analytical & methodical:** Demands precision, complete justification, logical clarity
- **Direct communication:** Informal tone, no unnecessary fluff, action-oriented
- **Deep understanding preference:** Not just solutions, but WHY things work that way
- **Problem-solving approach:** Code-first, understand through implementation
- **Rigorous standards:** Expects well-justified architectural decisions

### Technical Expertise
- **Primary Languages:** Python (pandas, NumPy, scikit-learn), MATLAB, SQL, R
- **Databases:** SQLite, PostgreSQL, SQL optimization
- **Tools:** VS Code, pgAdmin, Jupyter Notebooks, Linux terminal
- **Specializations:** Signal processing, machine learning, statistical modeling, time series analysis
- **Current Role:** Class delegate (delegado) for 2nd year Data Science program at UAM

### Learning Context
- 2nd year Data Science degree (UAM)
- Intensive exam preparation habits (long study sessions)
- Active engagement with course material through problem-solving
- Interests in advanced topics: convex analysis, linear optimization, quantum computing

### Professional Standards
- Expects responses to be **rigorous, complete, and well-justified**
- Prefers **hand-on problem-solving** through coding and implementation
- Values **understanding the reasoning** behind each architectural decision
- Demands **clarity without ambiguity** in technical explanations
- Appreciates **data-driven decisions** (real examples, not hypothetical scenarios)

---

## 🎯 PROJECT SCOPE & VISION

### What PLASM Is
A **personal content review management system** that allows Marc to:

1. **Easily add reviews** of films, series, anime, manga, and books
2. **Rate content systematically** using either:
   - **Analytic reviews:** Structured ratings across dimensions (direction, writing, acting, technical, emotional impact) with automatic weighted final score
   - **Subjective reviews:** Simple overall rating (0-10)
3. **Enrich data automatically** by searching external APIs (TMDb for films/series, Jikan for anime/manga, Google Books for books)
4. **Store reviews persistently** in SQLite with JSON exports
5. **Analyze review data** through future Streamlit dashboard (planned Phase 2)
6. **Export reviews** in portable JSON format for backup/portability

### What PLASM Is NOT
- Not a social platform (no user accounts, sharing, comments, social features)
- Not a web application (local desktop app initially)
- Not for real-time data (batch imports only)
- Not a recommendation engine (v1 is management + analysis, not ML)

### Scope Boundaries (v1)
**INCLUDED:**
- ✅ Local SQLite storage
- ✅ API integration (TMDb, Jikan, Google Books)
- ✅ Analytic + subjective review types
- ✅ JSON export for each review
- ✅ Terminal/CLI interface
- ✅ Poster downloading and local storage

**EXCLUDED (Phase 2+):**
- ❌ Streamlit dashboard (planned after v1)
- ❌ Multi-user support
- ❌ Cloud deployment
- ❌ Web interface
- ❌ Recommendation algorithms
- ❌ Social features

---

## 🏗️ ARCHITECTURE DECISIONS

### Database: SQLite (NOT MongoDB)

**Decision Rationale (discussed January 28, 2026):**

| Criterion | SQLite | MongoDB |
|-----------|--------|---------|
| Setup Complexity | ✅ Zero (built-in) | ❌ Server installation required |
| JSON Support | ✅ Native JSON type | ✅ BSON documents |
| Query Complexity | ✅ SQL (familiar to Marc) | ⚠️ Aggregation pipeline |
| Single-user Fit | ✅ Perfect | ❌ Overkill |
| Portability | ✅ `.db` file = backup | ❌ Requires MongoDB |
| Streamlit Integration | ✅ `pd.read_sql()` direct | ⚠️ `pymongo` → DataFrame conversion |

**Final Decision:** **SQLite with JSON columns** for:
- JSON natively stored in `JSON` columns (SQLite 3.38+)
- SQL queries Marc already knows
- Zero configuration
- Single command portability

**Future Migration Path:** If PLASM grows to multi-user: SQLite → PostgreSQL (schema identical, minimal refactoring)

---

## 📊 DATA MODEL

### Core Entities

#### 1. **Review** (Main entity)
```
id (auto-increment)
content_type (film | series | anime | manga | book)
source_api (tmdb | jikan | googlebooks)
api_id (UNIQUE, e.g., "tmdb_551")
review_type (analytic | subjective)
status (visto | en_progreso | pendiente)
date_added (timestamp)
```

#### 2. **Content Metadata** (from APIs)
All fields except those in review-specific sections:
```
title, original_title, year, description
poster_url, poster_local_path
api_rating
release_date
```

#### 3. **Content-Specific Fields**
**Films:**
- director, runtime, budget, revenue, imdb_id, production_companies (JSON)

**Series:**
- seasons, episodes, series_status

**Anime/Manga:**
- studio, chapters_episodes

**Books:**
- author, pages, isbn

**All:**
- genres (JSON array)

#### 4. **Review Data**
**Analytic Reviews:**
```json
{
  "direction": 8,
  "writing": 7,
  "acting": 8,
  "technical": 9,
  "emotional_impact": 9,
  "final_score": 8.25  // Auto-calculated: sum(rating × weight)
}
```

**Subjective Reviews:**
```json
{
  "overall_score": 8
}
```

**Common to Both:**
```
review_text (optional free-text review)
would_rewatch (boolean)
watch_context (cinema | home | streaming)
status (visto | en_progreso | pendiente)
```

### SQL Schema (SQLite)

**File:** `plasm.db` (single file)

```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Identification
    content_type TEXT CHECK(content_type IN ('film','series','anime','manga','book')),
    source_api TEXT CHECK(source_api IN ('tmdb','jikan','googlebooks')),
    api_id TEXT UNIQUE NOT NULL,
    
    -- Core metadata
    title TEXT NOT NULL,
    original_title TEXT,
    year INTEGER,
    poster_url TEXT,
    poster_local_path TEXT,
    description TEXT,
    api_rating REAL,
    
    -- Content-specific fields
    director TEXT,
    runtime INTEGER,
    genres JSON,
    release_date DATE,
    budget INTEGER,
    revenue INTEGER,
    production_companies JSON,
    imdb_id TEXT,
    seasons INTEGER,
    episodes INTEGER,
    series_status TEXT,
    studio TEXT,
    author TEXT,
    pages INTEGER,
    
    -- Review data
    review_type TEXT CHECK(review_type IN ('analytic','subjective')),
    analytic_ratings JSON,
    subjective_rating JSON,
    review_text TEXT,
    would_rewatch BOOLEAN DEFAULT 0,
    watch_context TEXT,
    status TEXT DEFAULT 'visto',
    
    -- Metadata
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_completed TIMESTAMP,
    
    -- Indexes
    UNIQUE(api_id)
);

CREATE INDEX idx_content_type ON reviews(content_type);
CREATE INDEX idx_status ON reviews(status);
CREATE INDEX idx_date_added ON reviews(date_added);
```

---

## 🔄 COMPLETE PROGRAM FLOW (Detailed)

**15-Stage Pipeline** (documented January 28, 2026)

### Stage 1: Entry Point (`main.py`)
- Program starts
- Display welcome message
- Show menu: "Add new review | View reviews | Search | Exit"
- User selects option

### Stage 2: Content Type Selection (`content_handler.py`)
- Display menu: "Film | Series | Anime | Manga | Book?"
- User input: normalized to lowercase, validated against PLASM constants
- **Output:** `content_type` = "film" | "series" | "anime" | "manga" | "book"

### Stage 3: Title Input (`content_handler.py`)
- Prompt: "Enter the title:"
- User input: "The Poseidon Adventure"
- Validation: non-empty, reasonable length
- **Output:** `title` = user input

### Stage 4: API Search (`api_manager.py`)
- Route to correct API based on `content_type`:
  - `"film"` → TMDb search_movie()
  - `"series"` → TMDb search_tv()
  - `"anime"` → Jikan search_anime()
  - `"manga"` → Jikan search_manga()
  - `"book"` → Google Books search_books()
- Retry logic: max 3 retries, 5-second timeout, exponential backoff
- **Output:** List of 3-5 normalized results (max)

```python
# Example output structure:
[
    {
        "id": 551,
        "title": "The Poseidon Adventure",
        "year": 1972,
        "poster_path": "/6RGiA5BfhelU9zoD0b1GAG4GWWf.jpg",
        "overview": "When their ocean liner capsizes...",
        "vote_average": 7.095
    },
    ...
]
```

### Stage 5: User Selects Result (`content_handler.py`)
- Display prettified results (with poster thumbnails, ratings, descriptions)
- User input: "1" (choose from 1-5)
- Validation: valid number within range
- **Output:** `selected_result` = full object from search results

### Stage 6: Fetch Complete Data (`api_manager.py`)
- Make detailed API call using selected result's ID
- Fetch additional data: credits, reviews, translations
- **Preprocess** based on content type:
  - `preprocess_tmdb_film()`
  - `preprocess_tmdb_series()`
  - `preprocess_jikan_anime()`
  - `preprocess_jikan_manga()`
  - `preprocess_google_books()`
- Download poster locally: `data/posters/The_Poseidon_Adventure.jpg`
- **Output:** Normalized complete data dict with all fields

```python
{
    "content_type": "film",
    "source_api": "tmdb",
    "api_id": "tmdb_551",
    "title": "The Poseidon Adventure",
    "year": 1972,
    "poster_url": "https://...",
    "poster_local_path": "data/posters/The_Poseidon_Adventure.jpg",
    "description": "...",
    "api_rating": 7.095,
    "director": "Ronald Neame",
    "runtime": 117,
    "genres": ["Adventure", "Drama", "Thriller"],
    ...
}
```

### Stage 7: Display to User (`content_handler.py`)
- Show prettified content details: title, poster, director, runtime, genres, description
- User confirms: "Ready to review? (y/n)"

### Stage 8: Review Type Selection (`content_handler.py`)
- Menu: "ANALYTIC (structured ratings) | SUBJECTIVE (overall score)?"
- User input: "1" (ANALYTIC) or "2" (SUBJECTIVE)
- **Output:** `review_type` = "analytic" | "subjective"

### Stage 9A: Analytic Review Path (`content_handler.py`)
**For each dimension** (with weights from `ANALYTIC_WEIGHTS[content_type]`):

1. **Direction (20%)** → Ask rating 0-10
2. **Writing (20%)** → Ask rating 0-10
3. **Acting (15%)** → Ask rating 0-10
4. **Technical (15%)** → Ask rating 0-10
5. **Emotional Impact (30%)** → Ask rating 0-10

**Automatic calculation:**
```
final_score = (8 × 0.20) + (7 × 0.20) + (8 × 0.15) + (9 × 0.15) + (9 × 0.30)
            = 8.25
```

**Output:**
```json
{
    "direction": 8,
    "writing": 7,
    "acting": 8,
    "technical": 9,
    "emotional_impact": 9,
    "final_score": 8.25
}
```

### Stage 9B: Subjective Review Path (`content_handler.py`)
- Prompt: "Overall rating (0-10)?"
- User input: "8"
- **Output:**
```json
{
    "overall_score": 8
}
```

### Stage 10: Common Review Data (`content_handler.py`)
**For BOTH paths**, ask:

1. **Review text (optional):** Free-form review
2. **Would rewatch?** (y/n) → `would_rewatch` = bool
3. **Watch context:** (cinema | home | streaming)
4. **Status:** (visto | en_progreso | pendiente) [default: "visto"]

**Output:**
```python
{
    "review_text": "Great adventure film from the 70s...",
    "would_rewatch": True,
    "watch_context": "home",
    "status": "visto"
}
```

### Stage 11: Data Fusion (`data_fusion.py`)
**Merge all components:**
```python
final_data = {
    # API data (all fields)
    **api_data,
    
    # Review configuration
    "review_type": "analytic",
    "analytic_ratings": {...},
    "subjective_rating": None,  # Not used in analytic
    
    # Common review fields
    "review_text": "...",
    "would_rewatch": True,
    "watch_context": "home",
    "status": "visto",
    
    # Metadata
    "date_added": "2026-01-28T17:36:00"
}
```

**Validation:**
- Check no missing required fields
- Validate ratings are 0-10
- Check `final_score` calculated correctly
- Query DB: Does `api_id` already exist?
  - If YES → Warn "Already reviewed. Update? (y/n)"
  - If NO → Continue

### Stage 12: Save to SQL (`storage/sql_handler.py`)
- Convert complex fields to JSON strings
- INSERT into `reviews` table
- Handle errors: unique constraint violation, invalid data
- Commit transaction
- **Output:** `review_id` (auto-increment from DB)

### Stage 13: Export to JSON (`storage/json_handler.py`)
- Convert `final_data` dict to JSON string
- Generate filename: `review_The_Poseidon_Adventure_2026-01-28.json`
- Save to: `data/exports/`
- **Output:** filepath

### Stage 14: Completion Feedback (`content_handler.py`)
- Display success message with review summary
- Show: Title, Type, Score, Status, Save locations

### Stage 15: Loop/Exit
- Menu: "Add another? View? Exit?"
- Back to Stage 1 or exit program

---

## 🔐 API Integration Details

### TMDb (The Movie Database)
**For:** Films & Series

**Endpoints:**
- Search: `GET /search/movie?query=...&api_key=...`
- Details: `GET /movie/{id}?api_key=...`
- Credits: `GET /movie/{id}/credits?api_key=...`

**Auth:** API key in `config.py`

**Rate limit:** 40 requests/10 seconds

**Preprocessing:** Extract fields, normalize to standard schema

### Jikan API (Anime/Manga)
**For:** Anime & Manga

**Endpoints:**
- Search: `GET https://api.jikan.moe/v4/anime?query=...`
- Details: `GET https://api.jikan.moe/v4/anime/{id}`

**Rate limit:** 60 requests/minute

**No auth needed:** Public API

### Google Books API
**For:** Books

**Endpoints:**
- Search: `GET https://www.googleapis.com/books/v1/volumes?q=...`

**Auth:** API key in `config.py`

**Rate limit:** 1000 requests/day

---

## 📁 Project Directory Structure

```
plasm/
│
├── plasm.db                          # SQLite database (single file)
├── config.py                         # API keys, constants, paths, weights
├── main.py                           # Entry point, main loop
│
├── content_handler.py                # User input + display logic
│   ├── get_content_type()
│   ├── get_title()
│   ├── select_from_results()
│   ├── display_content_details()
│   ├── choose_review_type()
│   ├── get_analytic_ratings()
│   ├── get_subjective_rating()
│   └── get_common_review_data()
│
├── api_manager.py                    # API interactions
│   ├── search_content()              # Route to correct API
│   ├── fetch_complete_data()
│   ├── _search_tmdb_movie()
│   ├── _search_tmdb_series()
│   ├── _search_jikan_anime()
│   ├── _search_jikan_manga()
│   ├── _search_googlebooks()
│   ├── _download_poster()
│   └── RetryHandler (context manager)
│
├── preprocessing/                    # Data normalization
│   ├── __init__.py
│   ├── tmdb_preprocessor.py
│   │   ├── preprocess_tmdb_film()
│   │   └── preprocess_tmdb_series()
│   ├── jikan_preprocessor.py
│   │   ├── preprocess_jikan_anime()
│   │   └── preprocess_jikan_manga()
│   └── googlebooks_preprocessor.py
│       └── preprocess_google_books()
│
├── data_fusion.py                    # Merge all data
│   └── merge_all_data()
│
├── storage/                          # Persistence layer
│   ├── __init__.py
│   ├── sql_handler.py
│   │   ├── save_review()
│   │   ├── get_all_reviews()
│   │   ├── search_reviews()
│   │   └── update_review()
│   └── json_handler.py
│       ├── export_to_json()
│       └── import_from_json()
│
├── data/                             # Data files
│   ├── posters/                      # Downloaded poster images
│   │   └── The_Poseidon_Adventure.jpg
│   ├── exports/                      # JSON backups
│   │   └── review_The_Poseidon_Adventure_2026-01-28.json
│   └── logs/                         # (Optional) API call logs
│
└── utils/                            # Helper functions
    ├── __init__.py
    ├── validators.py                 # Input validation
    ├── formatters.py                 # Pretty display
    └── constants.py                  # PLASM constants
```

---

## ⚙️ Configuration (config.py)

```python
# API Keys
TMDB_API_KEY = "your_key_here"
JIKAN_API_KEY = None  # Jikan is public
GOOGLE_BOOKS_API_KEY = "your_key_here"

# Paths
DB_PATH = "plasm.db"
POSTERS_DIR = "data/posters/"
EXPORTS_DIR = "data/exports/"

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
        "direction": 0.20,
        "writing": 0.25,
        "acting": 0.15,
        "technical": 0.10,
        "emotional_impact": 0.30
    },
    "anime": {...},
    "manga": {...},
    "book": {...}
}

# API retry configuration
MAX_RETRIES = 3
RETRY_TIMEOUT = 5
BACKOFF_FACTOR = 1.5

# Defaults
DEFAULT_STATUS = "visto"
DEFAULT_WATCH_CONTEXT = "home"
```

---

## 🚀 DEVELOPMENT ROADMAP

### ✅ COMPLETED (as of Jan 30, 2026)
1. ✅ Conceptualization and scope definition
2. ✅ Architecture decision (SQLite vs MongoDB)
3. ✅ Data model design
4. ✅ Complete flow documentation
5. ✅ Directory structure planning
6. ✅ Config template design

### 📋 TODO (Phase 1: Core Functionality)
**Stage 1: Setup & Infrastructure**
1. [ ] Create SQLite schema (create_tables.sql)
2. [ ] Implement `config.py` with real API keys
3. [ ] Create directory structure

**Stage 2: API Integration**
1. [ ] Implement `api_manager.py` with TMDb integration
   - [ ] `search_tmdb_movie()`
   - [ ] `search_tmdb_series()`
   - [ ] Retry handler with exponential backoff
2. [ ] Implement Jikan integration for anime/manga
3. [ ] Implement Google Books integration
4. [ ] Implement poster downloading

**Stage 3: Preprocessing**
1. [ ] Implement `preprocessing/tmdb_preprocessor.py`
   - [ ] Normalize film metadata
   - [ ] Normalize series metadata
2. [ ] Implement `preprocessing/jikan_preprocessor.py`
3. [ ] Implement `preprocessing/googlebooks_preprocessor.py`

**Stage 4: User Interface**
1. [ ] Implement `content_handler.py` with all input functions
2. [ ] Implement prettier display with colors/formatting
3. [ ] Implement validation and error handling

**Stage 5: Core Logic**
1. [ ] Implement `data_fusion.py` for merging
2. [ ] Implement `storage/sql_handler.py` for DB operations
3. [ ] Implement `storage/json_handler.py` for exports

**Stage 6: Testing**
1. [ ] Integration tests with real API calls
2. [ ] Edge cases (no results, API down, invalid input)
3. [ ] User acceptance testing

### 📊 Phase 2 (Future, not in scope)
- [ ] Streamlit dashboard for analytics
- [ ] Charts: rating distributions, genre analysis, completion rates
- [ ] Advanced search and filtering
- [ ] Data export to CSV
- [ ] Stats: average ratings by genre, most reviewed content type, etc.

### 🌐 Phase 3 (Future, much later)
- [ ] Web interface
- [ ] Multi-user support
- [ ] Cloud database (PostgreSQL migration)
- [ ] Social features (sharing, recommendations)
- [ ] ML-based recommendations

---

## 🔍 KEY TECHNICAL DECISIONS & RATIONALES

### 1. **Why SQLite and not MongoDB?**
- **Single-user local application** → SQLite is perfect fit
- **JSON columns available** (SQLite 3.38+) for nested data
- **Marc knows SQL** → No learning curve
- **Zero configuration** → `plasm.db` is just a file
- **Easy migration path** → Identical schema works with PostgreSQL later
- **Streamlit integration** → `pd.read_sql()` is direct and efficient

### 2. **Why preprocess each API into standard schema?**
- **Consistency** → All reviews use same column structure regardless of source API
- **Query simplicity** → Can query across content types easily
- **Future-proofing** → Easy to add new APIs without changing DB schema
- **Clean separation** → API logic separated from core business logic

### 3. **Why separate analytic and subjective reviews?**
- **Flexibility** → User can choose rating style based on mood/content
- **Data richness** → Analytic reviews give dimensional insights
- **Simplicity option** → Subjective for quick ratings
- **Future analytics** → Can correlate dimensions with satisfaction

### 4. **Why download posters locally?**
- **Resilience** → Works offline, API downtime doesn't break display
- **Performance** → No re-downloading from external URLs
- **Storage** → Permanent record with review

### 5. **Why JSON exports alongside SQLite?**
- **Portability** → Reviews readable in any text editor
- **Backup** → Independent backup format
- **Integration** → Can import to other systems easily
- **Human-readable** → Marc can inspect raw data

---

## 🧠 REMEMBER FOR FUTURE SESSIONS

### About Marc
- **Highly analytical, demands precision** → No hand-waving explanations
- **Knows SQL well** → Can use complex queries directly
- **Prefers implementation** → Show working code, not theory
- **Direct communication style** → Be concise, avoid fluff
- **Rigorous standards** → Every architectural choice should be justified

### Project Constraints
- **Single-user local app** → No need for scalability yet
- **Personal use case** → Design can be opinionated to Marc's workflow
- **Local-first** → Offline operation required
- **Extensible architecture** → Leave room for Streamlit dashboard later

### Technical Foundations
- **No MongoDB** → SQLite with JSON columns (decided)
- **15-stage pipeline** → Know exactly where user is in flow
- **3 APIs** → TMDb (films/series), Jikan (anime/manga), Google Books (books)
- **Analytic weights** → Vary by content type (defined in config)
- **Standard schema** → All content types normalized to same structure

### Next Steps (When Resuming)
Start with **Stage 1: Setup & Infrastructure**
1. Create `config.py` with API key placeholders
2. Create SQLite schema
3. Implement basic `api_manager.py` with TMDb integration
4. Test with actual API calls

---

## 📞 SESSION HISTORY

### Session 1: January 28, 2026 (5:36 PM - later)
**Topics:**
- Described complete 15-stage program flow with detailed explanations
- Each stage with function signatures and data structures
- Example with "The Poseidon Adventure" film

### Session 2: January 28, 2026 (6:24 PM)
**Topics:**
- Architecture decision: SQL vs MongoDB for JSON data
- Chose SQLite with JSON columns
- Rationale: single-user, local-first, Marc knows SQL
- Showed SQLite schema design
- Practical examples of insertion and reading with pandas

### Session 3: January 30, 2026 (4:23 PM)
**Topics:**
- Created this comprehensive internal documentation
- Consolidated all project information
- Structured for future session references
- Included user profile, architecture decisions, complete flow, roadmap

---

## 🎓 LESSONS LEARNED / DECISIONS

1. **Simplicity > Flexibility** → SQLite beats MongoDB for v1
2. **API Agnostic** → Preprocess all APIs to standard schema
3. **User Experience** → Clear flow, one thing at a time
4. **Data Integrity** → Validate at every stage
5. **Extensibility** → Design for Streamlit dashboard from start
6. **Pragmatism** → Local-first, single-user constraints are features not bugs

---

**END OF DOCUMENTATION**

This document is the **source of truth** for PLASM development. Reference it in all future sessions to maintain architectural consistency and project coherence.
