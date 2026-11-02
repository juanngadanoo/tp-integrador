# Registro de decisiones técnicas

Cada vez que elegís algo (modelo, tamaño de chunk, umbral, framework), anotalo acá con el **porqué**.
En la Clase 12 esto se convierte casi directo en la sección "Decisiones técnicas" del informe,
y es lo que te van a preguntar en la exposición.

Formato: fecha · decisión · alternativas consideradas · por qué · cómo lo medí (si aplica).

---

## Clase 1 — Matriz de selección de modelos

TODO (vos): completar la plantilla de `clase-01-fundamentos-llms/actividad.md` y responder las 3 preguntas guía.
En la columna de Gemini, justificá por qué lo usás para generación Y embeddings.

## 2026-10-20 · Modelo de embeddings: `gemini-embedding-001` a 768 dimensiones

- **Alternativas**: `text-embedding-004` (el que trae el notebook de la cátedra) y `gemini-embedding-2` (multimodal).
- **Por qué**: TODO (vos). Pista: qué soporta cada uno de `task_type`; qué necesitamos (solo texto o también imágenes); qué cambia en costo y almacenamiento con 768 vs. 3072 dimensiones.
- **Consecuencia**: con menos de 3072 dimensiones, `gemini-embedding-001` devuelve vectores sin normalizar. Por eso se normalizan en `embeddings.py`.

## Clase 4 — Estrategia de chunking

TODO (vos), cuando tengas el corpus: tamaño, overlap, por caracteres o por párrafos, y por qué para ESTE corpus.

## Clase 5 — Umbral de similitud

TODO (vos): qué valor elegiste y cómo lo calibraste (qué similitud dan las consultas buenas y cuál las de fuera de dominio).
