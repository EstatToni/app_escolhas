"""Motor de pontuação, desempate e variações condicionais."""

from typing import Dict, List, Tuple
from collections import Counter


def resolve_tie(candidates, theme, answers):
    """Resolve empates usando tie_breakers definidos no tema."""
    ans_map = {q: a for q, a in answers}
    q_index = {q["id"]: q for q in theme["questions"]}
    tb = theme.get("tie_breakers", [])

    for q_id in tb:
        if q_id not in ans_map:
            continue

        q = q_index[q_id]
        opt = next((o for o in q.get("options", [])
                    if o.get("id") == ans_map[q_id]), None)

        weights = opt.get("weights", {}) if opt else q.get("weights", {})

        best, best_val = None, -10**9
        vals = []

        for c in candidates:
            v = int(weights.get(c, 0))
            vals.append(v)
            if v > best_val:
                best, best_val = c, v

        if vals.count(best_val) == 1:
            return best

    return sorted(candidates)[0]


def compute_result(scores, theme, answers):
    """Determina o resultado final a partir do placar do quiz."""
    max_val = max(scores.values())
    candidates = [k for k, v in scores.items() if v == max_val]

    key = candidates[0] if len(candidates) == 1 else resolve_tie(candidates, theme, answers)
    return key, theme["results"][key]


def tally_signals(theme, answers):
    """Conta sinais (signals) marcados nas opções selecionadas."""
    counts = Counter()
    q_index = {q["id"]: q for q in theme["questions"]}

    for q_id, opt_id in answers:
        q = q_index.get(q_id)
        if not q:
            continue

        opt = next((o for o in q.get("options", []) if o.get("id") == opt_id), None)
        if not opt:
            continue

        for s in opt.get("signals", []):
            counts[s] += 1

    return dict(counts)


def apply_variant(block, theme, answers):
    """Aplica variante condicional ao resultado final."""
    variants = block.get("variants", [])
    if not variants:
        return block

    sigs = tally_signals(theme, answers)

    for v in variants:
        cond = v.get("when", {})
        sig = cond.get("signal")
        need = cond.get("min", 1)

        if sig and sigs.get(sig, 0) >= need:
            out = dict(block)
            if "body_prefix" in v:
                out["body"] = f"{v['body_prefix']} {out['body']}"
            if "body_suffix" in v:
                out["body"] = f"{out['body']} {v['body_suffix']}"
            return out

    return block
