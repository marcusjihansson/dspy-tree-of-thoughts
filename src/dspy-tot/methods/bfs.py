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

        # instrumentation
        total_generated = 0
        total_evaluated = 0
        generate_calls = 0
        evaluate_calls = 0
        
        for step in range(max_steps):
            # Generate candidates from all current states
            all_candidates = []
            step_generate_calls = 0
            for state in current_states:
                candidates = generate_fn(state, kwargs.get('n_generate', 3))
                all_candidates.extend(candidates)
                step_generate_calls += 1

            generate_calls += step_generate_calls
            total_generated += len(all_candidates)
            
            if not all_candidates:
                break
            
            # Evaluate candidates
            values = evaluate_fn(all_candidates)
            evaluate_calls += 1
            total_evaluated += len(all_candidates)
            
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
                    'success': True,
                    'metrics': {
                        'total_generated': total_generated,
                        'total_evaluated': total_evaluated,
                        'generate_calls': generate_calls,
                        'evaluate_calls': evaluate_calls,
                    },
                }
            
            search_history.append({
                'step': step,
                'candidates': all_candidates,
                'values': values,
                'selected': selected_candidates,
                'generated_this_step': len(all_candidates),
                'evaluated_this_step': len(all_candidates),
                'generate_calls_this_step': step_generate_calls,
                'evaluate_calls_this_step': 1,
            })
            
            current_states = selected_candidates
        
        return {
            'final_states': current_states,
            'search_history': search_history,
            'strategy': 'BFS',
            'steps_taken': max_steps,
            'success': False,
            'metrics': {
                'total_generated': total_generated,
                'total_evaluated': total_evaluated,
                'generate_calls': generate_calls,
                'evaluate_calls': evaluate_calls,
            },
        }

