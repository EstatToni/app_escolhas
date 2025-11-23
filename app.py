"""Aplicativo principal: Hub de seleção de jogos."""

import streamlit as st

# Importa o jogo 1 (Quiz)
from games.quiz.pages.home import page_home as quiz_home


def init_hub_state() -> None:
    """Garante que o estado do Hub exista."""
    if "active_game" not in st.session_state:
        st.session_state.active_game = None


def go_hub() -> None:
    """Retorna para a tela inicial."""
    st.session_state.active_game = None
    st.rerun()


def main() -> None:
    """Controla o fluxo entre Hub e Jogos."""
    init_hub_state()

    game = st.session_state.active_game

    # ------------------------------------------------------
    # 1) HUB — Escolha do jogo
    # ------------------------------------------------------
    if game is None:
        st.title("Escolha seu jogo")

        st.markdown("### 🎯 Jogo 1 — Quiz")
        if st.button("▶️ Jogar Quiz", key="go_quiz", use_container_width=True):
            st.session_state.active_game = "quiz"
            st.rerun()

        st.markdown("---")

        st.markdown("### 🌀 Jogo 2 — Roleta")
        st.button("⏳ Em breve", key="go_roleta", disabled=True, use_container_width=True)

        st.markdown("---")

        st.markdown("### 🍀 Jogo 3 — Sorte")
        st.button("⏳ Em breve", key="go_sorte", disabled=True, use_container_width=True)

        return

    # ------------------------------------------------------
    # 2) Jogo 1 — Quiz
    # ------------------------------------------------------
    if game == "quiz":
        # Adiciona botão de voltar ao Hub
        if st.button("⟵ Voltar ao início", key="back_from_quiz"):
            go_hub()
            return

        quiz_home()
        return


if __name__ == "__main__":
    main()
