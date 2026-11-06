"""GoogleProvider — CHECKPOINT CLASE 3.

Implementa LLMProvider con Gemini:
- Valida la entrada antes de gastar una llamada (prompt vacío, max_tokens inválido).
- Reintenta con backoff + jitter ante errores temporales (429, 5xx).
- No reintenta un 400 (el pedido está mal armado) y avisa claro si la respuesta viene vacía.
- Timeout de 30 s para que una llamada colgada no bloquee la aplicación.

Tests: pytest tests/test_cp3_proveedor.py -v
"""

import random
import time

from google.genai import types

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
            client = genai.Client(
                api_key=settings.google_api_key,
                http_options=types.HttpOptions(timeout=30000),
            )
        self.client = client
        self.model_id = settings.google_model_id
        self.max_reintentos = 3

    def generate(self, prompt: str, system: str | None = None,
                temperature: float = 0.7, max_tokens: int = 500) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("El prompt está vacío.")
        if not isinstance(max_tokens, int):
            raise ValueError("max_tokens debe ser un entero")
        if max_tokens <= 0:
            raise ValueError("max_tokens debe ser un entero mayor a 0")
        config = types.GenerateContentConfig(
            system_instruction=system,
            temperature=temperature,
            max_output_tokens=max_tokens,
        )
        for intento in range(self.max_reintentos):
            try:
                respuesta = self.client.models.generate_content(
                    model=self.model_id,
                    contents=prompt,
                    config=config,
                )
                if not respuesta.text:
                    raise RuntimeError("Gemini devolvió una respuesta vacía.")
                return respuesta.text
            except Exception as err:
                codigo = getattr(err, "code", None)
                if codigo == 400:
                    raise ValueError(f"Pedido inválido (400): {err}") from err
                if codigo not in CODIGOS_REINTENTABLES:
                    raise
                if intento < self.max_reintentos - 1:
                    espera = (2 ** intento) + random.uniform(0, 1)
                    time.sleep(espera)

        raise RuntimeError(f"Se agotaron los {self.max_reintentos} intentos por errores temporales de la API.")