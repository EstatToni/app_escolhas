"""Página do Jogo 2 — Roleta ANIMADA com Matplotlib."""

import math
import random
import time
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

from games.roleta.core.loader import load_roleta_questions
from games.roleta.core.state import init_roleta_state, reset_roleta


# ---------------------------------------------------------------------
# Utilidades de desenho da roleta
# ---------------------------------------------------------------------
def _hsl_to_rgb(h: float, s: float, l: float) -> tuple[float, float, float]:
    """Converte HSL para RGB normalizado 0–1."""
    def hue2rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p

    if s == 0:
        return (l, l, l)
    q = l * (1 + s) if l < 0.5 else l + s - l*s
    p = 2*l - q
    r = hue2rgb(p, q, h + 1/3)
    g = hue2rgb(p, q, h)
    b = hue2rgb(p, q, h - 1/3)
    return (r, g, b)


def _generate_colors(n: int) -> List[str]:
    """Gera n cores bem distintas (HSL → HEX)."""
    out = []
    for i in range(n):
        h = (i / n) % 1.0
        s = 0.70
        l = 0.48
        r, g, b = _hsl_to_rgb(h, s, l)
        out.append("#%02x%02x%02x" % (int(r*255), int(g*255), int(b*255)))
    return out


def _draw_wheel(labels: list[str], angle: float, highlight: int | None):
    """Desenha a roleta com ângulo e highlight opcionais."""
    n = len(labels)
    colors = _generate_colors(n)
    fracs = [1/n] * n

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    fig.subplots_adjust(0.02, 0.02, 0.98, 0.98)

    wedges, _ = ax.pie(
        fracs,
        colors=colors,
        startangle=angle,
        counterclock=True,
        wedgeprops=dict(width=0.88, edgecolor="white", linewidth=1.2),
    )

    # Rótulos curtos internos
    for i, w in enumerate(wedges):
        ang = (w.theta2 + w.theta1) / 2
        txt = labels[i][:18] + ("…" if len(labels[i]) > 18 else "")
        r = 0.62
        ax.text(
            r * math.cos(math.radians(ang)),
            r * math.sin(math.radians(ang)),
            txt,
            ha="center",
            va="center",
            fontsize=9,
            rotation=ang,
            rotation_mode="anchor",
            color="white",
        )

    # Ponteiro
    ax.annotate(
        "",
        xy=(0, 0.98),
        xytext=(0, 0.72),
        arrowprops=dict(arrowstyle="-|>", lw=2.0),
    )

    # Destaque final
    if highlight is not None:
        wedges[highlight].set_edgecolor("#FFD54F")
        wedges[highlight].set_linewidth(4)

    ax.set_aspect("equal")
    ax.axis("off")
    return fig


# ---------------------------------------------------------------------
# Lógica de rotação
# ---------------------------------------------------------------------
def _slice_index_under_pointer(n: int, angle: float) -> int:
    """Descobre qual segmento está no ponteiro (topo)."""
    deg = (90 - (angle % 360)) % 360
    return int(deg // (360 / n))


def _ease_out(t: float) -> float:
    """Easing cúbico suave."""
    x = 1 - t
    return 1 - x * x * x


def _compute_final_angle(n: int, target_idx: int, angle_start: float) -> float:
    """Gera ângulo final garantindo que caia no índice alvo."""
    slice_deg = 360 / n
    center = target_idx * slice_deg + slice_deg/2
    base = (90 - center) % 360
    spins = random.randint(3, 6)
    jitter = random.uniform(-slice_deg*0.25, slice_deg*0.25)
    final = base + spins*360 + jitter

    # garantir continuidade (não voltar)
    if final < angle_start:
        k = math.ceil((angle_start - final) / 360)
        final += 360*k

    return final


# ---------------------------------------------------------------------
# Página do jogo
# ---------------------------------------------------------------------
def page_roleta() -> None:
    """Renderiza o jogo 2 — Roleta animada."""
    qs = load_roleta_questions()
    init_roleta_state(qs)

    st.title("🌀 Jogo 2 — Roleta de Perguntas")

    left = st.session_state.roleta_left
    st.caption(f"Perguntas restantes: **{len(left)}**")
    st.divider()

    # Se acabou
    if not left:
        st.success("✨ Todas as perguntas foram usadas!")
        if st.button("🔁 Reiniciar"):
            reset_roleta()
            st.rerun()
        return

    # Frame inicial
    labels = list(left)
    angle = st.session_state.get("roleta_angle", 0.0)

    container = st.empty()
    fig = _draw_wheel(labels, angle, highlight=None)
    container.pyplot(fig)

    # Botões
    if st.button("🎯 Girar", type="primary"):
        n = len(labels)
        # index alvo aleatório
        idx = random.randrange(n)
        final_angle = _compute_final_angle(n, idx, angle)

        # animação
        frames = 40
        for i in range(frames):
            t = (i+1)/frames
            a = angle + (final_angle - angle) * _ease_out(t)
            fig = _draw_wheel(labels, a, highlight=None)
            container.pyplot(fig)
            time.sleep(0.025)

        # fixar estado
        st.session_state.roleta_angle = final_angle % 360
        st.session_state.roleta_last = labels[
            _slice_index_under_pointer(n, st.session_state.roleta_angle)
        ]

        # destaque final
        idx_final = labels.index(st.session_state.roleta_last)
        fig = _draw_wheel(labels, st.session_state.roleta_angle, highlight=idx_final)
        container.pyplot(fig)

    # Pergunta sorteada
    last = st.session_state.roleta_last
    if last:
        st.subheader("Pergunta sorteada:")
        st.markdown(f"### {last}")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("✅ Marcar como usada"):
                if last in left:
                    left.remove(last)
                st.session_state.roleta_last = None
                st.rerun()
        with c2:
            if st.button("↻ Girar novamente"):
                st.session_state.roleta_last = None
                st.rerun()

    st.divider()

    if st.button("⟵ Voltar ao início"):
        from app import go_hub
        go_hub()
