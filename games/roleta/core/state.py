"""Gerencia o estado da Roleta."""

import streamlit as st
from typing import List


def init_roleta_state(all_questions: List[str]) -> None:
    """Inicializa o estado do jogo da roleta."""
    if "roleta_all" not in st.session_state:
        st.session_state.roleta_all = list(all_questions)
    if "roleta_left" not in st.session_state:
        st.session_state.roleta_left = list(all_questions)
    if "roleta_last" not in st.session_state:
        st.session_state.roleta_last = None


def reset_roleta() -> None:
    """Reinicia a roleta e restaura todas as perguntas."""
    st.session_state.roleta_left = list(st.session_state.roleta_all)
    st.session_state.roleta_last = None
