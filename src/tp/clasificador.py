"""Clasificador de intención — CHECKPOINT CLASE 3 (lo escribís vos).

Este modelo NO es un ejercicio suelto: en la Clase 10 el agente lo va a usar para
decidir si una pregunta va al RAG o a una herramienta externa. Diseñalo pensando en eso.

Tests: pytest tests/test_cp3_clasificador.py -v
"""

from pydantic import BaseModel

from tp.llm.base import LLMProvider
from tp.llm.factory import get_provider


class IntencionConsulta(BaseModel):
    # TODO (vos): definí los campos. Mínimo:
    #   - tipo_pregunta: Literal[...] con 3-5 categorías que tengan sentido para documentación técnica
    #   - requiere_busqueda_en_documentacion: bool
    #   - resumen: str con un Field(max_length=...)
    # Pensá: ¿qué otra cosa necesitaría saber el agente para decidir qué hacer con la pregunta?
    pass


SYSTEM_CLASIFICADOR = (
    # TODO (vos): instrucciones para el modelo. Qué es cada categoría, cuándo requiere búsqueda.
    ""
)


def clasificar(texto: str, provider: LLMProvider | None = None) -> IntencionConsulta:
    """Devuelve SIEMPRE un IntencionConsulta validado, o levanta una excepción clara."""
    provider = provider or get_provider()
    # TODO (vos): validar `texto` y usar provider.generate_structured(...)
    raise NotImplementedError("Checkpoint 3: completá clasificar")
