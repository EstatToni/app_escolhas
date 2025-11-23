"""Tela inicial do Jogo 1: grid de temas, pré-requisitos e thumbnails."""

from pathlib import Path

import streamlit as st

from games.quiz.core.state import start_quiz
from games.quiz.core.theme_io import load_theme, load_theme_files

ROOT_DIR = Path(__file__).resolve().parents[3]


def _load_all_themes() -> list[dict]:
    """Carrega todos os JSONs do diretório `themes/`."""
    items: list[dict] = []
    for p in load_theme_files():
        data = load_theme(p)
        items.append(
        {
            "id": data["id"],
            "title": data["title"],
            "requires": data.get("requires"),
            "requires_any": data.get("requires_any"),
            "path": p,
            "raw": data,
        }
        )
    return items


def _iterify(x: object) -> list[str]:
    """Converte entrada em lista de strings.

    Regras:
    - None → []
    - "abc" → ["abc"]
    - lista/tupla/conjunto → cada item convertido para string.
    - Qualquer outro tipo → []
    """
    if not x:
        return []
    if isinstance(x, str):
        return [x]
    if isinstance(x, (list, tuple, set)):
        return [str(i) for i in x]
    return []


def _is_unlocked(req_all: object,
                 req_any: object,
                 completed_ids: set[str]) -> bool:
    """Determina se um tema está liberado para o usuário.

    Um tema pode declarar:
    - requires: todos devem estar concluídos
    - requires_any: pelo menos um deve estar concluído

    A função retorna True se ambos os critérios forem satisfeitos.
    """
    need_all = _iterify(req_all)
    need_any = _iterify(req_any)

    ok_all = all(r in completed_ids for r in need_all)
    ok_any = True if not need_any else any(r in completed_ids
                                            for r in need_any)

    return ok_all and ok_any


def _requirements_label(req_all: object,
                        req_any: object,
                        title_by_id: dict[str, str]) -> str:
    """Gera uma string amigável descrevendo pré-requisitos.

    Exemplos:
    - Apenas requires → "Tema A + Tema B"
    - Apenas requires_any → "Tema A ou Tema B"
    - Ambos → "(Tema A + Tema B) e (Tema C ou Tema D)"
    """
    names_all = [title_by_id.get(r, r) for r in _iterify(req_all)]
    names_any = [title_by_id.get(r, r) for r in _iterify(req_any)]

    parts: list[str] = []
    if names_all:
        parts.append(" + ".join(names_all))
    if names_any:
        parts.append(" ou ".join(names_any))

    if not parts:
        return ""
    if len(parts) == 2:
        return f"({parts[0]}) e ({parts[1]})"
    return parts[0]


def _find_theme_media(theme_raw: dict) -> Path | None:
    """Localiza a thumbnail do tema.

    Regras:
    1) Se o JSON tiver "thumbnail", tenta usar.
    2) Caso contrário, procura automaticamente em:
       assets/<pasta_do_tema>/{thumb,cover,card}.* (png/jpg/webp/gif)
    """
    th = theme_raw.get("thumbnail")
    if th:
        p = Path(th)
        if not p.is_absolute():
            p = ROOT_DIR / p
        if p.exists():
            return p

    theme_id = theme_raw.get("id", "tema")
    folder = theme_id.split("_v")[0]
    base = ROOT_DIR / "assets" / folder

    for name in ("thumb", "cover", "card", "_thumb", "_cover"):
        for ext in ("png", "jpg", "jpeg", "webp", "gif"):
            p = base / f"{name}.{ext}"
            if p.exists():
                return p

    return None


def _render_theme_card(theme_raw: dict,
                       completed_ids: set[str],
                       title_by_id: dict[str, str]) -> None:
    """Renderiza um card completo para um tema do Quiz.

    O card contém:
    - título
    - status (Disponível / Bloqueado)
    - imagem (thumbnail)
    - introdução
    - botão 'Começar' ou 'Bloqueado'
    """
    theme_id = theme_raw.get("id", "")
    title = theme_raw.get("title", theme_id)
    intro = theme_raw.get("intro", "")
    req_all = theme_raw.get("requires")
    req_any = theme_raw.get("requires_any")

    unlocked = _is_unlocked(req_all, req_any, completed_ids)

    with st.container(border=True):
        # Linha superior: Título à esquerda e status à direita.
        top_cols = st.columns([0.78, 0.22])
        with top_cols[0]:
            st.markdown(f"### {title}")
        with top_cols[1]:
            if unlocked:
                st.markdown(
                '<div style="text-align:right; white-space:nowrap;">'
                '✅ <b>Disponível</b></div>',
                unsafe_allow_html=True,
                )
            else:
                need = _requirements_label(req_all, req_any, title_by_id)
                st.markdown(
                '<div style="text-align:right; white-space:nowrap;">'
                '🔒 <b>Bloqueado</b></div>',
                unsafe_allow_html=True,
                )
                if need:
                    st.markdown(
                    '<div style="text-align:right; white-space:nowrap; '
                    'overflow:hidden; text-overflow:ellipsis;">'
                    f'Conclua: {need}</div>',
                    unsafe_allow_html=True,
                )

        # Imagem
        media = _find_theme_media(theme_raw)
        if media:
            st.image(str(media), width="stretch")

        # Introdução opcional
        if intro:
            st.caption(intro)

        # Botão
        btn_key = f"play_{theme_id}"
        if unlocked:
            if st.button("▶️ Começar", key=btn_key, width="stretch"):
                start_quiz(theme_raw)
                st.rerun()
        else:
            st.button("Bloqueado", key=f"{btn_key}_locked", disabled=True,
                    width="stretch")


def page_home() -> None:
    """Tela principal do Jogo 1.

    Mostra:
    - Título
    - Barra de progresso dos temas concluídos
    - Grid 2xN com todos os temas ordenados
    """
    st.title("Jogo das Escolhas")
    st.caption("Escolha um tema e siga o instinto.")

    items = _load_all_themes()
    title_by_id = {
        it.get("id", ""): it.get("title", it.get("id", "")) for it in items
    }

    # Ordem fixa desejada (IDs reais dos seus JSONs)
    custom_order = [
        "criaturas_eletricas_v1",
        "musica_persona_v1",
        "surpresa_v1",
    ]
    rank = {k: i for i, k in enumerate(custom_order)}

    # Temas não listados → vão pro final em ordem alfabética
    items_sorted = sorted(
        items,
        key=lambda it: (
            rank.get(it.get("id", ""), 10**6),
            it.get("title", it.get("id", "")),
        ),
    )

    # Progresso
    completed_ids = set(st.session_state.get("completed", []))
    total = len(items_sorted)
    done = len(completed_ids & {it.get("id", "") for it in items_sorted})

    cols_prog = st.columns([0.7, 0.3])
    with cols_prog[0]:
        st.progress(done / total if total else 0.0, text=f"{done}/{total}")
    with cols_prog[1]:
        st.write("")

    st.divider()

    # Grid de cards → 2 colunas
    cols = st.columns(2)
    for i, it in enumerate(items_sorted):
        theme_raw = it.get("raw", it)
        with cols[i % 2]:
            _render_theme_card(theme_raw, completed_ids, title_by_id)
