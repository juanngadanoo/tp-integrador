# Registro de decisiones técnicas

## Clase 1 — Matriz de selección de modelos

- **Elección**: Gemini para las dos cosas: `gemini-3.5-flash-lite` (generación) y `gemini-embedding-001` (embeddings).
- **Alternativa evaluada**: Llama 3.2 3B vía Ollama (modelo abierto, corre en la propia PC).
- **Por qué**: rápido (~1 s medido), barato (línea Flash-lite) y con salida estructurada, tool calling y streaming. Un solo proveedor y una sola API key para todo.
- **Cuándo cambiaría**: si el corpus fuera confidencial, a un modelo abierto en servidores propios (los datos no salen de la organización).
- **Detalle**: matriz completa y preguntas guía en `notebooks_clases/actividad.md`.


## 2026-10-20 · Modelo de embeddings: `gemini-embedding-001` a 768 dimensiones

- **Alternativas**: `text-embedding-004` (el que trae el notebook de la cátedra) y `gemini-embedding-2` (multimodal).
- **Por qué**: el corpus es solo texto, así que no hace falta un modelo multimodal como `gemini-embedding-2`. Frente a `text-embedding-004`, es un modelo más nuevo y permite elegir la dimensión (768, 1536 o 3072). Con 768 el índice ocupa 4 veces menos que con 3072 y la búsqueda es más rápida, con poca pérdida de calidad. La dimensión no cambia lo que cobra Google (se paga por el texto enviado), sí el espacio que ocupa el índice.
- **Consecuencia**: con menos de 3072 dimensiones, `gemini-embedding-001` devuelve vectores sin normalizar. Por eso se normalizan en `embeddings.py`.

## Clase 4 — Estrategia de chunking

- **Limpieza (MDN)**: se borran la ficha técnica (salvo `title:`), los botones de navegación y las marcas del sitio web; los links `{{jsxref(...)}}` se reemplazan por su texto visible. Por qué: lo que se repite en todas las páginas hace que los chunks se parezcan entre sí.
- **Chunking**: por caracteres, 800 con solapamiento 120 (15%). Alternativa: por párrafos (máx. 800 o 1200).
- **Por qué**: el corpus tiene bloques de código de hasta 10.400 caracteres; por párrafos, 24 chunks pasarían de 1500. 800 alcanza para una explicación + su ejemplo de código.
- **Cómo lo medí**: cantidad y tamaño de chunks sobre el corpus real (1118 chunks). Pendiente validar con búsquedas en la Clase 8.

## Clase 5 — Umbral de similitud

- **Valor elegido**: 0.6 (reemplaza el provisorio de 0.56).
- **Cómo lo medí**: 4 preguntas reales sobre el corpus de MDN y 2 fuera de dominio, con el índice real (768 dimensiones, `RETRIEVAL_QUERY`). Peor resultado bueno: 0.726; mejor fuera de dominio: 0.516.
- **Por qué no 0.3 (ejemplo de la notebook)**: con Gemini, hasta los textos sin relación dan alrededor de 0.5; 0.3 no filtraría nada.
- **Riesgo**: el puntaje cambia con la redacción de la pregunta; si se cortan respuestas válidas, bajarlo. Revalidar en la Clase 8.

## Clase 5 — Ingesta incremental por documento

- **Problema**: el plan gratuito de Gemini permite 100 embeddings por minuto y 1000 por día; el corpus tiene 1118 chunks.
- **Solución**: `ingestar.py` guarda en Chroma después de cada documento y saltea los ya indexados; ante un 429 se espera un minuto.
- **Consecuencia**: con el plan gratuito, la primera ingesta lleva dos días; si cambia el corpus o el chunking, hay que borrar `data/chroma` y re-ingestar.
- **Resolución**: con una API key de nivel 2 (tier pago) la ingesta completa entró en una sola corrida; la ingesta incremental queda como protección ante cortes.
