"""Aplicativo principal: Hub de seleção de jogos."""

import streamlit as st

# Jogo 1 — Quiz
from games.quiz.core.state import init_state as quiz_init_state
from games.quiz.pages.home import page_home as quiz_home
from games.quiz.pages.quiz import page_quiz
from games.quiz.pages.result import page_result

# Jogo 2 — Roleta
from games.roleta.pages.roleta import page_roleta

# Jogo 3 — Sorte
from games.sorte.pages.sorte import page_sorte


def init_hub_state() -> None:
    """Garante que o estado global do Hub exista."""
    if "active_game" not in st.session_state:
        st.session_state.active_game = None
    if "page" not in st.session_state:
        st.session_state.page = "home"


def go_hub() -> None:
    """Retorna para a tela inicial do app."""
    st.session_state.active_game = None
    st.session_state.page = "home"
    st.rerun()


def main() -> None:
    """Controla o fluxo entre Hub e os jogos."""
    init_hub_state()
    quiz_init_state()

    game = st.session_state.active_game

    # ------------------------------------------------------------------
    # 1) HUB — Seleção de jogo
    # ------------------------------------------------------------------
    if game is None:
        st.title("Escolha seu jogo")

        # Jogo 1 — Quiz
        st.markdown("### 🎯 Jogo 1 — Quiz")
        if st.button(
            "▶️ Jogar Quiz",
            key="go_quiz",
            use_container_width=True,
        ):
            st.session_state.active_game = "quiz"
            st.session_state.page = "home"
            st.rerun()

        st.markdown("---")

        # Jogo 2 — Roleta
        st.markdown("### 🌀 Jogo 2 — Roleta")
        if st.button(
            "▶️ Jogar Roleta",
            key="go_roleta_main",
            use_container_width=True,
        ):
            st.session_state.active_game = "roleta"
            st.rerun()

        st.markdown("---")

        # Jogo 3 — Sorte
        st.markdown("### 🍀 Jogo 3 — Sorte")
        if st.button(
            "▶️ Jogar Sorte",
            key="go_sorte_main",
            use_container_width=True,
        ):
            st.session_state.active_game = "sorte"
            st.rerun()

        return

    # ------------------------------------------------------------------
    # 2) Jogo 1 — Quiz (usa o roteamento interno do jogo)
    # ------------------------------------------------------------------
    if game == "quiz":
        if st.button("⟵ Voltar ao início", key="quiz_back"):
            go_hub()
            return

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

        st.session_state.page = "home"
        st.rerun()

    # ------------------------------------------------------------------
    # 3) Jogo 2 — Roleta
    # ------------------------------------------------------------------
    if game == "roleta":
        if st.button("⟵ Voltar ao início", key="roleta_back"):
            go_hub()
            return

        page_roleta()
        return

    # ------------------------------------------------------------------
    # 4) Jogo 3 — Sorte
    # ------------------------------------------------------------------
    if game == "sorte":
        if st.button("⟵ Voltar ao início", key="sorte_back"):
            go_hub()
            return

        page_sorte()
        return


if __name__ == "__main__":
    main()
