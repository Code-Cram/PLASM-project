PLASM - Complete Workflow Documentation

Visión General del Flujo

El sistema PLASM funciona como un pipeline de 15 etapas claramente definidas. Cada etapa tiene un propósito específico, inputs bien definidos y outputs que sirven como inputs para la siguiente etapa. Este diseño secuencial garantiza que no se pierda información y que el usuario tenga control total del proceso.

Flujo de Datos Global

User Input → API Search → Selection → API Fetch → Preprocessing → Display → Review Type Choice → Ratings Capture → Common Data → Merge → Validation → SQL Save → JSON Export → Success

Etapa 1: Inicialización y Menú Principal

Ubicación: main.py
Descripción: El programa inicia, carga configuración y muestra el menú principal
Acciones:
1. Importar y ejecutar main()
2. Crear/conectar a plasm.db si no existe
3. Cargar variables de config.py (API keys, paths, constantes)
4. Mostrar mensaje de bienvenida
5. Mostrar menú con opciones:
   1. Add new review
   2. View all reviews
   3. Search reviews
   4. Exit

Usuario selecciona opción 1 (Add new review) para continuar al workflow de creación

Entrada: Nada (inicio del programa)
Salida: Usuario selecciona "Add new review"
Responsables: main.py

Etapa 2: Selección de Tipo de Contenido

Ubicación: content_handler.py, función get_content_type()
Descripción: El usuario especifica qué tipo de contenido desea reseñar
Acciones:
1. Mostrar menú de tipos disponibles:
   What type of content did you consume?
   1. Film (película)
   2. Series (serie)
   3. Anime (anime)
   4. Manga (manga)
   5. Book (libro)

2. El usuario ingresa su selección (número o nombre)
3. Normalizar entrada: convertir a minúsculas, eliminar espacios
4. Validar contra CONTENT_TYPES en config.py
5. Si inválido: mostrar error y repetir pregunta
6. Si válido: proceder

Entrada: User input (string)
Salida: content_type = "film" | "series" | "anime" | "manga" | "book"
Validación: Debe estar en lista permitida
Error handling: ValueError si es inválido
Responsable: content_handler.get_content_type()

Etapa 3: Ingreso del Título

Ubicación: content_handler.py, función get_title()
Descripción: El usuario ingresa el título del contenido que desea reseñar
Acciones:
1. Mostrar prompt específico al tipo:
   Enter the title of the [film/series/anime/manga/book]:
2. Leer input del usuario
3. Validar:
   - No está vacío
   - No es más de 255 caracteres
   - No contiene caracteres prohibidos
4. Si inválido: mostrar error y repetir
5. Si válido: proceder

Entrada: content_type, user input (string)
Salida: title = user input
Ejemplo: "The Poseidon Adventure"
Validación: Non-empty, reasonable length
Responsable: content_handler.get_title()

Etapa 4: Búsqueda en APIs

Ubicación: api_manager.py, función search_content()
Descripción: Buscar el contenido en la API apropiada basado en tipo
Acciones:
1. Router de APIs según content_type:
   - "film" → usar TMDb search_movie()
   - "series" → usar TMDb search_tv()
   - "anime" → usar Jikan search_anime()
   - "manga" → usar Jikan search_manga()
   - "book" → usar Google Books search_books()

2. Construir request HTTP:
   - Agregar query parameter (title)
   - Incluir API key de config.py
   - Set timeout 5 segundos
   - Max retries 3, con exponential backoff

3. Hacer request a API
4. Si falla: retry lógica
   - Esperar 1 segundo
   - Retry con backoff factor 1.5
   - Max 3 intentos total
5. Si todos fallan: mostrar error y volver a Etapa 3

6. Si éxito: parsear respuesta JSON
7. Extraer campos relevantes de cada resultado:
   - id (identificador en API)
   - title
   - year/release date
   - poster_path (path relativo, no URL)
   - overview/description
   - vote_average/rating

8. Limitar a máximo 5 resultados
9. Normalizar a estructura estándar JSON:
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

Entrada: content_type, title
Salida: List[dict] con 3-5 resultados normalizados
Retry Logic: Max 3 intentos, exponential backoff
Error handling: APIError, NoResultsError
Responsable: api_manager.search_content(), api_manager._search_*()

Etapa 5: Selección de Resultado

Ubicación: content_handler.py, función select_from_results()
Descripción: El usuario elige cuál de los resultados es el que desea reseñar
Acciones:
1. Mostrar resultados formateados y bonitos:
   Search results for "The Poseidon Adventure":
   1. The Poseidon Adventure (1972) - Rating: 7.1/10
   2. Poseidon (2006) - Rating: 6.3/10
   3. The Poseidon Adventure (TV) (1979) - Rating: 6.8/10
   ...
   Which one did you watch? (1-5):

2. Leer selección del usuario (número 1-5)
3. Validar:
   - Es un número
   - Está en rango 1 a len(results)
4. Si inválido: error y repetir
5. Si válido: extraer resultado seleccionado
6. Proceder con selected_result (objeto completo del paso anterior)

Entrada: results (List[dict])
Salida: selected_result (dict con datos del resultado elegido), api_id (ej: "tmdb_551")
Responsable: content_handler.select_from_results()

Etapa 6: Obtención de Datos Completos

Ubicación: api_manager.py, función fetch_complete_data()
Descripción: Con el contenido seleccionado, hacer segundo request para obtener datos completos y enriquecidos
Acciones:
1. Usar el ID obtenido en Etapa 5
2. Hacer segundo request a API con datos completos:
   - TMDb: GET /movie/{id}?api_key=...&append_to_response=credits,reviews
   - Jikan: GET /anime/{id}/full
   - Google Books: GET /volumes/{id}

3. Obtener información adicional:
   - Créditos: director/autores, actores, productoras
   - Géneros
   - Runtime/páginas
   - Presupuesto/revenue (si aplicable)
   - Calificación de la plataforma

4. Descargar poster:
   - Obtener poster_path de respuesta
   - Construir URL completa: https://image.tmdb.org/t/p/w500{poster_path}
   - Descargar imagen a data/posters/
   - Nombres de archivo: sanitizar título y agregar extensión
   - Guardar ruta local en estructura

5. Preprocesar según content_type (ver Etapa 6b)

Entrada: content_type, api_id del resultado seleccionado
Salida: api_data normalizado con campos estándar
Responsable: api_manager.fetch_complete_data()

Etapa 6b: Preprocesamiento y Normalización

Ubicación: preprocessing/*.py
Descripción: Transformar datos específicos de cada API a esquema estándar
Acciones por content_type:

Si Film (preprocessing/tmdb_preprocessor.py):
1. Extraer y mapear campos:
   - id → api_id (con prefijo "tmdb_")
   - title, original_title, year
   - overview → description
   - vote_average → api_rating
   - director (de credits.crew)
   - actors (de credits.cast, primeros 5)
   - genres (array → JSON string)
   - runtime (minutos)
   - release_date
   - budget, revenue (si disponibles)
   - production_companies (JSON)
   - imdb_id (si disponible)
   - poster_url, poster_local_path

2. Validar campos requeridos
3. Crear estructura normalizada

Si Series (preprocessing/tmdb_preprocessor.py):
1. Igual a film, pero:
   - Agregar seasons, episodes, series_status
   - Episode runtime vs season runtime

Si Anime (preprocessing/jikan_preprocessor.py):
1. Mapear campos Jikan:
   - mal_id → api_id ("jikan_{id}_anime")
   - title, title_english, title_japanese
   - aired.from → year
   - synopsis → description
   - score → api_rating
   - studios (array)
   - episodes, status
   - genres
   - aired_string → release_date

Si Manga (preprocessing/jikan_preprocessor.py):
1. Mapear campos Jikan:
   - mal_id → api_id ("jikan_{id}_manga")
   - chapters, volumes
   - authors
   - status (publishing)

Si Book (preprocessing/googlebooks_preprocessor.py):
1. Mapear campos Google Books:
   - id → api_id ("googlebooks_{id}")
   - volumeInfo.title, subtitle, authors
   - publishedDate → year
   - description
   - averageRating → api_rating
   - pageCount
   - ISBN

Salida: api_data (dict normalizado)
Responsable: preprocessing/*.py

Resultado Final de Etapa 6:
api_data = {
  "content_type": "film",
  "source_api": "tmdb",
  "api_id": "tmdb_551",
  "title": "The Poseidon Adventure",
  "original_title": "The Poseidon Adventure",
  "year": 1972,
  "poster_url": "https://image.tmdb.org/t/p/w500/...",
  "poster_local_path": "data/posters/the_poseidon_adventure.jpg",
  "description": "When their ocean liner capsizes...",
  "api_rating": 7.095,
  "director": "Ronald Neame",
  "runtime": 117,
  "genres": ["Adventure", "Drama", "Thriller"],
  "release_date": "1972-12-13",
  "budget": 7000000,
  "production_companies": ["20th Century Fox"],
  ...
}

Etapa 7: Presentación al Usuario

Ubicación: content_handler.py, función display_content_details()
Descripción: Mostrar la información enriquecida del contenido para confirmación
Acciones:
1. Mostrar header formateado:
   THE POSEIDON ADVENTURE (1972)
   Película | Drama, Thriller, Adventure

2. Mostrar poster (ASCII art o ruta)
3. Mostrar metadata:
   Director: Ronald Neame
   Runtime: 117 minutes
   Public rating: 7.1/10
   Release date: 1972-12-13

4. Mostrar descripción (primeras 3 líneas, truncado si necesario)
5. Mostrar mensaje confirmación:
   Ready to review this? (y/n):

6. Leer respuesta
7. Si no: volver a Etapa 3
8. Si sí: proceder a Etapa 8

Entrada: api_data
Salida: User confirms o regresa
Responsable: content_handler.display_content_details()

Etapa 8: Selección de Tipo de Review

Ubicación: content_handler.py, función choose_review_type()
Descripción: El usuario elige si quiere hacer una evaluación analítica detallada o rápida/subjetiva
Acciones:
1. Mostrar opciones:
   How do you want to rate this content?

   1. ANALYTIC (Structured ratings)
      Rate different dimensions with automatic score calculation
      Typical time: 3-5 minutes
      Better for: Deep analysis, detailed comparison

   2. SUBJECTIVE (Overall score)
      Just give one overall rating
      Typical time: 10 seconds
      Better for: Quick reviews, casual content

   Which option? (1 or 2):

2. Leer selección
3. Validar (1 o 2)
4. Si inválido: repetir
5. Si válido: retornar "analytic" o "subjective"

Entrada: Nada (decision del usuario)
Salida: review_type = "analytic" | "subjective"
Responsable: content_handler.choose_review_type()

Etapa 9A: Captura de Rating Analítico

Ubicación: content_handler.py, función get_analytic_ratings()
Descripción: Para reviews analíticas, capturar rating de cada dimensión con pesos automáticos
Acciones:
1. Obtener pesos para este content_type de config.py:
   ANALYTIC_WEIGHTS["film"] = {
     "direction": 0.20,
     "writing": 0.20,
     "acting": 0.15,
     "technical": 0.15,
     "emotional_impact": 0.30
   }

2. Para cada dimensión, preguntar:
   Direction (20% weight) - How well was it directed? (0-10):
   [Usuario ingresa: 8]
   
   Writing (20% weight) - Quality of screenplay/story? (0-10):
   [Usuario ingresa: 7]
   
   Acting (15% weight) - Quality of performances? (0-10):
   [Usuario ingresa: 8]
   
   Technical (15% weight) - Cinematography, sound, VFX? (0-10):
   [Usuario ingresa: 9]
   
   Emotional Impact (30% weight) - How did it make you feel? (0-10):
   [Usuario ingresa: 9]

3. Validar cada rating:
   - Es número
   - Está entre 0-10
   Si inválido: pedir de nuevo

4. Calcular final_score automáticamente:
   final_score = (8 × 0.20) + (7 × 0.20) + (8 × 0.15) + (9 × 0.15) + (9 × 0.30)
               = 1.6 + 1.4 + 1.2 + 1.35 + 2.7
               = 8.25

5. Retornar estructura:
   analytic_ratings = {
     "direction": 8,
     "writing": 7,
     "acting": 8,
     "technical": 9,
     "emotional_impact": 9,
     "final_score": 8.25
   }

Entrada: content_type
Salida: analytic_ratings dict con final_score calculado
Responsable: content_handler.get_analytic_ratings()

Etapa 9B: Captura de Rating Subjetivo

Ubicación: content_handler.py, función get_subjective_rating()
Descripción: Para reviews subjetivas, capturar un único rating global
Acciones:
1. Mostrar prompt:
   What's your overall rating?
   How much did you enjoy it? (0-10):

2. Leer input del usuario
3. Validar:
   - Es número
   - Está entre 0-10
4. Si inválido: repetir
5. Si válido: retornar
   subjective_rating = {
     "overall_score": 8
   }

Entrada: Nada (decision del usuario)
Salida: subjective_rating dict
Responsable: content_handler.get_subjective_rating()

Etapa 10: Captura de Datos Comunes

Ubicación: content_handler.py, función get_common_review_data()
Descripción: Capturar datos adicionales que aplican a ambos tipos de review
Acciones (en orden):

1. Review Text (opcional):
   Write your review (press Enter to skip):
   [Usuario puede escribir múltiples líneas]
   review_text = input o None

2. Would Rewatch?
   Would you watch this again? (y/n):
   [User: y]
   would_rewatch = True

3. Watch Context:
   Where did you watch? (cinema/home_tv/streaming/other):
   [User: home_tv]
   watch_context = "home_tv"

4. Status:
   Status? (visto/en_progreso/pendiente/dropped) [default: visto]:
   [User: Enter para default]
   status = "visto"

5. Retornar estructura:
   common_data = {
     "review_text": "Great classic adventure film...",
     "would_rewatch": True,
     "watch_context": "home_tv",
     "status": "visto"
   }

Entrada: Nada (inputs del usuario)
Salida: common_data dict
Responsable: content_handler.get_common_review_data()

Etapa 11: Fusión de Datos

Ubicación: data_fusion.py, función merge_all_data()
Descripción: Combinar todos los componentes (API data + ratings + notas) en estructura final
Acciones:
1. Recibir 4 componentes:
   - api_data (de Etapa 6)
   - review_type (de Etapa 8)
   - ratings (analytic_ratings o subjective_rating de Etapa 9)
   - common_data (de Etapa 10)

2. Fusionar en diccionario final:
   final_data = {
     # API DATA (desempaquetado)
     "content_type": "film",
     "source_api": "tmdb",
     "api_id": "tmdb_551",
     "title": "The Poseidon Adventure",
     "year": 1972,
     ... (todos los campos de api_data)
     
     # REVIEW CONFIG
     "review_type": "analytic",
     
     # RATINGS
     "analytic_ratings": {
       "direction": 8,
       "writing": 7,
       "acting": 8,
       "technical": 9,
       "emotional_impact": 9,
       "final_score": 8.25
     },
     "subjective_rating": None,  # No usado en analytic
     
     # COMMON DATA
     "review_text": "Great classic adventure...",
     "would_rewatch": True,
     "watch_context": "home_tv",
     "status": "visto",
     
     # METADATA
     "date_added": "2026-01-30T17:45:30"
   }

3. Validar estructura:
   - Todos los campos requeridos presentes
   - Ratings válidos (0-10)
   - final_score calculado correctamente (si analytic)
   - api_id único (no vacío)

4. Retornar final_data validado

Entrada: api_data, review_type, ratings, common_data
Salida: final_data dict (validado y completo)
Responsable: data_fusion.merge_all_data()

Etapa 12: Chequeo de Duplicados

Ubicación: storage/sql_handler.py, función check_duplicate()
Descripción: Verificar si este contenido ya fue reseñado antes
Acciones:
1. Consultar BD:
   SELECT * FROM reviews WHERE api_id = ?
   [Parámetro: final_data["api_id"]]

2. Si existe:
   - Mostrar mensaje: "You already reviewed this. Update existing? (y/n):"
   - Si usuario dice sí: UPDATE la review existente
   - Si usuario dice no: ABORT el flujo (volver a Etapa 1)

3. Si no existe:
   - Proceder a Etapa 13

Entrada: final_data
Salida: Boolean (es duplicado o no)
Responsable: storage/sql_handler.check_duplicate()

Etapa 13: Guardar en SQL

Ubicación: storage/sql_handler.py, función save_review()
Descripción: Insertar el review completo en la base de datos SQLite
Acciones:
1. Convertir campos JSON complejos a strings:
   - genres: ["Adventure", "Drama"] → '["Adventure", "Drama"]'
   - analytic_ratings: {...} → JSON string
   - production_companies: [...] → JSON string

2. Preparar INSERT statement:
   INSERT INTO reviews (
     content_type, source_api, api_id, title, original_title, year,
     poster_url, poster_local_path, description, api_rating,
     director, runtime, genres, release_date, budget, revenue,
     production_companies, imdb_id,
     review_type, analytic_ratings, subjective_rating,
     review_text, would_rewatch, watch_context, status,
     date_added
   ) VALUES (?, ?, ?, ...)

3. Ejecutar insert con parámetros (evitar SQL injection)
4. Si error:
   - Unique constraint violation (api_id duplicado) → ya manejado en Etapa 12
   - Database locked → retry
   - Invalid data type → rollback y error al usuario
5. Si éxito:
   - Commit transaction
   - Obtener review_id (auto-increment)
   - Retornar review_id

Entrada: final_data
Salida: review_id (auto-increment)
Error handling: SQLError, ValidationError
Responsable: storage/sql_handler.save_review()

Etapa 14: Exportar a JSON

Ubicación: storage/json_handler.py, función export_to_json()
Descripción: Guardar una copia JSON del review para portabilidad y backups
Acciones:
1. Convertir final_data a JSON string con indentación:
   json.dumps(final_data, indent=2, ensure_ascii=False)

2. Generar nombre de archivo:
   Opción A: review_{titulo_sanitizado}_{fecha}.json
   Ejemplo: review_The_Poseidon_Adventure_2026-01-30.json
   
   Opción B: review_{id}.json
   Ejemplo: review_001.json

3. Crear ruta completa:
   data/exports/review_The_Poseidon_Adventure_2026-01-30.json

4. Crear directorios si no existen (mkdir -p)
5. Escribir archivo en disco
6. Retornar filepath

Entrada: final_data, review_id
Salida: filepath (string)
Responsable: storage/json_handler.export_to_json()

Etapa 15: Mensaje de Éxito y Continuación

Ubicación: main.py, content_handler.display_success_message()
Descripción: Mostrar confirmación de éxito y permitir siguientes acciones
Acciones:
1. Mostrar mensaje formateado:
   REVIEW SAVED SUCCESSFULLY!
   
   Title: The Poseidon Adventure (1972)
   Type: Film
   Rating system: Analytic
   Your score: 8.25/10
   Status: Visto
   
   Saved to:
   - SQLite database (ID: 1)
   - JSON export: data/exports/review_The_Poseidon_Adventure_2026-01-30.json

2. Mostrar menú de continuación:
   What next?
   1. Add another review
   2. View all reviews
   3. Search reviews
   4. Exit

3. Leer selección del usuario
4. Si 1: volver a Etapa 2
5. Si 2: mostrar lista de reviews (feature future)
6. Si 3: búsqueda (feature future)
7. Si 4: Exit gracefully

Entrada: review_id, final_data
Salida: Siguiente acción del usuario
Responsable: content_handler.display_success_message()

Ciclo Completo

El ciclo completo (Etapa 1 → 15) forma el "happy path" del sistema. Desde el punto de vista del usuario:

1. Inicia aplicación
2. Elige "Add new review"
3. Selecciona tipo de contenido
4. Ingresa título
5. Elige de resultados de búsqueda
6. Valida información
7. Elige tipo de rating
8. Ingresa ratings (5 dimensiones o 1 score)
9. Ingresa datos comunes (reseña, contexto, estado)
10. Confirma y guarda
11. Ve confirmación de éxito
12. Puede agregar otro review o salir

Tiempo estimado: 3-5 minutos por review (analytic) o 30-60 segundos (subjective)

Error Handling y Recovery

Si usuario comete error en cualquier Etapa:
- Etapa 2: selecciona tipo inválido → mostrar opciones válidas, repetir
- Etapa 3: ingresa título vacío → mostrar error, repetir
- Etapa 4: API no responde → reintentar 3 veces, luego error
- Etapa 5: selecciona resultado inválido → repetir pregunta
- Etapa 9: ingresa rating fuera de rango → repetir pregunta
- Etapa 12: review ya existe → ofrecer actualizar o cancelar

En todos los casos: mantener al usuario en el loop, no perder datos, permitir cancelación limpia.
Hay que añadir además, que hay 15 etapas y 9 módulos en la arquitectura del programa. Queda aclarar que estas 15 etapas se distribuyen en los 9 modulos.
