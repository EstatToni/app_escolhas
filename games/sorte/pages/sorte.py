"""Página principal do Jogo 3 — Sorte (3 cartas: passado, presente, futuro)."""

import random
from typing import Dict, List

import streamlit as st

from games.sorte.core.loader import load_sorte_cards
from games.sorte.core.state import init_sorte_state, pick_card, reset_sorte


def _stage_label(stage: str) -> str:
    """Retorna rótulo legível para o estágio."""
    if stage == "past":
        return "passado"
    if stage == "present":
        return "presente"
    if stage == "future":
        return "futuro"
    return stage


def _render_finished() -> None:
    """Mostra a leitura final das três cartas."""
    st.subheader("Leitura completa")

    picks = st.session_state.sorte_picks
    for item in picks:
        label = item["label"]
        card = item["card"]
        stage = item["stage"]

        st.markdown(f"### {label}: {card.get('name', 'Carta')}")

        text = card.get(stage) or card.get("meaning", "")
        if text:
            st.write(text)

        st.divider()

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🔁 Nova leitura", key="sorte_new"):
            reset_sorte()
            st.rerun()
    with c2:
        if st.button("⟵ Voltar ao início", key="sorte_home"):
            from app import go_hub
            go_hub()


def _render_choice_stage() -> None:
    """Renderiza a etapa de escolha de uma carta para o estágio atual."""
    stage = st.session_state.sorte_stage
    label = _stage_label(stage)

    st.subheader(f"Escolha uma carta para o {label}")

    left: List[Dict] = st.session_state.sorte_deck_left
    if not left:
        st.warning("Acabaram as cartas disponíveis.")
        st.session_state.sorte_stage = "done"
        return

    if len(left) <= 5:
        sample = left
    else:
        sample = random.sample(left, 5)

    st.caption("Clique em uma das cartas abaixo:")

    cols = st.columns(len(sample))
    for col, card in zip(cols, sample):
        with col:
            if st.button(
                "🂠",
                key=f"sorte_card_{stage}_{card['id']}",
                help="Escolher esta carta",
            ):
                pick_card(card)
                st.rerun()


def page_sorte() -> None:
    """Renderiza o Jogo 3 — Sorte (3 cartas: passado, presente, futuro)."""
    deck = load_sorte_cards()
    init_sorte_state(deck)

    st.title("🍀 Jogo 3 — Sorte")
    st.caption(
        "Você vai escolher três cartas: uma para o passado, "
        "uma para o presente e uma para o futuro."
    )

    stage = st.session_state.sorte_stage

    if stage == "done":
        _render_finished()
        return

    st.write(
        "As cartas estão embaralhadas. "
        "Escolha pela sensação, não pela lógica."
    )

    _render_choice_stage()
