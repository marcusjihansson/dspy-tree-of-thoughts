import hashlib
import json
from collections import defaultdict
from pathlib import Path


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
      - search_history: list (optional)
      - metrics: dict (optional)
    """
    # Already in new schema
    required_new = {
        "query_id",
        "tier",
        "strategy",
        "execution_time",
        "success",
        "evaluation_score",
        "steps_taken",
    }
    if required_new.issubset(raw.keys()):
        # Ensure optional keys exist
        raw.setdefault("question", "")
        raw.setdefault("final_answer", "")
        raw.setdefault("individual_scores", [])
        raw.setdefault("n_evaluations", 0)
        raw.setdefault("search_history", [])
        raw.setdefault("metrics", {})
        return raw

    # Legacy single-result schema (no tier/query_id)
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
            "search_history": raw.get("search_history", []),
            "metrics": raw.get("metrics", {}),
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


def _safe_div(a, b):
    return a / b if b else 0.0


def _mean_std(xs):
    n = len(xs)
    if n == 0:
        return 0.0, 0.0
    m = sum(xs) / n
    var = sum((x - m) ** 2 for x in xs) / n
    return m, var**0.5


def _hash(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


def comparative_analysis(entries):
    by_strategy = defaultdict(list)
    by_tier = defaultdict(list)
    by_query = defaultdict(list)

    for e in entries:
        by_strategy[e["strategy"]].append(e)
        by_tier[e["tier"]].append(e)
        by_query[e["query_id"]].append(e)

    results = {"by_strategy": {}, "by_tier": {}, "by_query": {}}

    print("Comparative Analysis of Search Strategies")
    print("=" * 60)

    # Overall by Strategy with dispersion and metrics
    print("\n== Overall by Strategy ==")
    for s, g in by_strategy.items():
        times = [x["execution_time"] for x in g]
        steps = [x["steps_taken"] for x in g]
        scores = [x["evaluation_score"] for x in g]
        success = [1.0 if x["success"] else 0.0 for x in g]
        total_steps = sum(steps)
        total_time = sum(times)
        avg_time, std_time = _mean_std(times)
        avg_steps, std_steps = _mean_std(steps)
        avg_score, std_score = _mean_std(scores)
        success_rate = sum(success) / len(success) if success else 0.0
        time_per_step = _safe_div(total_time, total_steps)

        # Aggregated metrics if present
        gen_counts = [x.get("metrics", {}).get("total_generated", 0) for x in g]
        eval_counts = [x.get("metrics", {}).get("total_evaluated", 0) for x in g]
        gen_calls = [x.get("metrics", {}).get("generate_calls", 0) for x in g]
        eval_calls = [x.get("metrics", {}).get("evaluate_calls", 0) for x in g]

        avg_gen, std_gen = _mean_std(gen_counts)
        avg_eval, std_eval = _mean_std(eval_counts)
        avg_gen_calls, _ = _mean_std(gen_calls)
        avg_eval_calls, _ = _mean_std(eval_calls)

        strategy_data = {
            "n": len(g),
            "avg_time": avg_time,
            "std_time": std_time,
            "avg_steps": avg_steps,
            "std_steps": std_steps,
            "time_per_step": time_per_step,
            "success_rate": success_rate,
            "avg_score": avg_score,
            "std_score": std_score,
            "avg_gen": avg_gen,
            "std_gen": std_gen,
            "avg_eval": avg_eval,
            "std_eval": std_eval,
            "avg_gen_calls": avg_gen_calls,
            "avg_eval_calls": avg_eval_calls,
        }
        results["by_strategy"][s] = strategy_data

        print(
            f"{s:12} n={len(g):2} "
            f"avg_time={avg_time:.3f}±{std_time:.3f}s "
            f"steps={avg_steps:.2f}±{std_steps:.2f} "
            f"time/step={time_per_step:.3f}s "
            f"success={success_rate:.2f} "
            f"avg_score={avg_score:.2f}±{std_score:.2f} "
            f"gen={avg_gen:.1f} eval={avg_eval:.1f} "
            f"gen_calls={avg_gen_calls:.1f} eval_calls={avg_eval_calls:.1f}"
        )

    # By Tier
    print("\n== By Tier ==")
    for t, g in by_tier.items():
        times = [x["execution_time"] for x in g]
        steps = [x["steps_taken"] for x in g]
        scores = [x["evaluation_score"] for x in g]
        total_steps = sum(steps)
        total_time = sum(times)
        avg_time, std_time = _mean_std(times)
        avg_steps, std_steps = _mean_std(steps)
        avg_score, std_score = _mean_std(scores)
        success_rate = sum(1 for x in g if x["success"]) / len(g) if g else 0.0
        time_per_step = _safe_div(total_time, total_steps)

        tier_data = {
            "n": len(g),
            "avg_time": avg_time,
            "std_time": std_time,
            "avg_steps": avg_steps,
            "std_steps": std_steps,
            "time_per_step": time_per_step,
            "success_rate": success_rate,
            "avg_score": avg_score,
            "std_score": std_score,
        }
        results["by_tier"][t] = tier_data

        print(
            f"{t:12} n={len(g):2} "
            f"avg_time={avg_time:.3f}±{std_time:.3f}s "
            f"steps={avg_steps:.2f}±{std_steps:.2f} "
            f"time/step={time_per_step:.3f}s "
            f"success={success_rate:.2f} "
            f"avg_score={avg_score:.2f}±{std_score:.2f}"
        )

    # Per Query summary
    print("\n== Per Query Summary (winner by time among successful runs) ==")
    for q, g in sorted(by_query.items()):
        rows = []
        for e in g:
            row = {
                "strategy": e["strategy"],
                "time": e["execution_time"],
                "steps": e["steps_taken"],
                "success": e["success"],
                "score": e["evaluation_score"],
                "answer_hash": _hash(e.get("final_answer", "")),
                "gen": e.get("metrics", {}).get("total_generated", 0),
                "eval": e.get("metrics", {}).get("total_evaluated", 0),
            }
            rows.append(row)
        winners = [r for r in rows if r["success"]]
        winner = (
            min(winners, key=lambda r: r["time"])["strategy"] if winners else "none"
        )
        hashes = {r["answer_hash"] for r in rows}
        answers_identical = len(hashes) == 1

        query_data = {
            "winner": winner,
            "answers_identical": answers_identical,
            "results": rows,
        }
        results["by_query"][q] = query_data

        print(f"{q}: winner={winner}, answers_identical={answers_identical}")
        for r in sorted(rows, key=lambda x: x["time"]):
            print(
                f"  - {r['strategy']:10} time={r['time']:.4f}s steps={r['steps']:2} "
                f"success={int(r['success'])} score={r['score']:.1f} gen={r['gen']} eval={r['eval']}"
            )

    return results


def main():
    entries = load_results()
    if not entries:
        print("No results found in test/results/")
        return
    output = comparative_analysis(entries)
    Path("test/analysis/analysis_results/").mkdir(parents=True, exist_ok=True)
    with open(
        file=f"test/analysis/analysis_results/comparative_analysis_result.json",
        mode="w",
    ) as f:
        json.dump(output, f, indent=2)


if __name__ == "__main__":
    main()
