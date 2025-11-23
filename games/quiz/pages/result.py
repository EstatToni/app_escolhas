"""Página de resultado do quiz, com imagem/gif e convite Surpresa."""

from pathlib import Path
from typing import List, Tuple, Union

import streamlit as st

from games.quiz.core.engine import apply_variant, compute_result
from games.quiz.core.state import mark_completed, reset_app, start_quiz

# Importa o composer se existir; caso contrário, funciona sem convite.
try:
    from games.quiz.core.composer import (  # type: ignore
        collect_plan,
        compose_invite,
    )
    _HAS_COMPOSER = True
except Exception:  # noqa: BLE001
    collect_plan = None  # type: ignore
    compose_invite = None  # type: ignore
    _HAS_COMPOSER = False

ROOT_DIR = Path(__file__).resolve().parents[3]


def _resolve_path(path_str: str) -> Path:
    """Resolve caminhos relativos ao diretório raiz do projeto."""
    p = Path(path_str)
    if not p.is_absolute():
        p = ROOT_DIR / p
    return p


def _render_result_card(block: dict) -> None:
    """Desenha o cartão do resultado (prefere GIF se existir)."""
    media_path = block.get("image_gif") or block.get("image")
    if media_path:
        p = _resolve_path(media_path)
        if p.exists():
            st.image(str(p))
        else:
            st.caption(f"[mídia do resultado não encontrada: {p}]")
            st.caption("→ Coloque o arquivo nesse caminho exato.")

    with st.container():
        st.success(block["title"])
        st.markdown(block["body"])


def _answers_to_pairs(
    answers: Union[
        List[Tuple[str, str]],
        List[dict],
        dict,
    ]
) -> List[Tuple[str, str]]:
    """Normaliza respostas em lista de pares (q_id, opt_id)."""
    pairs: List[Tuple[str, str]] = []

    if isinstance(answers, dict):
        for k, v in answers.items():
            if isinstance(k, str) and isinstance(v, str):
                pairs.append((k, v))
        return pairs

    if isinstance(answers, list):
        for item in answers:
            if isinstance(item, tuple) and len(item) == 2:
                q_id, opt_id = item
                if isinstance(q_id, str) and isinstance(opt_id, str):
                    pairs.append((q_id, opt_id))
            elif isinstance(item, dict):
                q_id = (
                    item.get("q")
                    or item.get("question")
                    or item.get("qid")
                    or item.get("id")
                )
                opt_id = (
                    item.get("a")
                    or item.get("answer")
                    or item.get("opt")
                    or item.get("option")
                )
                if isinstance(q_id, str) and isinstance(opt_id, str):
                    pairs.append((q_id, opt_id))
    return pairs


def _render_surprise_invite(theme: dict) -> None:
    """Se for o tema Surpresa, gera e mostra o convite personalizado."""
    is_surprise = theme.get("id", "").startswith("surpresa")
    has_map = bool(theme.get("compose_map"))
    if not (is_surprise or has_map):
        return

    if not _HAS_COMPOSER:
        st.info(
            "Para montar o convite automaticamente, crie "
            "`core/composer.py` e adicione `compose_map` no JSON "
            "do tema Surpresa."
        )
        return

    # Normaliza respostas e compõe o convite.
    pairs = _answers_to_pairs(st.session_state.answers)
    plan = collect_plan(theme, pairs)  # type: ignore[misc]
    invite = compose_invite(theme, plan)  # type: ignore[misc]

    if invite.strip():
        st.divider()
        st.subheader("Convite")
        st.markdown(invite)


def page_result() -> None:
    """Renderiza o resultado final; aplica variante e ações."""
    theme = st.session_state.theme
    mark_completed(theme["id"])

    key, base = compute_result(
        scores=st.session_state.scores,
        theme=theme,
        answers=st.session_state.answers,
    )
    block = apply_variant(base, theme, st.session_state.answers)

    _render_result_card(block)
    _render_surprise_invite(theme)

    st.divider()
    c1, _, c3 = st.columns([1, 1, 1])
    with c1:
        if st.button("↻ Rejogar este tema"):
            start_quiz(theme)
            st.rerun()
    with c3:
        if st.button("⟵ Voltar ao início"):
            reset_app()
            st.rerun()
