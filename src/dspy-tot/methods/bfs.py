"""
Breadth-First Search strategy for Tree-of-Thought reasoning.
Original ToT approach - explores all nodes at current depth before going deeper.
"""

from typing import List, Dict, Any, Callable
from .base import SearchStrategy


class BreadthFirstSearch(SearchStrategy):
    """Breadth-First Search - explores all nodes at current depth before going deeper."""
    
    def search(self, 
               initial_state: str,
               generate_fn: Callable[[str, int], List[str]],
               evaluate_fn: Callable[[List[str]], List[float]],
               is_goal_fn: Callable[[str], bool],
               max_steps: int,
               n_select: int = 2,
               **kwargs) -> Dict[str, Any]:
        
        current_states = [initial_state]
        search_history = []
        
        for step in range(max_steps):
            # Generate candidates from all current states
            all_candidates = []
            for state in current_states:
                candidates = generate_fn(state, kwargs.get('n_generate', 3))
                all_candidates.extend(candidates)
            
            if not all_candidates:
                break
            
            # Evaluate candidates
            values = evaluate_fn(all_candidates)
            
            # Select top candidates
            candidate_value_pairs = list(zip(all_candidates, values))
            candidate_value_pairs.sort(key=lambda x: x[1], reverse=True)
            
            selected_candidates = [pair[0] for pair in candidate_value_pairs[:n_select]]
            
            # Check for goal states
            goal_states = [state for state in selected_candidates if is_goal_fn(state)]
            if goal_states:
                return {
                    'final_states': goal_states,
                    'search_history': search_history,
                    'strategy': 'BFS',
                    'steps_taken': step + 1,
                    'success': True
                }
            
            search_history.append({
                'step': step,
                'candidates': all_candidates,
                'values': values,
                'selected': selected_candidates
            })
            
            current_states = selected_candidates
        
        return {
            'final_states': current_states,
            'search_history': search_history,
            'strategy': 'BFS',
            'steps_taken': max_steps,
            'success': False
        }

