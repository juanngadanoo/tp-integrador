"""Estrategias de chunking (Clase 4, sección 5) y modelo Chunk (sección 6)."""

import hashlib
from dataclasses import dataclass, field


def chunking_por_caracteres(texto: str, tamano: int = 300, solapamiento: int = 50) -> list[str]:
    """Tamaño fijo con solapamiento, por caracteres (no respeta oraciones)."""
    if solapamiento >= tamano:
        raise ValueError("El solapamiento tiene que ser menor que el tamaño del chunk.")
    chunks, paso = [], tamano - solapamiento
    for inicio in range(0, len(texto), paso):
        chunk = texto[inicio:inicio + tamano]
        if chunk.strip():
            chunks.append(chunk)
        if inicio + tamano >= len(texto):
            break
    return chunks


def chunking_por_parrafos(texto: str, max_chars: int = 500) -> list[str]:
    """Agrupa párrafos (separados por línea en blanco) hasta el tamaño máximo.
    Ojo: un párrafo solo más largo que max_chars queda entero (no se corta)."""
    parrafos = [p.strip() for p in texto.split("\n\n") if p.strip()]
    chunks, actual = [], ""
    for p in parrafos:
        if len(actual) + len(p) + 1 <= max_chars:
            actual = (actual + "\n\n" + p).strip()
        else:
            if actual:
                chunks.append(actual)
            actual = p
    if actual:
        chunks.append(actual)
    return chunks


@dataclass
class Chunk:
    texto: str
    documento_id: str
    posicion: int
    # TODO (vos, practicá Clase 4 sección 6): agregá
    #   - fuente: str            (nombre de archivo o URL; lo vas a mostrar en las citas de la Clase 6)
    #   - fecha_ingesta: str     (timestamp ISO, con default_factory)
    chunk_id: str = field(init=False)

    def __post_init__(self):
        hash_contenido = hashlib.sha256(self.texto.encode()).hexdigest()[:8]
        self.chunk_id = f"{self.documento_id}-{self.posicion:03d}-{hash_contenido}"
