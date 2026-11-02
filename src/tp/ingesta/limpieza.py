"""Limpieza y normalización (Clase 4, sección 4)."""

import re
import unicodedata


def limpiar_texto(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto)   # comillas/acentos
    texto = re.sub(r"[ \t]+", " ", texto)           # espacios repetidos
    texto = re.sub(r"\n{3,}", "\n\n", texto)        # más de 2 saltos seguidos
    # TODO (vos, practicá Clase 4): cuando tengas el corpus real, mirá qué boilerplate
    # se repite (headers, footers, "Página X de Y", menús) y agregá la regex acá.
    return texto.strip()
