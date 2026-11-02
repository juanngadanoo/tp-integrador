"""GoogleProvider — CHECKPOINT CLASE 3 (lo escribís vos).

Ya tenés toda la lógica hecha en tu notebook de la Clase 2:
- `llamar_google` (sección 2): cómo armar la llamada y leer el texto.
- el `for intento in range(3)` de tu `LLMClient` (sección 10): reintentos con backoff.

La tarea es mover eso adentro de `generate()`. Los tests de tests/test_cp3_proveedor.py
te dicen si quedó bien:  pytest tests/test_cp3_proveedor.py -v
"""

import random
import time

from tp.config import settings
from tp.llm.base import LLMProvider

CODIGOS_REINTENTABLES = {429, 500, 502, 503, 504}


class GoogleProvider(LLMProvider):
    def __init__(self, client=None):
        # `client` se puede inyectar desde afuera: los tests le pasan uno falso para no gastar API.
        if client is None:
            from google import genai
            if not settings.google_api_key:
                raise RuntimeError("Falta GOOGLE_API_KEY en el .env")
            client = genai.Client(api_key=settings.google_api_key)
        self.client = client
        self.model_id = settings.google_model_id
        self.max_reintentos = 3

    def generate(self, prompt: str, system: str | None = None,
                temperature: float = 0.7, max_tokens: int = 500) -> str:
        if not isinstance(max_tokens, int):
            raise ValueError("max_tokens debe ser un entero")
        if max_tokens <= 0:
            raise ValueError("max_tokens debe ser un entero mayor a 0")
        raise NotImplementedError("Checkpoint 3: completá GoogleProvider.generate")
