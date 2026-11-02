"""Checkpoint 3 — clasificar(): o devuelve un objeto validado, o falla explícitamente."""

import json

import pytest

from tp.clasificador import IntencionConsulta, clasificar
from tp.llm.base import LLMProvider


class FakeProvider(LLMProvider):
    def __init__(self, respuestas):
        self.respuestas = list(respuestas)
        self.llamadas = 0

    def generate(self, prompt, system=None, temperature=0.7, max_tokens=500):
        self.llamadas += 1
        return self.respuestas.pop(0)


def _json_valido() -> str:
    """Arma un JSON válido para TU schema, sea cual sea el Literal que elegiste."""
    props = IntencionConsulta.model_json_schema()["properties"]
    return json.dumps({
        "tipo_pregunta": props["tipo_pregunta"]["enum"][0],
        "requiere_busqueda_en_documentacion": True,
        "resumen": "Pregunta sobre configuración.",
    })


def test_schema_tiene_los_campos_minimos():
    props = IntencionConsulta.model_json_schema()["properties"]
    for campo in ("tipo_pregunta", "requiere_busqueda_en_documentacion", "resumen"):
        assert campo in props, f"Falta el campo '{campo}'"
    assert len(props["tipo_pregunta"].get("enum", [])) >= 3, "tipo_pregunta: Literal con 3 o más categorías"
    assert props["requiere_busqueda_en_documentacion"]["type"] == "boolean"
    assert "maxLength" in props["resumen"], "Limitá el largo de resumen con Field(max_length=...)"


def test_devuelve_objeto_validado():
    r = clasificar("¿Cómo configuro las credenciales?", provider=FakeProvider([_json_valido()]))
    assert isinstance(r, IntencionConsulta)


def test_se_recupera_de_una_respuesta_invalida():
    p = FakeProvider(["esto no es json", _json_valido()])
    assert isinstance(clasificar("hola", provider=p), IntencionConsulta)
    assert p.llamadas == 2


def test_categoria_inventada_no_pasa():
    malo = json.loads(_json_valido()) | {"tipo_pregunta": "categoria_inventada_xyz"}
    with pytest.raises(ValueError):
        clasificar("hola", provider=FakeProvider([json.dumps(malo)] * 3))


@pytest.mark.parametrize("texto", ["", "   "])
def test_texto_vacio_falla_sin_llamar(texto):
    p = FakeProvider([])
    with pytest.raises(ValueError):
        clasificar(texto, provider=p)
    assert p.llamadas == 0


def test_tiene_system_prompt():
    from tp.clasificador import SYSTEM_CLASIFICADOR
    assert len(SYSTEM_CLASIFICADOR.strip()) > 50, "Escribí instrucciones reales para el clasificador."
