"""Carrega perguntas do arquivo themes/roleta.json."""

import json
from pathlib import Path


THEME_PATH = Path("games/roleta/roleta.json")


def load_roleta_questions() -> list[str]:
    """Retorna lista de perguntas para a roleta."""
    if not THEME_PATH.exists():
        return []

    with THEME_PATH.open("r", encoding="utf-8") as f:
        data = json.load(f)

    qs = data.get("questions", [])
    return [str(x).strip() for x in qs if str(x).strip()]
