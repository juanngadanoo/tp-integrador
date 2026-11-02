"""Factory de proveedores (Clase 3). Para sumar otro proveedor: crear su clase y agregarla al dict."""

from tp.config import settings
from tp.llm.base import LLMProvider


def get_provider() -> LLMProvider:
    from tp.llm.google import GoogleProvider

    proveedores = {
        "google": GoogleProvider,
    }
    if settings.llm_provider not in proveedores:
        raise ValueError(f"Proveedor '{settings.llm_provider}' no implementado. "
                         f"Disponibles: {', '.join(proveedores)}")
    return proveedores[settings.llm_provider]()
