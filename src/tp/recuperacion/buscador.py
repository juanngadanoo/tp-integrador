"""Índice vectorial y buscador — CHECKPOINT CLASE 5.

`abrir_coleccion` es infraestructura (ya está). `indexar` y `buscar` los escribís vos.

Tests: pytest tests/test_cp5_buscador.py -v
"""

import chromadb

from tp.config import settings
from tp.ingesta.embeddings import embed_consulta


def abrir_coleccion(ruta=None, nombre=None):
    """Colección persistente de Chroma configurada con distancia coseno."""
    cliente = chromadb.PersistentClient(path=str(ruta or settings.chroma_dir))
    return cliente.get_or_create_collection(nombre or settings.chroma_coleccion,
                                            metadata={"hnsw:space": "cosine"})


def indexar(coleccion, registros: list[dict]) -> int:
    """Carga en Chroma la salida de pipeline_ingesta. Devuelve cuántos chunks quedaron indexados.
    Tiene que ser idempotente: correrlo dos veces con los mismos datos NO duplica chunks."""
    # TODO (vos): usar coleccion.upsert(ids=..., embeddings=..., documents=..., metadatas=...)
    #   metadatas: al menos documento_id, posicion y fuente.
    raise NotImplementedError("Checkpoint 5: completá indexar")


def buscar(consulta: str, coleccion, k: int = 3, umbral_similitud: float = 0.0,
           where: dict | None = None, embed_fn=embed_consulta) -> list[dict]:
    """Top-k chunks para `consulta`, descartando los que estén por debajo de `umbral_similitud`.
    Devuelve una lista de {chunk_id, texto, similitud, documento_id, posicion, fuente},
    ordenada de mayor a menor similitud."""
    # TODO (vos):
    # 1. Embeber la consulta con embed_fn (ya usa RETRIEVAL_QUERY).
    # 2. coleccion.query(query_embeddings=[...], n_results=k, where=where)
    # 3. Chroma devuelve DISTANCIA coseno, no similitud: ¿cómo convertís una en la otra?
    # 4. Filtrar por umbral y armar la lista de dicts.
    raise NotImplementedError("Checkpoint 5: completá buscar")
