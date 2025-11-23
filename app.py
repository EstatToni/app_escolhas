"""Ponto de entrada do app Streamlit; roteamento entre páginas."""

import streamlit as st

from core.state import init_state, reset_app, get_page
from pages.home import page_home
from pages.quiz import page_quiz
from pages.result import page_result


def main():
    """Configura e roteia páginas."""
    st.set_page_config(page_title="Jogo das Escolhas", page_icon="⚡")
    init_state()
    st.sidebar.button("Resetar", on_click=reset_app)
    page = get_page()
    if page == "home":
        page_home()
    elif page == "quiz":
        page_quiz()
    elif page == "result":
        page_result()
    else:
        reset_app()
        page_home()


if __name__ == "__main__":
    main()
