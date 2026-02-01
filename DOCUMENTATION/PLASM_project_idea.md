PLASM - Content Review Management System

Concepto Fundamental

PLASM (Películas, Libros, Anime, Series, Manga) es un sistema personal de gestión y análisis de reviews de contenido multimedia. Nace de la necesidad de consolidar en un único espacio lo que actualmente está fragmentado en plataformas como IMDb, Goodreads, Letterboxd, MyAnimeList y similares.

El problema original lo encontre durante el uso extensivo de estas aplicaciones: Quiero un espacio único donde poder comentar, evaluar y dar reseñas sin restricciones, sin depender de plataformas externas, y manteniendo control total sobre mis propios datos.




Objetivo Principal:

Crear un software amigable, robusto y extensible que permita al usuario:
- Registrar reviews de cualquier tipo de contenido sin limitaciones
- Evaluar contenido tanto de foaarma estructurada a base de preguntas que valoran respuestas objetivas como una manera rápida o subjetiva de forma overall
- Enriquecer automáticamente los datos mediante APIs públicas
- Almacenar información de forma persistente y portátil
- Analizar patrones en sus preferencias y consumo de contenido



Público Objetivo:

Consumidores intensivos de contenido multimedia con orientación analítica y data-driven que desean:
- Independencia de plataformas comerciales
- Control total sobre sus reviews y datos personales
- Flexibilidad en criterios de evaluación
- Capacidad de análisis posterior sobre sus propios patrones




Beneficios Clave:
Centralización: Un único punto de acceso para todos los tipos de contenido
Flexibilidad: Dos modos de rating (analítico y subjetivo) según el contexto
Enriquecimiento automático: Metadata, posters, descripciones desde APIs confiables
Portabilidad: Exportación en JSON, no vendor lock-in
Privacidad: Base de datos local, sin sincronización en cloud
Análisis: Fundación para futuras dashboards y visualizaciones



Visión futura y desarrollo de proyecto:

Fase 1 (actual): Que sea completamente funcional en terminal incluyendo todo el workflow necesario en python y sql. La fase 1 estará completa cuando al utilizar el programa pueda realizar una reseña entera y se guarde correctamente tanto en json como en mi base de datos.
Fase 2: Poder ser utilizado por cualquier otro usuario que no sea yo. Es decir, incluir una interfaz gráfica donde se conecte database y el propio programa y en la interfaz se visualicen las reviews.
Fase 3: Finalizar todas las ideas y hacer que sea completamente funcional sin mi soporte. Añadir herramientas para gestionar la base de datos como gráficos o contadores de cual es el género que más ha consumido, que contenido es el que más disfruta o el que más ha consumido.
Fase 4: Desarrollar app/web para que sea disponible para todo el mundo y dar un soporte para la base de datos qu sea a nivel global. Es decir, que todo el mundo pueda usarlo y todo el mundo pueda tener su base de datos de reviews. 
Fase 5: Incluir en redes sociales/newsletter e incluir soporte para el usuario y añadir herramientas que mejoren el entorno como wrap anual y escalarlo junto ads o hacer que el proyecto se retroalimente.



Diferenciadores frente a plataformas existentes:

IMDb/TMDB: Limitadas a films/series, no permite reviews personalizadas
Goodreads: Optimizada solo para libros
Letterboxd: Solo películas, aunque con buena comunidad
MyAnimeList: Solo anime/manga, interface desactualizada
PLASM: Unificado, local-first, totalmente personalizable, data-driven



Extensiones Potenciales:

Videojuegos: Integración con IGDB API
Podcasts: Integración con Spotify/Apple Podcasts APIs
Música: Integración con Last.fm o MusicBrainz
Cómics: Integración con Grand Comics Database
Documentales: Categorizados como subgrupo de films
Influencers/Streamers: Review de creadores de contenido
Eventos: Conciertos, obras de teatro, películas en cines




Estrategia de Datos:

Los datos se estructuran en tres capas:
1. Metadata enriquecida (desde APIs): información objetiva del contenido
2. Ratings estructurados: dimensiones ponderadas que varían por tipo
3. Notas personales: reseña libre, contexto de visualización, estado

Esta separación permite análisis granular en Phase 2 (ej: correlacionar quality de dirección con score final)

Casos de Uso Principales

Use case 1: Usuario ve una película y quiere registrarla inmediatamente
- Acceso rápido a review subjective (5 segundos)
- Captura de contexto (dónde vio, si la recomendaría)

Use case 2: Usuario analiza a fondo una obra maestra
- Review analytic con 5 dimensiones ponderadas
- Reseña detallada con notas personales
- Comparación histórica con otras obras del mismo director

Use case 3: Usuario analiza sus patrones
- Dashboard: géneros más valorados
- Timeline: evolución de ratings en el tiempo
- Correlaciones: ¿qué directores tienen mis scores más altos?
- Rankings: tier lists por género, director, año

Arquitectura Conceptual

La información fluye en una cadena clara:
1. Búsqueda y validación del contenido (APIs externas)
2. Captura de opinión del usuario (CLI input)
3. Normalización y fusión de datos (preprocessing)
4. Almacenamiento persistente (SQLite + JSON backups)
5. Análisis y visualización (futuro dashboard)

Cada etapa es independiente y modular, permitiendo evolución sin reescritura.

Principios de Diseño

Simplicidad: CLI intuitivo, flujo paso a paso
Exhaustividad: Sin datos perdidos, todo se registra
Flexibilidad: Usuario elige nivel de detalle por review
Extensibilidad: Nueva APIs y content types sin refactoring mayor
Integridad: Validación en cada punto, recuperación ante errores
Portabilidad: Formato estándar (JSON, SQLite), no propietario

Se busca que todos los modulos que se desarrollen en este proyecto sean fáciles y rápidos de entender dentro de lo posible para que se pueda escalar y desarrollar de una manera sencilla y correcta y sobre todo para la modificación de los modulos. Posiblemente, como se vaya a escalar el proyecto se necesita que los programas sean sencillos a la hora de implementar nuevos modulos.

Restricciones Iniciales (v1)

Monousuario: No hay multi-user, no hay sharing
Local: Base de datos en el equipo del usuario
CLI: No hay interfaz gráfica (fundación para futura web)
Batch: No hay real-time, no hay streaming
Offline-first: APIs son complementarias, no obligatorias

