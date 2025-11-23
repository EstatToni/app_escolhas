"""Leitura e validação de temas em JSON."""

import json
from pathlib import Path
from typing import Dict, List

THEMES_DIR = Path("themes")


def load_theme_files() -> List[Path]:
    """Retorna lista ordenada de arquivos JSON de temas."""
    return sorted(THEMES_DIR.glob("*.json"))


def load_theme(path: Path) -> Dict:
    """Carrega um tema JSON e valida todas as chaves obrigatórias."""
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    required = ["id", "title", "intro", "questions", "results", "tie_breakers"]
    for key in required:
        if key not in data:
            raise ValueError(f"Tema inválido, faltou a chave: {key}")

    return data
