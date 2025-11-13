"""Página inicial do Jogo 2 (placeholder)."""

import streamlit as st

from core.state import go_hub


def page_game2() -> None:
    """Renderiza o modo 2 (a definir) com botão de retorno ao Hub."""
    st.title("Jogo 2")
    st.caption("Novo modo — em construção.")
    st.info("Aqui vamos implementar as mecânicas do Jogo 2.")

    if st.button("⟵ Voltar aos jogos", key="back_hub_g2", width="stretch"):
        go_hub()
        st.rerun()
