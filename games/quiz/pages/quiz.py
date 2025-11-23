"""Página de perguntas do quiz, com barra e imagem por pergunta."""

from pathlib import Path

import streamlit as st

from games.quiz.core.state import current_question, next_step, record_answer

ROOT_DIR = Path(__file__).resolve().parents[3]


def _show_question_image(q: dict):
    """Exibe imagem da pergunta, resolvendo caminho relativo ao projeto."""
    path = q.get("image")
    if not path:
        return

    p = Path(path)
    if not p.is_absolute():
        p = ROOT_DIR / p
    if p.exists():
        st.image(str(p), caption=None)
    else:
        st.caption(f"[imagem não encontrada: {p}]")


def page_quiz():
    """Renderiza a página de perguntas com progresso e imagem."""
    theme = st.session_state.theme
    total_q = len(theme["questions"])
    idx = st.session_state.q_index
    prog = idx / total_q if total_q else 0.0

    st.header(theme["title"])
    st.caption(theme["intro"])

    st.progress(prog)
    st.caption(f"Progresso: {idx}/{total_q}")
    st.divider()

    q = current_question()
    st.subheader(f"Pergunta {idx + 1} de {total_q}")

    _show_question_image(q)

    st.write(q["text"])

    options = [o["id"] for o in q["options"]]
    labels = {o["id"]: o["label"] for o in q["options"]}

    with st.form(key=f"form_{q['id']}"):
        choice = st.radio(
            "Escolha uma opção:",
            options=options,
            format_func=lambda x: labels[x],
            index=0,
            key=f"radio_{q['id']}",
        )
        submitted = st.form_submit_button("Confirmar")

    if submitted:
        record_answer(q["id"], choice)
        next_step()
        st.rerun()
