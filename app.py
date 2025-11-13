"""Roteador principal: Hub de jogos + Quiz + Jogo 2."""

import streamlit as st
from pages.game2 import page_game2  # Jogo 2 (novo)

from core.state import go_hub, set_game
from pages.home import page_home as page_quiz_home  # Jogo 1 (Quiz)


def _page_hub() -> None:
    """Tela de seleção de jogo (Hub)."""
    st.title("Escolha seu jogo")
    st.caption("Comece por um modo.")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Jogo 1 — Quiz")
        st.caption("Perguntas por tema com resultado final.")
        if st.button("▶️ Abrir Quiz", key="sel_quiz", width="stretch"):
            set_game("quiz")
        st.rerun()

    with c2:
        st.subheader("Jogo 2")
        st.caption("Novo modo — vamos construir agora.")
        if st.button("▶️ Abrir Jogo 2", key="sel_game2", width="stretch"):
            set_game("game2")
        st.rerun()


def main() -> None:
    """Roteia entre Hub, Quiz e Jogo 2."""
    if "game" not in st.session_state:
        st.session_state.game = None

    game = st.session_state.game
    if not game:
        _page_hub()
        return

    if game == "quiz":
        page_quiz_home()
        return

    if game == "game2":
        page_game2()
        return

    go_hub()
    st.rerun()


if __name__ == "__main__":
    main()
