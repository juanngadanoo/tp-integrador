"""Pipeline de ingesta — CHECKPOINT CLASE 4.

Recordá la regla de la Clase 4, sección 7: acá NO va nada de búsqueda.

Tests: pytest tests/test_cp4_ingesta.py -v
"""

from pathlib import Path

from tp.ingesta.chunking import Chunk, chunking_por_caracteres, chunking_por_parrafos  # noqa: F401
from tp.ingesta.embeddings import embed_documentos
from tp.ingesta.limpieza import limpiar_texto  # noqa: F401

# Estrategia: por caracteres, 800 con solapamiento 120 (15%). El corpus (34 páginas de MDN) tiene párrafos
# cortos pero también bloques de código de hasta 10.400 caracteres: por párrafos, 24 chunks pasarían de 1500.
# 800 alcanza para una explicación + su ejemplo de código sin mezclar secciones.
TAMANO_CHUNK = 800
SOLAPAMIENTO = 120

def cargar_corpus(carpeta: Path) -> dict[str, tuple[str, str]]:
    """Lee los .md/.txt de la carpeta. Devuelve {documento_id: (texto_crudo, fuente)}.
    Infraestructura: ya está hecho. Si el corpus viene en PDF/HTML, se agrega acá."""
    documentos = {}
    for archivo in sorted(carpeta.rglob("*")):
        if archivo.suffix.lower() in {".md", ".txt"} and archivo.name != "LEEME.md":
            doc_id = archivo.relative_to(carpeta).with_suffix("").as_posix().replace("/", "__")
            documentos[doc_id] = (archivo.read_text(encoding="utf-8"), archivo.relative_to(carpeta).as_posix())
    return documentos

def pipeline_ingesta(documentos: dict[str, tuple[str, str]], embed_fn=embed_documentos) -> list[dict]:
    """documentos: {documento_id: (texto_crudo, fuente)}.
    Devuelve una lista de dicts {chunk_id, texto, vector, documento_id, posicion, fuente}.

    `embed_fn` se puede reemplazar: los tests le pasan una función falsa para no gastar API.
    """
    # 1. Limpiar -> cortar -> etiquetar
    todos_los_chunks = []
    for documento_id, (texto_crudo, fuente) in documentos.items():
        texto_limpio = limpiar_texto(texto_crudo)
        textos = chunking_por_caracteres(texto_limpio, TAMANO_CHUNK, SOLAPAMIENTO)
        for posicion, texto in enumerate(textos):
            todos_los_chunks.append(Chunk(texto=texto, documento_id=documento_id, posicion=posicion, fuente=fuente))

    # 2. Embeber TODOS los textos en una sola llamada (batch)
    vectores = embed_fn([c.texto for c in todos_los_chunks])

    # 3. Emparejar cada ficha con su vector
    registros = []
    for chunk, vector in zip(todos_los_chunks, vectores):
        registros.append({
            "chunk_id": chunk.chunk_id,
            "texto": chunk.texto,
            "vector": vector,
            "documento_id": chunk.documento_id,
            "posicion": chunk.posicion,
            "fuente": chunk.fuente,
            "fecha_ingesta": chunk.fecha_ingesta,
        })
    return registros
