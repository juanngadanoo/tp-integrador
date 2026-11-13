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
    coleccion.upsert(
        ids=[r["chunk_id"] for r in registros],
        embeddings=[r["vector"] for r in registros],
        documents=[r["texto"] for r in registros],
        metadatas=[{
            "documento_id": r["documento_id"],
            "posicion": r["posicion"],
            "fuente": r["fuente"],
            "fecha_ingesta": r.get("fecha_ingesta", ""),
        } for r in registros],
    )
    return coleccion.count()



def buscar(consulta: str, coleccion, k: int = 3, umbral_similitud: float = 0.0,
           where: dict | None = None, embed_fn=embed_consulta) -> list[dict]:
    """Top-k chunks para `consulta`, descartando los que estén por debajo de `umbral_similitud`.
    Devuelve una lista de {chunk_id, texto, similitud, documento_id, posicion, fuente},
    ordenada de mayor a menor similitud."""
    vector = embed_fn(consulta)
    res = coleccion.query(query_embeddings=[vector], n_results=k, where=where)

    resultados = []
    for chunk_id, texto, meta, distancia in zip(
        res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0]
    ):
        similitud = 1 - distancia
        if similitud >= umbral_similitud:
            resultados.append({
                "chunk_id": chunk_id,
                "texto": texto,
                "similitud": similitud,
                "documento_id": meta["documento_id"],
                "posicion": meta["posicion"],
                "fuente": meta["fuente"],
            })
    return resultados

