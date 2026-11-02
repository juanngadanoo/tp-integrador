"""Checkpoint 4 — pipeline de ingesta. Criterios de éxito de la Clase 4."""

import dataclasses

from conftest import embedding_falso
from tp.ingesta.chunking import Chunk
from tp.ingesta.pipeline import pipeline_ingesta

TEXTO_LARGO = "\n\n".join(
    f"Sección {i}. La API permite configurar credenciales mediante variables de entorno. "
    f"Para el parámetro número {i} se recomienda revisar la documentación oficial." for i in range(40)
)
DOCS = {
    "guia_config": (TEXTO_LARGO, "guia_config.md"),
    "faq": ("¿Qué es un token?\n\n\n\nUn token es un fragmento de texto.", "faq.md"),
}


class EmbedEspia:
    def __init__(self):
        self.llamadas = 0

    def __call__(self, textos):
        self.llamadas += 1
        return [embedding_falso(t) for t in textos]


def test_chunk_tiene_fuente_y_fecha():
    campos = {f.name for f in dataclasses.fields(Chunk)}
    assert {"fuente", "fecha_ingesta"} <= campos


def test_estructura_de_salida():
    regs = pipeline_ingesta(DOCS, embed_fn=EmbedEspia())
    assert len(regs) > 2
    for r in regs:
        assert {"chunk_id", "texto", "vector", "documento_id", "posicion", "fuente"} <= r.keys()


def test_chunks_menores_a_1500_caracteres():
    assert all(len(r["texto"]) < 1500 for r in pipeline_ingesta(DOCS, embed_fn=EmbedEspia()))


def test_trazabilidad_sin_ambiguedad():
    regs = pipeline_ingesta(DOCS, embed_fn=EmbedEspia())
    ids = [r["chunk_id"] for r in regs]
    assert len(ids) == len(set(ids)), "chunk_id repetido"
    for r in regs:
        assert r["chunk_id"].startswith(r["documento_id"])
        assert r["fuente"] == DOCS[r["documento_id"]][1]


def test_vector_corresponde_a_su_texto():
    for r in pipeline_ingesta(DOCS, embed_fn=EmbedEspia()):
        assert r["vector"] == embedding_falso(r["texto"]), "Se mezclaron vectores entre chunks"


def test_embebe_en_batch_no_de_a_uno():
    espia = EmbedEspia()
    pipeline_ingesta(DOCS, embed_fn=espia)
    assert espia.llamadas == 1


def test_aplica_limpieza():
    regs = [r for r in pipeline_ingesta(DOCS, embed_fn=EmbedEspia()) if r["documento_id"] == "faq"]
    assert all("\n\n\n" not in r["texto"] for r in regs)
