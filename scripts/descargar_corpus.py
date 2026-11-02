"""Descarga el corpus del TP: la JavaScript Guide de MDN (solo los index.md, sin imágenes).

Uso (desde la raíz del repo, con el venv activado):
    python scripts/descargar_corpus.py

Fuente: https://github.com/mdn/content/tree/main/files/en-us/web/javascript/guide
Licencia: CC-BY-SA 2.5, © Mozilla Contributors. Hay que mantener la atribución
en cualquier material que se comparta fuera de la cursada.

Usa solo la biblioteca estándar de Python (no hace falta instalar nada) y se puede
correr varias veces: pisa los archivos con la versión actual de MDN.

La lista de documentos es FIJA a propósito (relevada el 02/11/2026): si MDN agrega
páginas, el corpus no cambia solo, y los resultados de la evaluación (Clase 8)
siguen siendo comparables entre corridas. Para sumar un documento, agregalo a DOCUMENTOS.
"""

import urllib.request

from tp.config import settings

BASE = "https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/javascript/guide"

DOCUMENTOS = [
    "agent_communication_and_coordination/index.md",
    "closures/index.md",
    "control_flow_and_error_handling/index.md",
    "data_structures/index.md",
    "enumerability_and_ownership_of_properties/index.md",
    "equality_comparisons_and_sameness/index.md",
    "expressions_and_operators/index.md",
    "functions/index.md",
    "grammar_and_types/index.md",
    "index.md",
    "indexed_collections/index.md",
    "inheritance_and_the_prototype_chain/index.md",
    "internationalization/index.md",
    "introduction/index.md",
    "iterators_and_generators/index.md",
    "keyed_collections/index.md",
    "language_overview/index.md",
    "loops_and_iteration/index.md",
    "memory_management/index.md",
    "meta_programming/index.md",
    "modules/index.md",
    "numbers_and_strings/index.md",
    "regular_expressions/assertions/index.md",
    "regular_expressions/character_classes/index.md",
    "regular_expressions/cheatsheet/index.md",
    "regular_expressions/groups_and_backreferences/index.md",
    "regular_expressions/index.md",
    "regular_expressions/quantifiers/index.md",
    "representing_dates_times/index.md",
    "resource_management/index.md",
    "typed_arrays/index.md",
    "using_classes/index.md",
    "using_promises/index.md",
    "working_with_objects/index.md",
]


def main():
    destino = settings.corpus_dir
    print(f"Descargando {len(DOCUMENTOS)} documentos de MDN en {destino}\n")

    for ruta in DOCUMENTOS:
        with urllib.request.urlopen(f"{BASE}/{ruta}", timeout=30) as resp:
            texto = resp.read().decode("utf-8")
        # El index.md de la raíz de la guía queda como `_portada/index.md`
        # para no mezclarlo con data/corpus/LEEME.md.
        archivo = destino / (ruta if "/" in ruta else f"_portada/{ruta}")
        archivo.parent.mkdir(parents=True, exist_ok=True)
        archivo.write_text(texto, encoding="utf-8")
        print(f"  ok  {archivo.relative_to(destino).as_posix()}  ({len(texto):,} caracteres)")

    print(f"\nListo: {len(DOCUMENTOS)} documentos en {destino}")


if __name__ == "__main__":
    main()
