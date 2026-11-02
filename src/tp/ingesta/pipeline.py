"""Pipeline de ingesta — CHECKPOINT CLASE 4 (lo escribís vos).

Recordá la regla de la Clase 4, sección 7: acá NO va nada de búsqueda.

Tests: pytest tests/test_cp4_ingesta.py -v
"""

from pathlib import Path

from tp.ingesta.chunking import Chunk, chunking_por_caracteres, chunking_por_parrafos  # noqa: F401
from tp.ingesta.embeddings import embed_documentos
from tp.ingesta.limpieza import limpiar_texto  # noqa: F401

# TODO (vos): justificá acá, en 2-3 líneas, la estrategia y los valores elegidos PARA ESTE CORPUS.
# (Se completa cuando tengas el corpus real: depende de cómo estén escritos sus documentos.)
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
    # TODO (vos):
    # 1. Para cada documento: limpiar -> chunkear -> crear un Chunk por fragmento.
    # 2. Embeber TODOS los textos en una sola llamada a embed_fn (no uno por uno: ¿por qué?).
    # 3. Combinar cada Chunk con su vector y devolver la lista de dicts.
    raise NotImplementedError("Checkpoint 4: completá pipeline_ingesta")
