"""Interfaz común de proveedores (Clase 3, sección 8) + patrón de reintento estructurado (sección 3).

Este archivo es código de la cátedra portado a módulo. No hace falta tocarlo.
"""

import json
from abc import ABC, abstractmethod

from pydantic import BaseModel, ValidationError


def generar_estructurado_con_reintentos(llamar_fn, prompt: str, schema_model: type[BaseModel],
                                        system: str | None = None, max_reintentos: int = 3) -> BaseModel:
    """Pide JSON, valida con Pydantic y, si falla, reintenta mostrándole el error al modelo."""
    instruccion_base = (
        f"{prompt}\n\nRespondé ÚNICAMENTE con un JSON válido que cumpla este schema "
        f"(sin texto adicional, sin markdown):\n{json.dumps(schema_model.model_json_schema(), ensure_ascii=False)}"
    )
    ultimo_error = None

    for _ in range(max_reintentos):
        instruccion = instruccion_base
        if ultimo_error:
            instruccion += (f"\n\nTu respuesta anterior no cumplió el schema. Error: {ultimo_error}\n"
                            "Corregí y devolvé SOLO el JSON.")
        texto = llamar_fn(instruccion, system=system, temperature=0.0)
        # Gemini a veces envuelve el JSON en ```json ... ```: lo sacamos antes de validar.
        texto = texto.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
        try:
            return schema_model.model_validate_json(texto)
        except (ValidationError, json.JSONDecodeError) as e:
            ultimo_error = str(e)

    raise ValueError(f"No se obtuvo una respuesta válida tras {max_reintentos} intentos. "
                     f"Último error: {ultimo_error}")


class LLMProvider(ABC):
    """Interfaz común para cualquier proveedor de modelos de lenguaje."""

    @abstractmethod
    def generate(self, prompt: str, system: str | None = None,
                 temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Devuelve SOLO el texto generado por el modelo."""

    def generate_structured(self, prompt: str, schema_model: type[BaseModel], system: str | None = None):
        """Por defecto usa el reintento genérico. Un proveedor con soporte nativo puede sobreescribirlo."""
        return generar_estructurado_con_reintentos(self.generate, prompt, schema_model, system=system)
