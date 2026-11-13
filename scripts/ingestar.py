"""Corre la ingesta completa: corpus -> chunks -> embeddings -> Chroma.

Guarda en Chroma después de cada documento y saltea los que ya están indexados:
si se corta (por ejemplo, por el límite diario de 1000 embeddings del plan gratuito
de Google), se vuelve a correr y sigue desde donde quedó.
Si cambiás el corpus o el chunking, borrá la carpeta data/chroma y volvé a correrlo.

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

    coleccion = abrir_coleccion()
    t0 = time.time()
    for documento_id, contenido in documentos.items():
        if coleccion.get(where={"documento_id": documento_id}, limit=1)["ids"]:
            print(f"  ya indexado, se saltea: {documento_id}")
            continue
        try:
            registros = pipeline_ingesta({documento_id: contenido})
        except Exception as err:
            print(f"\nSe cortó en {documento_id}: {str(err)[:150]}")
            print(f"Quedaron {coleccion.count()} chunks guardados. Volvé a correr el script más tarde: sigue desde acá.")
            return
        total = indexar(coleccion, registros)
        print(f"  {documento_id}: {len(registros)} chunks (total en el índice: {total})")

    print(f"Índice listo: {coleccion.count()} chunks en {settings.chroma_dir} "
        f"(colección '{settings.chroma_coleccion}') en {time.time() - t0:.1f} s")


if __name__ == "__main__":
    main()
