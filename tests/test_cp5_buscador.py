"""Checkpoint 5 — índice persistente + buscador con umbral. Criterios de éxito de la Clase 5."""

import pytest

from conftest import embedding_falso
from tp.recuperacion.buscador import abrir_coleccion, buscar, indexar

TEXTOS = {
    "credenciales": "Para configurar credenciales copiá el archivo env de ejemplo y completá la API key.",
    "tokens": "Un token es un fragmento de texto que el modelo procesa; el costo se mide en tokens.",
    "timeouts": "Los timeouts y reintentos con backoff evitan que una llamada colgada bloquee la aplicación.",
}


def _registros():
    return [{"chunk_id": f"{k}-000-abc", "texto": t, "vector": embedding_falso(t),
             "documento_id": k, "posicion": 0, "fuente": f"{k}.md"} for k, t in TEXTOS.items()]


def _consulta_falsa(texto):
    return embedding_falso(texto)


@pytest.fixture
def coleccion(tmp_path):
    col = abrir_coleccion(ruta=tmp_path, nombre="test")
    indexar(col, _registros())
    return col


def test_indexar_es_idempotente(coleccion):
    indexar(coleccion, _registros())
    assert coleccion.count() == len(TEXTOS)


def test_guarda_metadata(coleccion):
    meta = coleccion.get(ids=["tokens-000-abc"])["metadatas"][0]
    assert {"documento_id", "posicion", "fuente"} <= meta.keys()


def test_devuelve_lo_relevante_primero(coleccion):
    res = buscar("¿Cómo configuro las credenciales y la API key?", coleccion, k=3, embed_fn=_consulta_falsa)
    assert res[0]["documento_id"] == "credenciales"
    assert {"chunk_id", "texto", "similitud", "documento_id", "posicion", "fuente"} <= res[0].keys()
    sims = [r["similitud"] for r in res]
    assert sims == sorted(sims, reverse=True)
    assert all(-1.0 <= s <= 1.0 for s in sims), "¿Convertiste distancia a similitud?"


def test_umbral_descarta_consultas_fuera_de_dominio(coleccion):
    res = buscar("receta de empanadas salteñas al horno", coleccion, k=3,
                 umbral_similitud=0.3, embed_fn=_consulta_falsa)
    assert res == []


def test_filtro_por_metadata(coleccion):
    res = buscar("tokens credenciales timeouts", coleccion, k=3,
                 where={"documento_id": "timeouts"}, embed_fn=_consulta_falsa)
    assert [r["documento_id"] for r in res] == ["timeouts"]


def test_el_indice_persiste(tmp_path):
    indexar(abrir_coleccion(ruta=tmp_path, nombre="persist"), _registros())
    reabierta = abrir_coleccion(ruta=tmp_path, nombre="persist")  # simula reiniciar el kernel
    assert reabierta.count() == len(TEXTOS)
