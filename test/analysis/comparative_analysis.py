import json
from pathlib import Path
from collections import defaultdict


def _coerce_entry(raw: dict, file_path: Path) -> dict | None:
    """Coerce heterogeneous result JSONs into a common schema.
    Returns None if the entry cannot be coerced.
    Common schema keys:
      - query_id: str
      - tier: str
      - strategy: str
      - question: str
      - execution_time: float
      - success: bool
      - steps_taken: int
      - final_answer: str
      - evaluation_score: float
      - individual_scores: list
      - n_evaluations: int
    """
    # Already in new schema
    required_new = {"query_id", "tier", "strategy", "execution_time", "success", "evaluation_score", "steps_taken"}
    if required_new.issubset(raw.keys()):
        # Ensure optional keys exist
        raw.setdefault("question", "")
        raw.setdefault("final_answer", "")
        raw.setdefault("individual_scores", [])
        raw.setdefault("n_evaluations", 0)
        return raw

    # Legacy single-result schema (no tier/query_id), e.g., {"strategy": ..., "execution_time": ..., ...}
    if "strategy" in raw and "execution_time" in raw:
        stem = file_path.stem
        return {
            "query_id": stem,  # fallback to filename
            "tier": "legacy",
            "strategy": raw.get("strategy", "unknown"),
            "question": raw.get("question", ""),
            "execution_time": float(raw.get("execution_time", 0.0)),
            "success": bool(raw.get("success", False)),
            "steps_taken": int(raw.get("steps_taken", 0)),
            "final_answer": raw.get("final_answer", ""),
            "evaluation_score": float(raw.get("evaluation_score", 0.0)),
            "individual_scores": raw.get("individual_scores", []),
            "n_evaluations": int(raw.get("n_evaluations", 0)),
        }

    return None


def load_results():
    results_dir = Path("test/results")
    entries = []
    for f in results_dir.glob("*.json"):
        try:
            with open(f, "r", encoding="utf-8") as fh:
                raw = json.load(fh)
            coerced = _coerce_entry(raw, f)
            if coerced is not None:
                entries.append(coerced)
        except Exception:
            pass
    return entries


def agg(group):
    n = len(group)
    if n == 0:
        return {"n": 0, "avg_time": 0, "success_rate": 0, "avg_score": 0, "avg_steps": 0}
    return {
        "n": n,
        "avg_time": sum(g["execution_time"] for g in group) / n,
        "success_rate": sum(1 for g in group if g["success"]) / n,
        "avg_score": sum(g["evaluation_score"] for g in group) / n,
        "avg_steps": sum(g["steps_taken"] for g in group) / n,
    }


def comparative_analysis(entries):
    by_strategy = defaultdict(list)
    by_tier = defaultdict(list)
    by_query = defaultdict(list)

    for e in entries:
        by_strategy[e["strategy"]].append(e)
        by_tier[e["tier"]].append(e)
        by_query[e["query_id"]].append(e)

    print("Comparative Analysis of Search Strategies")
    print("=" * 60)

    print("\n== Overall by Strategy ==")
    for s, g in by_strategy.items():
        a = agg(g)
        print(f"{s:12} n={a['n']:2} avg_time={a['avg_time']:.2f}s success={a['success_rate']:.2f} avg_score={a['avg_score']:.2f} steps={a['avg_steps']:.2f}")

    print("\n== By Tier ==")
    for t, g in by_tier.items():
        a = agg(g)
        print(f"{t:12} n={a['n']:2} avg_time={a['avg_time']:.2f}s success={a['success_rate']:.2f} avg_score={a['avg_score']:.2f} steps={a['avg_steps']:.2f}")

    print("\n== Per Query Best Score ==")
    for q, g in by_query.items():
        best = max(g, key=lambda x: x["evaluation_score"])
        print(f"{q:6} -> {best['strategy']:12} score={best['evaluation_score']:.2f} time={best['execution_time']:.2f}s steps={best['steps_taken']}")


def main():
    entries = load_results()
    if not entries:
        print("No results found in test/results/")
        return
    comparative_analysis(entries)


if __name__ == "__main__":
    main()
