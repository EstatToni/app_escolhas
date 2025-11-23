"""Funções para compor o convite final do tema Surpresa."""

from typing import Dict, List, Tuple


def collect_plan(theme: dict, answers: List[Tuple[str, str]]) -> Dict[str, str]:
    """Coleta o dicionário plan selecionado em cada pergunta."""
    q_index = {q["id"]: q for q in theme.get("questions", [])}
    plan: Dict[str, str] = {}
    for q_id, opt_id in answers:
        q = q_index.get(q_id)
        if not q:
            continue
        opt = next((o for o in q.get("options", []) if o.get("id") == opt_id),
                   None)
        if not opt:
            continue
        opt_plan = opt.get("plan", {})
        for k, v in opt_plan.items():
            plan[k] = v
    return plan


def compose_invite(theme: dict, plan: Dict[str, str]) -> str:
    """Gera o texto do convite a partir de compose_map e compose_order."""
    cmap = theme.get("compose_map", {})
    order = theme.get("compose_order", [])
    parts: List[str] = []

    # Frases principais em ordem intuitiva
    horario = _phrase(cmap, "horario", plan.get("horario"))
    lugar = _phrase(cmap, "lugar", plan.get("lugar"))
    vibe = _phrase(cmap, "vibe", plan.get("vibe"))
    atividade = _phrase(cmap, "atividade", plan.get("atividade"))
    comida = _phrase(cmap, "comida", plan.get("comida"))
    bebida = _phrase(cmap, "bebida", plan.get("bebida"))
    som = _phrase(cmap, "som", plan.get("som"))
    transporte = _phrase(cmap, "transporte", plan.get("transporte"))
    orcamento = _phrase(cmap, "orcamento", plan.get("orcamento"))
    dress = _phrase(cmap, "dress", plan.get("dress"))
    gesto = _phrase(cmap, "gesto", plan.get("gesto"))
    clima = _phrase(cmap, "clima", plan.get("clima"))

    if horario:
        parts.append(f"Que tal {horario}?")
    if lugar and vibe:
        parts.append(f"Pensei em {lugar} com clima {vibe}.")
    elif lugar:
        parts.append(f"Pensei em {lugar}.")
    if atividade:
        parts.append(f"A ideia é {atividade}.")
    if comida and bebida:
        parts.append(f"Pra comer, {comida}; pra beber, {bebida}.")
    elif comida:
        parts.append(f"Pra comer, {comida}.")
    elif bebida:
        parts.append(f"Pra beber, {bebida}.")
    if som:
        parts.append(f"Música em volume {som}.")
    if transporte:
        parts.append(f"Vamos {transporte}.")
    if orcamento:
        parts.append(f"Orçamento {orcamento}.")
    if dress:
        parts.append(f"Dress code {dress}.")
    if gesto:
        parts.append(f"Gesto extra: {gesto}.")
    if clima:
        parts.append(f"Se chover, {clima}.")

    parts.append("Se topar, eu organizo tudo do jeitinho que você escolheu. :)")
    return " ".join(parts)


def _phrase(cmap: dict, key: str, value: str) -> str:
    """Resolve a frase amigável para um valor do plano."""
    if not value:
        return ""
    return cmap.get(key, {}).get(value, "")
