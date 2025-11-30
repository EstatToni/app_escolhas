"""Carregamento das cartas do Jogo 3 — Sorte."""

import json
from pathlib import Path
from typing import Dict, List


BASE_DIR = Path(__file__).resolve().parents[1]
CARDS_PATH = BASE_DIR / "cards.json"


def _fallback_cards() -> List[Dict]:
    """Retorna um baralho básico se não houver JSON ou der erro."""
    return [
        {
            "id": "viajante",
            "name": "O Viajante",
            "past": "Um começo antigo, escolhas feitas na coragem "
                    "sem tanta estrutura.",
            "present": "Você está em transição, testando caminhos "
                       "sem ter tudo definido.",
            "future": "Novos percursos se abrem, mas pedem um pouco "
                      "mais de calma e atenção aos sinais.",
        },
        {
            "id": "ancora",
            "name": "A Âncora",
            "past": "Situações em que você segurou firme algo, mesmo "
                    "quando já podia ter ido embora.",
            "present": "Existe um ponto de estabilidade na sua vida "
                       "que sustenta o resto.",
            "future": "Pode surgir uma oportunidade de se firmar em "
                      "algo mais sólido e tranquilo.",
        },
        {
            "id": "labirinto",
            "name": "O Labirinto",
            "past": "Momentos de confusão, indecisão ou caminhos que "
                    "pareciam se repetir.",
            "present": "Você talvez esteja repensando rotas, testando "
                       "alternativas sem respostas claras.",
            "future": "Vem um tipo de clareza, mas só depois de aceitar "
                      "que nem tudo tem solução imediata.",
        },
        {
            "id": "ponte",
            "name": "A Ponte",
            "past": "Alguém ou algo já funcionou como conexão crucial "
                    "entre fases da sua vida.",
            "present": "Você está em meio a uma travessia, saindo de "
                       "um lugar e ainda não pisando no outro.",
            "future": "Aparece uma passagem mais suave para a próxima "
                      "etapa, talvez com ajuda externa.",
        },
        {
            "id": "fogueira",
            "name": "A Fogueira",
            "past": "Houve períodos de intensidade alta, de muito "
                    "gasto de energia em pouco tempo.",
            "present": "Você pode estar queimando energia em algo que "
                       "faz sentido, mas cansa.",
            "future": "Vem um convite para aquecer, mas também dosar "
                      "quanto combustível você coloca em cada coisa.",
        },
        {
            "id": "jardim",
            "name": "O Jardim",
            "past": "Fases mais leves, com convivência boa e sensação "
                    "de espaço aberto.",
            "present": "Pode haver um desejo de cuidar melhor do seu "
                       "entorno, rotina e corpo.",
            "future": "Um cenário mais fértil surge se você regar aos "
                      "poucos, em vez de tentar resolver tudo num dia.",
        },
    ]


def load_sorte_cards() -> List[Dict]:
    """Carrega as cartas do JSON; cai em fallback se falhar."""
    if not CARDS_PATH.exists():
        return _fallback_cards()

    try:
        data = json.loads(CARDS_PATH.read_text(encoding="utf-8"))
    except Exception:
        return _fallback_cards()

    items = data.get("cards", [])
    cards: List[Dict] = []
    for raw in items:
        if not isinstance(raw, dict):
            continue
        if "id" not in raw or "name" not in raw:
            continue
        cards.append(raw)

    if not cards:
        return _fallback_cards()
    return cards
