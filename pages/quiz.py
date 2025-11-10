"""Página de perguntas do quiz, com barra e imagem por pergunta."""

from pathlib import Path

import streamlit as st

from core.state import current_question, record_answer, next_step


def _show_question_image(q: dict):
    """Exibe imagem se existir; senão, mostra lembrete de caminho."""
    path = q.get("image")
    alt = q.get("image_alt", "Imagem ilustrativa")
    if not path:
        return
    p = Path(path)
    if p.exists():
        st.image(str(p), caption=None)
    else:
        st.caption(f"[adicione a imagem em: {path}]")
        # dica: coloque a imagem local no caminho acima


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
