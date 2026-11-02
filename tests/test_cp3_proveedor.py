"""Checkpoint 3 — GoogleProvider.generate. Criterios de la consigna de las Clases 2 y 3."""

import pytest

from conftest import FakeAPIError, FakeGoogleClient
from tp.llm.base import LLMProvider
from tp.llm.google import GoogleProvider


def test_es_un_llmprovider():
    assert issubclass(GoogleProvider, LLMProvider)


def test_devuelve_solo_el_texto():
    p = GoogleProvider(client=FakeGoogleClient(["París"]))
    assert p.generate("¿Capital de Francia?") == "París"


def test_pasa_system_temperature_y_max_tokens():
    fake = FakeGoogleClient(["ok"])
    GoogleProvider(client=fake).generate("hola", system="sé breve", temperature=0.1, max_tokens=42)
    config = fake.llamadas[0]["config"]
    assert config.system_instruction == "sé breve"
    assert config.temperature == 0.1
    assert config.max_output_tokens == 42


@pytest.mark.parametrize("max_tokens", [-10, 0, "500", 2.5])
def test_max_tokens_invalido_da_valueerror_sin_llamar_a_la_api(max_tokens):
    fake = FakeGoogleClient([])
    with pytest.raises(ValueError):
        GoogleProvider(client=fake).generate("hola", max_tokens=max_tokens)
    assert fake.llamadas == [], "Un input inválido se rechaza ANTES de gastar una llamada."


@pytest.mark.parametrize("prompt", ["", "   ", None])
def test_prompt_vacio_da_valueerror(prompt):
    with pytest.raises(ValueError):
        GoogleProvider(client=FakeGoogleClient([])).generate(prompt)


def test_reintenta_ante_rate_limit(sin_esperas):
    fake = FakeGoogleClient([FakeAPIError(429), FakeAPIError(503), "ok"])
    assert GoogleProvider(client=fake).generate("hola") == "ok"
    assert len(fake.llamadas) == 3


def test_error_400_no_se_reintenta(sin_esperas):
    fake = FakeGoogleClient([FakeAPIError(400, "bad request"), "no debería llegar"])
    with pytest.raises(ValueError):
        GoogleProvider(client=fake).generate("hola")
    assert len(fake.llamadas) == 1, "Un 400 no se arregla reintentando."


def test_reintentos_agotados_da_error_claro(sin_esperas):
    fake = FakeGoogleClient([FakeAPIError(429)] * 3)
    with pytest.raises(RuntimeError):
        GoogleProvider(client=fake).generate("hola")
    assert len(fake.llamadas) == 3


def test_respuesta_vacia_no_devuelve_none():
    with pytest.raises(RuntimeError):
        GoogleProvider(client=FakeGoogleClient([None])).generate("hola")
