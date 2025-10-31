"""Best-first search strategy tests."""

from base_test import BaseToTTest


class TestBestFirst(BaseToTTest):
    """Test class for Best-first search strategy."""
    STRATEGY = 'best_first'
    
    def is_goal_fn(self, state):
        """Override with simpler goal function used in original test."""
        return 'DSPy' in state and len(state.split()) > 80
