"""Clasificador de intención — CHECKPOINT CLASE 3.

En la Clase 10 el agente lo va a usar para decidir si una pregunta va al RAG
o a una herramienta externa.

Tests: pytest tests/test_cp3_clasificador.py -v
"""

from typing import Literal

from pydantic import BaseModel, Field

from tp.llm.base import LLMProvider
from tp.llm.factory import get_provider


class IntencionConsulta(BaseModel):
    tipo_pregunta: Literal["concepto", "como_hacer", "error", "fuera_de_tema"] = Field(
        ...,
        description="concepto: qué es algo o cómo funciona. como_hacer: cómo lograr algo con código. error: un problema o resultado inesperado. fuera_de_tema: no tiene que ver con JavaScript.",
    )
    requiere_busqueda_en_documentacion: bool = Field(
        ...,
        description="True para toda pregunta sobre JavaScript, aunque sepas la respuesta. False solo si es fuera_de_tema.",
    )
    resumen: str = Field(..., max_length=200, description="La pregunta resumida en una oración.")


SYSTEM_CLASIFICADOR = (
    "Sos un clasificador de preguntas para un asistente que responde usando la documentación de JavaScript de MDN. "
    "Categorías: "
    "concepto = el usuario quiere entender qué es algo o cómo funciona. "
    "como_hacer = quiere lograr algo concreto con código. "
    "error = describe un problema, un error o un resultado inesperado. "
    "fuera_de_tema = la pregunta no tiene que ver con JavaScript. "
    "Regla: toda pregunta sobre JavaScript (concepto, como_hacer o error) requiere búsqueda en la documentación, "
    "aunque vos sepas la respuesta. Solo fuera_de_tema no requiere búsqueda."
)


def clasificar(texto: str, provider: LLMProvider | None = None) -> IntencionConsulta:
    """Devuelve SIEMPRE un IntencionConsulta validado, o levanta una excepción clara."""
    if not texto or not texto.strip():
        raise ValueError("El texto a clasificar está vacío.")
    provider = provider or get_provider()
    return provider.generate_structured(
        f"Clasificá esta pregunta de un usuario sobre JavaScript: '{texto}'",
        IntencionConsulta,
        system=SYSTEM_CLASIFICADOR,
    )
