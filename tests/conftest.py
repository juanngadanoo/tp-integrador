"""Herramientas compartidas por los tests. Nada de esto gasta API."""

import hashlib
import re

import numpy as np
import pytest


class FakeAPIError(Exception):
    """Imita `google.genai.errors.APIError`: el código HTTP está en el atributo `code`
    (igual que en el SDK real; NO es `status_code`)."""

    def __init__(self, status_code: int, mensaje: str = "error falso"):
        super().__init__(f"{status_code} {mensaje}")
        self.code = status_code


class _FakeResp:
    def __init__(self, text):
        self.text = text


class FakeGoogleClient:
    """Imita genai.Client: client.models.generate_content(...).
    `respuestas` es una lista: cada elemento es un str (respuesta OK) o una Exception (se lanza)."""

    def __init__(self, respuestas):
        self.respuestas = list(respuestas)
        self.llamadas = []
        self.models = self

    def generate_content(self, model, contents, config=None):
        self.llamadas.append({"model": model, "contents": contents, "config": config})
        r = self.respuestas.pop(0)
        if isinstance(r, Exception):
            raise r
        return _FakeResp(r)


def embedding_falso(texto: str, dim: int = 64) -> list[float]:
    """Bolsa de palabras hasheada y normalizada: textos con palabras en común quedan cerca."""
    v = np.zeros(dim)
    for palabra in re.findall(r"\w+", texto.lower()):
        v[int(hashlib.md5(palabra.encode()).hexdigest(), 16) % dim] += 1
    n = np.linalg.norm(v)
    return (v / n).tolist() if n else v.tolist()


@pytest.fixture
def sin_esperas(monkeypatch):
    """Anula time.sleep para que los tests de reintentos no tarden."""
    import time
    monkeypatch.setattr(time, "sleep", lambda s: None)
