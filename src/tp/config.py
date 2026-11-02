"""Configuración central del proyecto.

Todo lo que dependa del entorno (credenciales, modelos, rutas) se lee ACÁ y en
ningún otro lado. El resto del código importa `settings` en vez de llamar a
os.environ por su cuenta: así hay un solo lugar para revisar en la defensa.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

# Raíz del repo (dos niveles arriba de src/tp/)
RAIZ = Path(__file__).resolve().parents[2]
load_dotenv(RAIZ / ".env")


@dataclass(frozen=True)
class Settings:
    llm_provider: str = os.environ.get("LLM_PROVIDER", "google").lower()

    # Google (Gemini)
    google_api_key: str | None = os.environ.get("GOOGLE_API_KEY")
    google_model_id: str = os.environ.get("GOOGLE_MODEL_ID", "gemini-3.8-flash")
    google_embedding_model_id: str = os.environ.get("GOOGLE_EMBEDDING_MODEL_ID", "gemini-embedding-001")
    # Dimensión del embedding. Si cambia, hay que re-ingestar todo el corpus.
    embedding_dim: int = int(os.environ.get("EMBEDDING_DIM", "768"))

    # Rutas
    corpus_dir: Path = RAIZ / os.environ.get("CORPUS_DIR", "data/corpus")
    chroma_dir: Path = RAIZ / os.environ.get("CHROMA_DIR", "data/chroma")
    chroma_coleccion: str = os.environ.get("CHROMA_COLECCION", "corpus_tp")


settings = Settings()
