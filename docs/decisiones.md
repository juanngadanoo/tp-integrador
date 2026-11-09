# Registro de decisiones técnicas

## Clase 1 — Matriz de selección de modelos

TODO: completar la plantilla de `clase-01-fundamentos-llms/actividad.md` y responder las 3 preguntas guía.
En la columna de Gemini, justificá por qué lo usás para generación Y embeddings.

## 2026-10-20 · Modelo de embeddings: `gemini-embedding-001` a 768 dimensiones

- **Alternativas**: `text-embedding-004` (el que trae el notebook de la cátedra) y `gemini-embedding-2` (multimodal).
- **Por qué**: TODO (vos). Pista: qué soporta cada uno de `task_type`; qué necesitamos (solo texto o también imágenes); qué cambia en costo y almacenamiento con 768 vs. 3072 dimensiones.
- **Consecuencia**: con menos de 3072 dimensiones, `gemini-embedding-001` devuelve vectores sin normalizar. Por eso se normalizan en `embeddings.py`.

## Clase 4 — Estrategia de chunking

- **Limpieza (MDN)**: se borran la ficha técnica (salvo `title:`), los botones de navegación y las marcas del sitio web; los links `{{jsxref(...)}}` se reemplazan por su texto visible. Por qué: lo que se repite en todas las páginas hace que los chunks se parezcan entre sí.
- **Chunking**: por caracteres, 800 con solapamiento 120 (15%). Alternativa: por párrafos (máx. 800 o 1200).
- **Por qué**: el corpus tiene bloques de código de hasta 10.400 caracteres; por párrafos, 24 chunks pasarían de 1500. 800 alcanza para una explicación + su ejemplo de código.
- **Cómo lo medí**: cantidad y tamaño de chunks sobre el corpus real (1118 chunks). Pendiente validar con búsquedas en la Clase 8.

## Clase 5 — Umbral de similitud

Con el resultado arrojado en la celda 11 (propia) de la clase 04 , tomé la decisión de que el umbral de similitud debe parametrizarse por encima de 0.56, dado que con mi proveedor (google) un umbral de 0.5 dejaría pasar cualquier cosa.

Valor provisorio: hay que recalibrarlo en la Clase 5 con la configuración real del TP (768 dimensiones y task_type)