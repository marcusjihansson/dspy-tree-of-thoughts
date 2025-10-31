"""
Monte Carlo Tree Search strategy for Tree-of-Thought reasoning.
Balances exploration and exploitation using simulations and UCB.
"""

import random
from typing import List, Dict, Any, Callable
from .base import SearchStrategy, SearchNode


class MonteCarloTreeSearch(SearchStrategy):
    """Monte Carlo Tree Search - balances exploration and exploitation."""

    def search(
        self,
        initial_state: str,
        generate_fn: Callable[[str, int], List[str]],
        evaluate_fn: Callable[[List[str]], List[float]],
        is_goal_fn: Callable[[str], bool],
        max_steps: int,
        simulations_per_step: int = 10,
        **kwargs,
    ) -> Dict[str, Any]:
        root = SearchNode(state=initial_state, path=[initial_state], depth=0, value=0.0)
        search_history = []

        # instrumentation
        self._metrics = {
            "total_generated": 0,
            "total_evaluated": 0,
            "generate_calls": 0,
            "evaluate_calls": 0,
        }

        for step in range(max_steps):
            best_reward = -float("inf")
            best_node = None

            # Run multiple simulations
            for sim in range(simulations_per_step):
                # Selection: find best node to expand
                node = self._select_node(root)

                # Expansion: add children if not terminal
                if not is_goal_fn(node.state) and not node.children:
                    self._expand_node(
                        node, generate_fn, evaluate_fn, kwargs.get("n_generate", 3)
                    )

                # Simulation: random rollout from expanded node
                reward = self._simulate(
                    node, generate_fn, evaluate_fn, is_goal_fn, max_depth=5
                )

                # Backpropagation: update values back to root
                self._backpropagate(node, reward)

                if reward > best_reward:
                    best_reward = reward
                    best_node = node

            # Check for goal
            if best_node and is_goal_fn(best_node.state):
                result = {
                    "final_states": [best_node.state],
                    "search_history": search_history,
                    "strategy": "MCTS",
                    "steps_taken": step + 1,
                    "success": True,
                    "best_path": best_node.path,
                    "metrics": self._metrics,
                }
                return result

            search_history.append(
                {
                    "step": step,
                    "best_node": best_node.state if best_node else root.state,
                    "best_reward": best_reward,
                    "tree_size": self._count_nodes(root),
                }
            )

        # Return best leaf node
        best_leaf = self._get_best_leaf(root)

        result = {
            "final_states": [best_leaf.state],
            "search_history": search_history,
            "strategy": "MCTS",
            "steps_taken": max_steps,
            "success": False,
            "best_path": best_leaf.path,
            "metrics": self._metrics,
        }
        return result

    def _select_node(self, node: SearchNode) -> SearchNode:
        """Select node using UCB policy."""
        while node.children:
            node = max(node.children, key=lambda x: x.ucb_value)
        return node

    def _expand_node(
        self,
        node: SearchNode,
        generate_fn: Callable,
        evaluate_fn: Callable,
        n_generate: int,
    ):
        """Expand node by adding children."""
        candidates = generate_fn(node.state, n_generate)
        # instrumentation
        self._metrics["generate_calls"] += 1
        self._metrics["total_generated"] += len(candidates)
        if candidates:
            values = evaluate_fn(candidates)
            # instrumentation
            self._metrics["evaluate_calls"] += 1
            self._metrics["total_evaluated"] += len(candidates)
            for candidate, value in zip(candidates, values):
                child = SearchNode(
                    state=candidate,
                    path=node.path + [candidate],
                    depth=node.depth + 1,
                    value=value,
                    parent=node,
                )
                node.children.append(child)

    def _simulate(
        self,
        node: SearchNode,
        generate_fn: Callable,
        evaluate_fn: Callable,
        is_goal_fn: Callable,
        max_depth: int = 5,
    ) -> float:
        """Random simulation from node."""
        current_state = node.state
        total_reward = node.value
        depth = 0

        while depth < max_depth and not is_goal_fn(current_state):
            candidates = generate_fn(
                current_state, 2
            )  # Fewer candidates for simulation
            # instrumentation
            self._metrics["generate_calls"] += 1
            self._metrics["total_generated"] += len(candidates)
            if not candidates:
                break

            # Random selection for simulation
            current_state = random.choice(candidates)
            values = evaluate_fn([current_state])
            # instrumentation
            self._metrics["evaluate_calls"] += 1
            self._metrics["total_evaluated"] += 1
            total_reward += values[0] if values else 0
            depth += 1

        # Bonus for reaching goal
        if is_goal_fn(current_state):
            total_reward += 10.0

        return total_reward

    def _backpropagate(self, node: SearchNode, reward: float):
        """Update node statistics back to root."""
        while node:
            node.visits += 1
            node.total_reward += reward
            node = node.parent

    def _count_nodes(self, node: SearchNode) -> int:
        """Count total nodes in tree."""
        count = 1
        for child in node.children:
            count += self._count_nodes(child)
        return count

    def _get_best_leaf(self, node: SearchNode) -> SearchNode:
        """Get leaf node with highest average reward."""
        if not node.children:
            return node

        best_child = max(node.children, key=lambda x: x.total_reward / max(x.visits, 1))
        return self._get_best_leaf(best_child)
