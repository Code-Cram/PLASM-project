
Project Directory Structure:

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
