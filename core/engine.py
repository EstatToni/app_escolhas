"""Motor de pontuação, desempate e variações condicionais."""

from typing import Dict, List, Tuple
from collections import Counter


def resolve_tie(candidates, theme, answers):
    """Desempata usando tie_breakers; usa pesos da opção se houver."""
    ans_map = {q: a for q, a in answers}
    q_index = {q["id"]: q for q in theme["questions"]}
    tb = theme.get("tie_breakers", [])
    for q_id in tb:
        if q_id not in ans_map:
            continue
        q = q_index[q_id]
        # procurar pesos na opção escolhida
        opt_id = ans_map[q_id]
        opt = next((o for o in q.get("options", [])
                    if o.get("id") == opt_id), None)
        weights = {}
        if opt and isinstance(opt.get("weights"), dict):
            weights = opt["weights"]
        else:
            weights = q.get("weights", {})
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


def compute_result(
    scores: Dict[str, int],
    theme: Dict,
    answers: List[Tuple[str, str]],
) -> Tuple[str, Dict]:
    """Retorna (chave_resultado, bloco_resultado) do vencedor."""
    max_val = max(scores.values())
    candidates = [k for k, v in scores.items() if v == max_val]
    if len(candidates) == 1:
        key = candidates[0]
    else:
        key = resolve_tie(candidates, theme, answers)
    return key, theme["results"][key]


def tally_signals(theme: Dict, answers: List[Tuple[str, str]]) -> Dict[str, int]:
    """Conta sinais marcados nas opções escolhidas."""
    counts = Counter()
    q_index = {q["id"]: q for q in theme["questions"]}
    for q_id, opt_id in answers:
        q = q_index.get(q_id)
        if not q:
            continue
        opts = q.get("options", [])
        opt = next((o for o in opts if o.get("id") == opt_id), None)
        if not opt:
            continue
        for s in opt.get("signals", []):
            counts[s] += 1
    return dict(counts)


def apply_variant(block: Dict, theme: Dict,
                  answers: List[Tuple[str, str]]) -> Dict:
    """Aplica a primeira variante cujo 'when' casar com os sinais."""
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
                out["body"] = f"{v['body_prefix']} {out.get('body', '')}".strip()
            if "body_suffix" in v:
                out["body"] = f"{out.get('body', '')} {v['body_suffix']}".strip()
            return out
    return block
