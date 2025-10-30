"""
Beam Search strategy for Tree-of-Thought reasoning.
Keeps top-k candidates at each step for efficient exploration.
"""

from typing import List, Dict, Any, Callable
from .base import SearchStrategy


class BeamSearch(SearchStrategy):
    """Beam Search - keeps top-k candidates at each step."""
    
    def search(self, 
               initial_state: str,
               generate_fn: Callable[[str, int], List[str]],
               evaluate_fn: Callable[[List[str]], List[float]],
               is_goal_fn: Callable[[str], bool],
               max_steps: int,
               beam_width: int = 3,
               **kwargs) -> Dict[str, Any]:
        
        current_beam = [initial_state]
        search_history = []
        
        for step in range(max_steps):
            all_candidates = []
            
            # Generate candidates from each state in beam
            for state in current_beam:
                candidates = generate_fn(state, kwargs.get('n_generate', 3))
                all_candidates.extend(candidates)
            
            if not all_candidates:
                break
            
            # Evaluate all candidates
            values = evaluate_fn(all_candidates)
            
            # Keep top beam_width candidates
            candidate_value_pairs = list(zip(all_candidates, values))
            candidate_value_pairs.sort(key=lambda x: x[1], reverse=True)
            
            # Check for goal states
            goal_states = [state for state, _ in candidate_value_pairs if is_goal_fn(state)]
            if goal_states:
                return {
                    'final_states': goal_states[:1],  # Return best goal state
                    'search_history': search_history,
                    'strategy': 'Beam',
                    'steps_taken': step + 1,
                    'success': True
                }
            
            # Update beam
            current_beam = [state for state, _ in candidate_value_pairs[:beam_width]]
            
            search_history.append({
                'step': step,
                'beam_size': len(current_beam),
                'total_candidates': len(all_candidates),
                'best_value': candidate_value_pairs[0][1] if candidate_value_pairs else 0,
                'beam_states': current_beam
            })
        
        return {
            'final_states': current_beam,
            'search_history': search_history,
            'strategy': 'Beam',
            'steps_taken': max_steps,
            'success': False
        }