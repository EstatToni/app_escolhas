"""Aplicativo principal: Hub de seleção de jogos e roteamento de cada modo."""

import streamlit as st

# Importa páginas do Jogo 1 (Quiz)
from games.quiz.pages.home import page_home as quiz_home
from games.quiz.pages.quiz import page_quiz
from games.quiz.pages.result import page_result


def init_hub_state() -> None:
    """Garante que o estado global do Hub exista."""
    if "active_game" not in st.session_state:
        st.session_state.active_game = None


def go_hub() -> None:
    """Retorna para a tela inicial."""
    st.session_state.active_game = None
    st.rerun()


def main() -> None:
    """Controla o fluxo entre Hub e cada jogo."""
    init_hub_state()

    game = st.session_state.active_game

    # ---------------------------------------------------------------------
    # 1) HUB — Seleção de jogo
    # ---------------------------------------------------------------------
    if game is None:
        st.title("Escolha seu jogo")

        st.markdown("### 🎯 Jogo 1 — Quiz")
        if st.button("▶️ Jogar Quiz", key="go_quiz", use_container_width=True):
            st.session_state.active_game = "quiz"
            st.session_state.page = "home"   # <<< IMPORTANTE
            st.rerun()

        st.markdown("---")

        st.markdown("### 🌀 Jogo 2 — Roleta")
        st.button("⏳ Em breve", key="go_roleta",
                  disabled=True, use_container_width=True)

        st.markdown("---")

        st.markdown("### 🍀 Jogo 3 — Sorte")
        st.button("⏳ Em breve", key="go_sorte",
                  disabled=True, use_container_width=True)

        return

    # ---------------------------------------------------------------------
    # 2) Jogo 1 — Quiz (roteamento interno)
    # ---------------------------------------------------------------------
    if game == "quiz":

        # Botão para voltar ao Hub
        if st.button("⟵ Voltar ao início", key="back_from_quiz"):
            go_hub()
            return

        # Estado interno do jogo (home → quiz → result)
        page = st.session_state.get("page", "home")

        if page == "home":
            quiz_home()
            return

        if page == "quiz":
            page_quiz()
            return

        if page == "result":
            page_result()
            return

        # Se der algo inesperado, volta pra home do jogo
        st.session_state.page = "home"
        st.rerun()


if __name__ == "__main__":
    main()
