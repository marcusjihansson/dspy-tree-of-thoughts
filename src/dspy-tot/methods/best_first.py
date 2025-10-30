"""
Best-First Search strategy for Tree-of-Thought reasoning.
Greedy algorithm that always picks the best heuristic value.
"""

import heapq
from typing import List, Dict, Any, Callable
from .base import SearchStrategy


class BestFirstSearch(SearchStrategy):
    """Best-First Search (Greedy) - always picks best heuristic value."""
    
    def search(self, 
               initial_state: str,
               generate_fn: Callable[[str, int], List[str]],
               evaluate_fn: Callable[[List[str]], List[float]],
               is_goal_fn: Callable[[str], bool],
               max_steps: int,
               **kwargs) -> Dict[str, Any]:
        
        # Priority queue: (-value, state, path) - negative for max heap behavior
        open_set = [(0.0, initial_state, [initial_state])]
        visited = set()
        search_history = []
        step = 0
        
        while open_set and step < max_steps:
            # Get state with best heuristic value
            neg_value, current_state, path = heapq.heappop(open_set)
            
            if current_state in visited:
                continue
            
            visited.add(current_state)
            
            # Check if goal reached
            if is_goal_fn(current_state):
                return {
                    'final_states': [current_state],
                    'search_history': search_history,
                    'strategy': 'Best-First',
                    'steps_taken': step,
                    'success': True,
                    'best_path': path
                }
            
            # Generate successors
            candidates = generate_fn(current_state, kwargs.get('n_generate', 3))
            if candidates:
                values = evaluate_fn(candidates)
                
                for candidate, value in zip(candidates, values):
                    if candidate not in visited:
                        heapq.heappush(open_set, (-value, candidate, path + [candidate]))
            
            search_history.append({
                'step': step,
                'current_state': current_state,
                'current_value': -neg_value,
                'open_set_size': len(open_set),
                'visited_size': len(visited)
            })
            
            step += 1
        
        # Return best state found
        best_state = current_state if 'current_state' in locals() else initial_state
        
        return {
            'final_states': [best_state],
            'search_history': search_history,
            'strategy': 'Best-First',
            'steps_taken': step,
            'success': False
        }