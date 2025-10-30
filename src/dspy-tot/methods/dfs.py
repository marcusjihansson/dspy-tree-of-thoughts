"""
Depth-First Search strategy for Tree-of-Thought reasoning.
Good for crossword-like tasks and constraint satisfaction problems.
"""

from typing import List, Dict, Any, Callable
from .base import SearchStrategy


class DepthFirstSearch(SearchStrategy):
    """Depth-First Search - explores as far as possible before backtracking."""

    def search(
        self,
        initial_state: str,
        generate_fn: Callable[[str, int], List[str]],
        evaluate_fn: Callable[[List[str]], List[float]],
        is_goal_fn: Callable[[str], bool],
        max_steps: int,
        max_depth: int = 10,
        **kwargs,
    ) -> Dict[str, Any]:
        search_history = []
        best_states = []

        def dfs_recursive(state: str, depth: int, path: List[str]) -> bool:
            if depth >= max_depth or len(search_history) >= max_steps:
                return False

            if is_goal_fn(state):
                best_states.append(state)
                return True

            # Generate candidates
            candidates = generate_fn(state, kwargs.get("n_generate", 3))
            if not candidates:
                return False

            # Evaluate candidates
            values = evaluate_fn(candidates)

            # Sort by value (best first)
            candidate_value_pairs = list(zip(candidates, values))
            candidate_value_pairs.sort(key=lambda x: x[1], reverse=True)

            search_history.append(
                {
                    "step": len(search_history),
                    "depth": depth,
                    "state": state,
                    "candidates": candidates,
                    "values": values,
                    "path": path.copy(),
                }
            )

            # Explore each candidate depth-first
            for candidate, value in candidate_value_pairs:
                new_path = path + [candidate]
                if dfs_recursive(candidate, depth + 1, new_path):
                    return True

            return False

        found_goal = dfs_recursive(initial_state, 0, [initial_state])

        return {
            "final_states": best_states if best_states else [initial_state],
            "search_history": search_history,
            "strategy": "DFS",
            "steps_taken": len(search_history),
            "success": found_goal,
        }
