"""Gerência do estado via st.session_state e operações do quiz."""

from typing import Dict, List, Tuple

import streamlit as st


def init_state():
    """Inicializa chaves do estado se necessário."""
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
    """Obtém a página atual."""
    return st.session_state.page


def set_page(name: str):
    """Define a página atual."""
    st.session_state.page = name


def start_quiz(theme: Dict):
    """Inicia o quiz para o tema escolhido."""
    st.session_state.theme = theme
    st.session_state.q_index = 0
    st.session_state.answers = []
    st.session_state.scores = {k: 0 for k in theme["results"].keys()}
    st.session_state.finished = False
    st.session_state.page = "quiz"


def reset_app():
    """Reseta o app para a tela inicial (mantém progresso)."""
    for key in ["theme", "q_index", "answers", "scores", "finished"]:
        if key in st.session_state:
            del st.session_state[key]
    st.session_state.page = "home"


def current_question() -> Dict:
    """Retorna a pergunta atual do tema."""
    theme = st.session_state.theme
    idx = st.session_state.q_index
    return theme["questions"][idx]


def record_answer(q_id: str, opt_id: str):
    """Registra a resposta e atualiza pontuações pela opção escolhida."""
    st.session_state.answers.append((q_id, opt_id))
    theme = st.session_state.theme
    q_map = {q["id"]: q for q in theme["questions"]}
    q = q_map[q_id]
    opts = q.get("options", [])
    opt = next((o for o in opts if o.get("id") == opt_id), None)
    # Preferir pesos na opção; se ausente, cair para pesos da pergunta
    weight_map = {}
    if opt and isinstance(opt.get("weights"), dict):
        weight_map = opt["weights"]
    else:
        weight_map = q.get("weights", {})  # compatibilidade antiga
    for rk in st.session_state.scores.keys():
        st.session_state.scores[rk] += int(weight_map.get(rk, 0))


def next_step():
    """Avança para a próxima pergunta ou finaliza."""
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
    """Indica se o tema foi concluído."""
    return theme_id in st.session_state.completed
