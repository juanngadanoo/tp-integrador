# TP Final Integrador — Desarrollador de Agentes de IA (ITBA 2026)

Sistema RAG + agente con herramientas, expuesto vía FastAPI, sobre el corpus de documentación técnica de la cátedra.
Proveedor: **Google Gemini** (generación + embeddings).

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows 
pip install -r requirements.txt
pip install -e .                # registra el paquete `tp` para poder importarlo desde scripts y notebooks
copy .env.example .env          # y completá GOOGLE_API_KEY
```

## Uso

```bash
python scripts/descargar_corpus.py          # baja el corpus de MDN (una sola vez)
pytest -v                                   # tests de todos los checkpoints
python scripts/ingestar.py                  # corpus -> índice vectorial
python scripts/buscar.py "tu pregunta"      # prueba manual del buscador
```

## Estructura

```
src/tp/
  config.py                 configuración central (lee el .env)
  llm/base.py               LLMProvider + reintento estructurado
  llm/google.py             GoogleProvider                         [CP3 ✅]
  llm/factory.py            get_provider()
  clasificador.py           IntencionConsulta + clasificar()       [CP3 ✅]
  ingesta/limpieza.py       limpiar_texto                          [CP4 ✅]
  ingesta/chunking.py       chunking + dataclass Chunk             [CP4 ✅]
  ingesta/embeddings.py     embeddings Gemini (documento/consulta)
  ingesta/pipeline.py       cargar_corpus + pipeline_ingesta       [CP4 ✅]
  recuperacion/buscador.py  Chroma: indexar + buscar               [CP5 — TODO]
scripts/                    descargar_corpus.py, ingestar.py, buscar.py
tests/                      un archivo por checkpoint
data/corpus/                corpus: JavaScript Guide de MDN (34 páginas)
docs/decisiones.md          registro de decisiones técnicas -> base del informe final
```

## Estado de checkpoints

| Clase | Checkpoint | Estado |
|---|---|---|
| 1 | Matriz de selección de modelos | ✅ `notebooks_clases/actividad.md` + resumen en `docs/decisiones.md` |
| 2 | `LLMClient` con reintentos | ✅ hecho en notebook |
| 3 | `LLMProvider` + salida estructurada | ✅ `pytest tests/test_cp3_*` |
| 4 | Ingesta: limpieza, chunking, metadata | ✅ `pytest tests/test_cp4_ingesta.py` |
| 5 | Índice vectorial + buscador | ⬜ `pytest tests/test_cp5_buscador.py` |
| 6 | RAG end-to-end con citas | — |
| 7 | Casos fallidos diagnosticados | — |
| 8 | Dataset de evaluación + métricas | — |
| 9 | Herramienta externa con tool calling | — |
| 10 | Workflow con estado + aprobación humana | — |
| 11 | FastAPI + logging + seguridad | — |
| 12 | Integración, docs, diagrama, entrega | — |
