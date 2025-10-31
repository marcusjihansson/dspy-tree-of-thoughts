"""
A* Search strategy for Tree-of-Thought reasoning.
Uses heuristic function to guide optimal search.
"""

import heapq
from typing import List, Dict, Any, Callable, Optional
from .base import SearchStrategy


class AStarSearch(SearchStrategy):
    """A* Search - uses heuristic to guide search optimally."""
    
    def search(self, 
               initial_state: str,
               generate_fn: Callable[[str, int], List[str]],
               evaluate_fn: Callable[[List[str]], List[float]],
               is_goal_fn: Callable[[str], bool],
               max_steps: int,
               heuristic_fn: Optional[Callable[[str], float]] = None,
               **kwargs) -> Dict[str, Any]:
        
        # instrumentation
        total_generated = 0
        total_evaluated = 0
        generate_calls = 0
        evaluate_calls = 0

        # Wrap evaluate_fn for heuristic if needed so we count those calls
        def heuristic_eval(state: str) -> float:
            nonlocal total_evaluated, evaluate_calls
            vals = evaluate_fn([state])
            evaluate_calls += 1
            total_evaluated += 1
            return vals[0] if vals else 0.0

        if heuristic_fn is None:
            # Use evaluation function as heuristic (counted)
            heuristic_fn = lambda state: heuristic_eval(state) if state else 0.0
        
        # Priority queue: (f_score, g_score, state, path)
        open_set = [(0.0, 0.0, initial_state, [initial_state])]
        closed_set = set()
        search_history = []
        step = 0
        
        while open_set and step < max_steps:
            # Get node with lowest f_score
            f_score, g_score, current_state, path = heapq.heappop(open_set)
            
            if current_state in closed_set:
                continue
            
            closed_set.add(current_state)
            
            # Check if goal reached
            if is_goal_fn(current_state):
                return {
                    'final_states': [current_state],
                    'search_history': search_history,
                    'strategy': 'A*',
                    'steps_taken': step,
                    'success': True,
                    'best_path': path,
                    'metrics': {
                        'total_generated': total_generated,
                        'total_evaluated': total_evaluated,
                        'generate_calls': generate_calls,
                        'evaluate_calls': evaluate_calls,
                    },
                }
            
            # Generate successors
            candidates = generate_fn(current_state, kwargs.get('n_generate', 3))
            generate_calls += 1
            total_generated += len(candidates)
            if candidates:
                values = evaluate_fn(candidates)
                evaluate_calls += 1
                total_evaluated += len(candidates)
                
                for candidate, value in zip(candidates, values):
                    if candidate in closed_set:
                        continue
                    
                    # g_score: cost from start to current node
                    new_g_score = g_score + (1.0 - value)  # Lower evaluation = higher cost
                    
                    # h_score: heuristic estimate to goal
                    h_score = -heuristic_fn(candidate)  # Negative because we want max heap behavior
                    
                    # f_score: total estimated cost
                    new_f_score = new_g_score + h_score
                    
                    heapq.heappush(open_set, (new_f_score, new_g_score, candidate, path + [candidate]))
            
            search_history.append({
                'step': step,
                'current_state': current_state,
                'f_score': f_score,
                'g_score': g_score,
                'open_set_size': len(open_set),
                'closed_set_size': len(closed_set)
            })
            
            step += 1
        
        # Return best state found
        best_state = current_state if 'current_state' in locals() else initial_state
        
        return {
            'final_states': [best_state],
            'search_history': search_history,
            'strategy': 'A*',
            'steps_taken': step,
            'success': False,
            'metrics': {
                'total_generated': total_generated,
                'total_evaluated': total_evaluated,
                'generate_calls': generate_calls,
                'evaluate_calls': evaluate_calls,
            },
        }