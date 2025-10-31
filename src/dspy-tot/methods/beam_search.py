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

        # instrumentation
        total_generated = 0
        total_evaluated = 0
        generate_calls = 0
        evaluate_calls = 0
        
        for step in range(max_steps):
            all_candidates = []
            
            # Generate candidates from each state in beam
            step_generate_calls = 0
            for state in current_beam:
                candidates = generate_fn(state, kwargs.get('n_generate', 3))
                all_candidates.extend(candidates)
                step_generate_calls += 1

            generate_calls += step_generate_calls
            total_generated += len(all_candidates)
            
            if not all_candidates:
                break
            
            # Evaluate all candidates
            values = evaluate_fn(all_candidates)
            evaluate_calls += 1
            total_evaluated += len(all_candidates)
            
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
                    'success': True,
                    'metrics': {
                        'total_generated': total_generated,
                        'total_evaluated': total_evaluated,
                        'generate_calls': generate_calls,
                        'evaluate_calls': evaluate_calls,
                    },
                }
            
            # Update beam
            current_beam = [state for state, _ in candidate_value_pairs[:beam_width]]
            
            search_history.append({
                'step': step,
                'beam_size': len(current_beam),
                'total_candidates': len(all_candidates),
                'best_value': candidate_value_pairs[0][1] if candidate_value_pairs else 0,
                'beam_states': current_beam,
                'generated_this_step': len(all_candidates),
                'evaluated_this_step': len(all_candidates),
                'generate_calls_this_step': step_generate_calls,
                'evaluate_calls_this_step': 1,
            })
        
        return {
            'final_states': current_beam,
            'search_history': search_history,
            'strategy': 'Beam',
            'steps_taken': max_steps,
            'success': False,
            'metrics': {
                'total_generated': total_generated,
                'total_evaluated': total_evaluated,
                'generate_calls': generate_calls,
                'evaluate_calls': evaluate_calls,
            },
        }