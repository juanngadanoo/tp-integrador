"""Embeddings con Google (Clase 4, sección 3), actualizado al modelo vigente.

Diferencias con la función `embed_google` del notebook de la cátedra:
- Modelo `gemini-embedding-001` (el notebook usa `text-embedding-004`).
- `task_type`: RETRIEVAL_DOCUMENT para el corpus y RETRIEVAL_QUERY para las consultas.
  Es el mismo concepto que `search_document` / `search_query` de Cohere en la Clase 5.
- Batching: no manda todo el corpus en una sola request.
- Normalización: con dimensión < 3072, gemini-embedding-001 NO devuelve vectores
  normalizados, así que los normalizamos acá para que la similitud coseno sea correcta.

Preguntas que te pueden hacer en la defensa sobre este archivo:
  ¿Por qué distinto task_type para documento y consulta? ¿Por qué normalizar?
  ¿Qué pasa si cambiás EMBEDDING_DIM con el índice ya construido?
"""

import numpy as np

from tp.config import settings

TAMANO_LOTE = 50

_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=settings.google_api_key)
    return _client


def _normalizar(vector: list[float]) -> list[float]:
    v = np.array(vector)
    norma = np.linalg.norm(v)
    return (v / norma).tolist() if norma else v.tolist()


def embed_google(textos: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Devuelve un vector normalizado por cada texto, en el mismo orden."""
    from google.genai import types

    if task_type not in {"RETRIEVAL_DOCUMENT", "RETRIEVAL_QUERY"}:
        raise ValueError(f"task_type inválido: {task_type}")

    client = _get_client()
    config = types.EmbedContentConfig(task_type=task_type, output_dimensionality=settings.embedding_dim)
    vectores: list[list[float]] = []
    for i in range(0, len(textos), TAMANO_LOTE):
        lote = textos[i:i + TAMANO_LOTE]
        resp = client.models.embed_content(model=settings.google_embedding_model_id,
                                           contents=lote, config=config)
        vectores.extend(_normalizar(e.values) for e in resp.embeddings)
    return vectores


def embed_documentos(textos: list[str]) -> list[list[float]]:
    return embed_google(textos, task_type="RETRIEVAL_DOCUMENT")


def embed_consulta(texto: str) -> list[float]:
    return embed_google([texto], task_type="RETRIEVAL_QUERY")[0]
