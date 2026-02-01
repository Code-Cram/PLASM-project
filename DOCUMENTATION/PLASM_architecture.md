PLASM - Architecture and Project Structure

El proyecto PLASM se estructura en tres niveles:

Nivel 1: Python Backend (Core Logic)
Nivel 2: SQLDatabase (Data Persistence)
Nivel 3: User Interface Frontend (Presentation & Interaction)

NIVEL 1: Python Backend Architecture

Disclaimer: Importante tener en cuenta el siguiente diagrama donde se revela la dependencia de módulos entre otros módulos
main.py
  ├── content_handler.py
  │     ├── api_manager.py
  │     │     └── preprocessing/*
  │     └── utils/validators.py
  ├── data_fusion.py
  │     └── config.py
  └── storage/
        ├── sql_handler.py
        └── json_handler.py

También, tener en cuenta como se desarrolla el control de errores para los distintos programas.
Categorías de errores:
1. InputError: Validación fallida del usuario → Retry local
2. APIError: Timeout/rate limit → Exponential backoff (3 intentos)
3. DatabaseError: SQL constraint violation → Rollback + mensaje
4. ValidationError: Datos inconsistentes → Detener workflow, logging

Logging strategy:
- Nivel DEBUG: API calls con payloads
- Nivel INFO: Flujo de etapas completadas
- Nivel ERROR: Fallos con traceback



Módulo 1: main.py (Orquestación)

Responsabilidad: Punto de entrada y coordinación global. En este módulo el usuario podrá decidir entre borrar una review, añadir una review, ver las reviews o simplemente abandonar. En un futuro podemos incluir más opciones como una lista para guardar películas que queremos ver por ejemplo.

Funciones principales:
- Inicializar aplicación
- Cargar configuración y credenciales
- Gestionar flujo de ejecución principal
- Mostrar menú de opciones
Dependencias: todos los demás módulos (los demás scripts)
Patrones: configuración y opciones usuario



Módulo 2: content_handler.py (Interacción con el user)

Responsabilidad: Captura de input del usuario y presentación de datos. Este módulo se activa siempre que el user quiera añadir una review. Este módulo es el más importante, ya que es el que más funciones incluyes y más desarrollo complejo lleva. Se encarga tanto de crear la review como crear el json, como preguntar al user toda la información necesaria.

Funciones:
- get_content_type() - Seleccionar tipo de contenido
- get_title() - Ingresar título
- display_content_details() - Mostrar información enriquecida
- select_from_results() - Elegir de resultados de búsqueda
- choose_review_type() - Seleccionar modo rating
- get_analytic_ratings() - Capturar evaluación estructurada
- get_subjective_rating() - Capturar evaluación rápida
- get_common_review_data() - Capturar reseña y metadatos
Patrones: Input validation, Error handling, Pretty printing



Módulo 3: api_manager.py (Integración de APIs)

Responsabilidad: Comunicación con APIs externas y normalización

Funciones:
- search_content() - Búsqueda centralizada (router)
- _search_tmdb_movie() - Búsqueda TMDb (films)
- _search_tmdb_series() - Búsqueda TMDb (series)
- _search_jikan_anime() - Búsqueda Jikan (anime)
- _search_jikan_manga() - Búsqueda Jikan (manga)
- _search_googlebooks() - Búsqueda Google Books
- fetch_complete_data() - Obtención de datos completos
- _download_poster() - Descargar y guardar posters localmente
Patrones: Retry logic (exponential backoff), Caching, Factory pattern (router APIs)



Módulo 4: preprocessing/ (Normalización de Datos)
Responsabilidad: Transformar respuestas de APIs a esquema estándar. Es decir, al disponer de diversas APIs cada una devolverá datos diferentes con atributos diferentes. Buscamos tener una estandarización para no tener problemas después al construir la base de datos en SQL.

Submódulos:
- tmdb_preprocessor.py: preprocess_tmdb_film(), preprocess_tmdb_series()
- jikan_preprocessor.py: preprocess_jikan_anime(), preprocess_jikan_manga()
- googlebooks_preprocessor.py: preprocess_google_books()
Salida común: Diccionario normalizado con campos estándar
Patrones: Strategy pattern (preprocesadores específicos por API)



Módulo 5: data_fusion.py (Consolidación)
Responsabilidad: Fusión de API data + ratings + notas personales. En este script se busca la creación total del json/diccionario donde se encuentra la info que viene de la API, como el rating, el poster, el género y también se incluye la nota del user más toda la información que quiera aportar.

Función principal:
- merge_all_data() - Combina 4 componentes en structure final
Validaciones:
- Campos requeridos presentes
- Ratings en rango 0-10
- final_score calculado correctamente
- Detección de duplicados
Salida: final_data dict con todos los campos listos para DB



Módulo 6: storage/sql_handler.py (Persistencia SQL)

Responsabilidad: Operaciones de base de datos. En este script desarrollamos el manejador del SQL. Es decir, la base de datos del user.

Funciones:
- save_review() - Insertar nuevo review
- update_review() - Actualizar review existente
- get_all_reviews() - Obtener todos los reviews
- search_reviews() - Búsqueda por criterios
- check_duplicate() - Verificar si ya existe
Transacciones: Commit/rollback en caso de error
Patrones: Connection pooling (si escalamos)



Módulo 7: storage/json_handler.py (Exportación)

Responsabilidad: Exportar reviews en formato JSON para almacenarlas en SQL.

Funciones:
- export_to_json() - Guardar individual review a JSON
- import_from_json() - Importar JSON a memoria
- batch_export() - Exportar todos los reviews
Formato: JSON lines o single file por review
Ubicación: data/exports/



Módulo 8: utils/validators.py (Validación)

Responsabilidad: Validadores reutilizables. No son más que controles de errores.

Funciones:
- validate_content_type()
- validate_rating()
- validate_title_length()
- validate_email() - si Phase 2 trae usuarios
Patrón: Validadores como funciones puras

Módulo: utils/formatters.py (Presentación)
Responsabilidad: Formateo de output para terminal
Funciones:
- format_content_details()
- format_search_results()
- format_success_message()
- format_error_message()
Uso: Separar lógica de presentación de lógica de negocio



Módulo 9: config.py (Configuración)
Responsabilidad: Centralizar constantes y credenciales. Es una especie de controlador de errores a nivel scripts. Maneja que todos los datos que cojen los demás scripts sean correctos. Además, se añaden los distintos pesos a la hora de calificar.
Contenido:
- API keys (TMDb, Google Books)
- Paths (data/, exports/, posters/)
- Content type definitions
- Analytic weights por tipo. Por ejemplo, en películas:
    "film": {
        "direction": 0.20,
        "writing": 0.20,
        "acting": 0.20,
        "technical": 0.20,
        "emotional_impact": 0.20
- Retry configuration
Patrón: Environment variables + defaults






NIVEL 2:Database Layer Architecture

Base de Datos: SQLite

Justificación de SQLite sobre alternativas:
- Monousuario local: Sin necesidad de servidor
- JSON nativo: Soporta JSON columns (SQLite 3.38+)
- Portabilidad: Todo en un archivo .db
- Integración pandas: pd.read_sql() directo
- Migración futura: Schema idéntico para PostgreSQL

Tabla Principal: reviews

Campo: id
Tipo: INTEGER PRIMARY KEY AUTOINCREMENT
Propósito: Identificador único
Índice: Sí (primario)

Campo: content_type
Tipo: TEXT CHECK
Valores: film | series | anime | manga | book
Índice: Sí (búsquedas frecuentes)

Campo: source_api
Tipo: TEXT
Valores: tmdb | jikan | googlebooks

Campo: api_id
Tipo: TEXT UNIQUE NOT NULL
Propósito: Identificador externo (evita duplicados)
Ejemplo: tmdb_551, jikan_1_anime

Campo: title
Tipo: TEXT NOT NULL
Propósito: Título del contenido
Longitud: <= 255 caracteres

Campo: original_title
Tipo: TEXT
Propósito: Título original (ej: "火影忍者" para Naruto)

Campo: year
Tipo: INTEGER
Propósito: Año de release/publicación

Campo: description
Tipo: TEXT
Propósito: Sinopsis/descripción

Campo: poster_url
Tipo: TEXT
Propósito: URL original en API

Campo: poster_local_path
Tipo: TEXT
Propósito: Ruta local (data/posters/)

Campo: api_rating
Tipo: REAL
Propósito: Rating promedio de la plataforma origen

Campos Content-Specific (Películas)
director, runtime (minutos), budget, revenue, imdb_id, production_companies (JSON)

Campos Content-Specific (Series)
seasons, episodes, series_status

Campos Content-Specific (Anime/Manga)
studio, chapters/episodes count

Campos Content-Specific (Libros)
author, pages, isbn

Campos Content-Specific (Todos)
genres (JSON array), release_date

Campos Review Data

Campo: review_type
Tipo: TEXT CHECK
Valores: analytic | subjective

Campo: analytic_ratings
Tipo: JSON
Estructura (si review_type == analytic):
{
  "direction": 8,
  "writing": 7,
  "acting": 8,
  "technical": 9,
  "emotional_impact": 9,
  "final_score": 8.25
}

Campo: subjective_rating
Tipo: JSON
Estructura (si review_type == subjective):
{
  "overall_score": 8
}

Campo: review_text
Tipo: TEXT
Propósito: Reseña libre del usuario (opcional)

Campo: would_rewatch
Tipo: BOOLEAN DEFAULT 0
Propósito: ¿Vería de nuevo?

Campo: watch_context
Tipo: TEXT
Valores: cinema | home_tv | streaming | other

Campo: status
Tipo: TEXT DEFAULT visto
Valores: visto | en_progreso | pendiente | dropped

Campos Metadata

Campo: date_added
Tipo: TIMESTAMP DEFAULT CURRENT_TIMESTAMP
Propósito: Cuándo se ingresó el review

Campo: date_completed
Tipo: TIMESTAMP
Propósito: Cuándo se terminó de ver (opcional)

Índices

idx_content_type: Búsquedas por tipo
idx_status: Filtrados por estado
idx_date_added: Ordenamientos cronológicos
idx_api_id: Detección de duplicados (UNIQUE)

Estrategia de Escalado

v1: SQLite local (actual plan)
v1.5: SQLite con backups automáticos en JSON
v2: Migración a PostgreSQL (schema idéntico)
v2.5: Replicación/sincronización (opcional)







NIVEL 3: User Interface Architecture

Nivel personal (focus rigth now) CLI (Terminal)

Responsabilidad: Interacción con usuario
Características:
- Menús navegables
- Validación de input interactiva
- Pretty printing de resultados
- Manejo de errores con mensajes claros

Componentes CLI:
1. Menu System: Opciones numeradas, validación
2. Input Capture: get_content_type(), get_title(), etc
3. Display Engine: Formateo de resultados, posters ASCII
4. Error Handling: Try-catch con mensajes al usuario
5. Confirmations: Y/N prompts para acciones críticas

Flujo de Pantallas (User Journey)

Pantalla 1: Welcome & Main Menu
Opciones: Add review | View reviews | Search | Exit
Acciones: main.py

Pantalla 2: Content Type Selection
Menú con PLASM types
Acción: content_handler.get_content_type()

Pantalla 3: Title Input
Prompt: "Enter title:"
Acción: content_handler.get_title()

Pantalla 4: API Search Results
Lista de 3-5 resultados con posters
Acción: content_handler.select_from_results()

Pantalla 5: Content Details Confirmation
Mostrar metadata enriquecida
Acción: content_handler.display_content_details()

Pantalla 6: Review Type Selection
Analytic vs Subjective
Acción: content_handler.choose_review_type()

Pantalla 7: Rating Input
(A) Si Analytic: 5 dimensiones con pesos
(B) Si Subjective: 1 rating overall
Acción: get_analytic_ratings() o get_subjective_rating()

Pantalla 8: Common Review Data
Review text, would rewatch, context, status
Acción: content_handler.get_common_review_data()

Pantalla 9: Confirmation & Save
Mostrar resumen
Guardar en DB y JSON
Acción: sql_handler.save_review(), json_handler.export_to_json()

Pantalla 10: Success Message
Review guardado exitosamente
Loop back to Pantalla 1

Future UI Layers (Phase 2+)

Streamlit Dashboard (Phase 2):
- Statistics: ratings distribution, genre analysis
- Visualizations: charts, trends, tier lists
- Advanced search: filters, sort, aggregations
- Analytics: correlations, insights

Web Interface (Phase 3):
- React/Vue frontend
- FastAPI backend
- Multi-user support
- Cloud deployment option

API REST (Phase 3):
- GET /reviews
- POST /reviews
- PUT /reviews/{id}
- DELETE /reviews/{id}
- GET /analytics/...

Conexiones Inter-módulos

main.py
├─ Llama content_handler.get_content_type()
├─ Llama api_manager.search_content()
├─ Llama content_handler.select_from_results()
├─ Llama api_manager.fetch_complete_data()
├─ Llama content_handler.choose_review_type()
├─ Llama get_analytic_ratings() o get_subjective_rating()
├─ Llama content_handler.get_common_review_data()
├─ Llama data_fusion.merge_all_data()
├─ Llama sql_handler.save_review()
└─ Llama json_handler.export_to_json()

api_manager.py
├─ Usa config.py para API keys y rutas
├─ Llama preprocessing.*.py para normalización
└─ Llama storage para download de posters

data_fusion.py
├─ Toma input de content_handler
├─ Valida usando validators
├─ Llama sql_handler.check_duplicate()

storage/
├─ Usa utils.validators para integridad
└─ Genera logs en data/logs/
