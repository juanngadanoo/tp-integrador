"""Limpieza y normalización (Clase 4, sección 4)."""

import re
import unicodedata


def limpiar_texto(texto: str) -> str:
    texto = unicodedata.normalize("NFKC", texto)   # comillas/acentos
    texto = re.sub(r"[ \t]+", " ", texto)           # espacios repetidos
    # MDN: ficha técnica del principio (dejamos solo "title:")
    texto = re.sub(r"^(---|slug:.*|page-type:.*|sidebar:.*)$", "", texto, flags=re.MULTILINE)
    # MDN: botones de navegación "anterior / siguiente"
    texto = re.sub(r"^\{\{(PreviousNext|Previous|Next)\(.*\)\}\}$", "", texto, flags=re.MULTILINE)
    # MDN: marcas solo para el sitio web (ejemplos interactivos, cartel "opcional") -> se borran
    texto = re.sub(r"\{\{(EmbedLiveSample|InteractiveExample|optional_inline)[^}]*\}\}", "", texto)
    # MDN: links con dos textos {{jsxref("ruta", "texto")}} -> nos quedamos con el texto
    texto = re.sub(r'\{\{\w+\("[^"]*", "([^"]*)"[^}]*\}\}', r"\1", texto)
    # MDN: links con un texto {{jsxref("Map")}} -> nos quedamos con Map
    texto = re.sub(r'\{\{\w+\("([^"]*)"\)\}\}', r"\1", texto)
    texto = re.sub(r"\n{3,}", "\n\n", texto)        # más de 2 saltos seguidos
    return texto.strip()
