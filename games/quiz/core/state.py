"""Gerência do estado via st.session_state e operações do quiz."""

from typing import Dict
import streamlit as st


def init_state():
    """Inicializa todas as chaves necessárias no session_state."""
    if "page" not in st.session_state:
        st.session_state.page = "home"
    if "theme" not in st.session_state:
        st.session_state.theme = None
    if "q_index" not in st.session_state:
        st.session_state.q_index = 0
    if "answers" not in st.session_state:
        st.session_state.answers = []
    if "scores" not in st.session_state:
        st.session_state.scores = {}
    if "finished" not in st.session_state:
        st.session_state.finished = False
    if "completed" not in st.session_state:
        st.session_state.completed = set()


def get_page() -> str:
    """Retorna a página atual."""
    return st.session_state.page


def set_page(name: str):
    """Define a página atual."""
    st.session_state.page = name


def start_quiz(theme: Dict):
    """Inicializa o quiz para um tema específico."""
    st.session_state.theme = theme
    st.session_state.q_index = 0
    st.session_state.answers = []
    st.session_state.scores = {k: 0 for k in theme["results"].keys()}
    st.session_state.finished = False
    st.session_state.page = "quiz"


def reset_app():
    """Retorna o app para a tela inicial mantendo progresso salvo."""
    for key in ["theme", "q_index", "answers", "scores", "finished"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.page = "home"


def current_question():
    """Retorna o dicionário da pergunta atual."""
    theme = st.session_state.theme
    idx = st.session_state.q_index
    return theme["questions"][idx]


def record_answer(q_id: str, opt_id: str):
    """Registra uma resposta e aplica os pesos ao placar."""
    st.session_state.answers.append((q_id, opt_id))
    theme = st.session_state.theme
    q = {q["id"]: q for q in theme["questions"]}[q_id]

    opt = next((o for o in q.get("options", []) if o["id"] == opt_id), None)
    weights = opt.get("weights", {}) if opt else q.get("weights", {})

    for rk in st.session_state.scores.keys():
        st.session_state.scores[rk] += int(weights.get(rk, 0))


def next_step():
    """Avança para a próxima pergunta ou finaliza o quiz."""
    theme = st.session_state.theme
    if st.session_state.q_index + 1 < len(theme["questions"]):
        st.session_state.q_index += 1
    else:
        st.session_state.finished = True
        st.session_state.page = "result"


def mark_completed(theme_id: str):
    """Marca um tema como concluído."""
    st.session_state.completed.add(theme_id)


def is_completed(theme_id: str) -> bool:
    """Retorna True se o tema já foi concluído."""
    return theme_id in st.session_state.completed
