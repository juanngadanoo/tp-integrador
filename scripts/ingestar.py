"""Corre la ingesta completa: corpus -> chunks -> embeddings -> Chroma.

Uso (desde la raíz del repo, con el venv activado):
    python scripts/ingestar.py
"""

import time

from tp.config import settings
from tp.ingesta.pipeline import cargar_corpus, pipeline_ingesta
from tp.recuperacion.buscador import abrir_coleccion, indexar


def main():
    documentos = cargar_corpus(settings.corpus_dir)
    if not documentos:
        raise SystemExit(f"No hay documentos .md/.txt en {settings.corpus_dir}. ¿Ya bajaste el corpus?")
    print(f"{len(documentos)} documentos encontrados en {settings.corpus_dir}")

    t0 = time.time()
    registros = pipeline_ingesta(documentos)
    print(f"{len(registros)} chunks embebidos en {time.time() - t0:.1f} s")

    total = indexar(abrir_coleccion(), registros)
    print(f"Índice listo: {total} chunks en {settings.chroma_dir} (colección '{settings.chroma_coleccion}')")


if __name__ == "__main__":
    main()
