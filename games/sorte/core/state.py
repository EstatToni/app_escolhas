"""Gerência de estado do Jogo 3 — Sorte."""

from typing import Dict, List
import streamlit as st


def init_sorte_state(deck: List[Dict]) -> None:
    """Inicializa o estado da leitura de cartas, se ainda não existir."""
    if "sorte_deck_all" not in st.session_state:
        st.session_state.sorte_deck_all = list(deck)
        st.session_state.sorte_deck_left = list(deck)
        st.session_state.sorte_picks = []
        st.session_state.sorte_stage = "past"


def reset_sorte() -> None:
    """Reinicia a leitura, restaurando o baralho e limpando escolhas."""
    st.session_state.sorte_deck_left = list(
        st.session_state.sorte_deck_all
    )
    st.session_state.sorte_picks = []
    st.session_state.sorte_stage = "past"


def pick_card(card: Dict) -> None:
    """Registra a carta escolhida para o estágio atual e avança estágio."""
    stage = st.session_state.sorte_stage
    label_map = {
        "past": "Passado",
        "present": "Presente",
        "future": "Futuro",
    }
    label = label_map.get(stage, stage)

    st.session_state.sorte_picks.append(
        {
            "stage": stage,
            "label": label,
            "card": card,
        }
    )

    cid = card.get("id")
    st.session_state.sorte_deck_left = [
        c for c in st.session_state.sorte_deck_left
        if c.get("id") != cid
    ]

    if stage == "past":
        st.session_state.sorte_stage = "present"
    elif stage == "present":
        st.session_state.sorte_stage = "future"
    else:
        st.session_state.sorte_stage = "done"
