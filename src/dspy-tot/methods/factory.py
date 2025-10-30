"""
Factory for creating search strategies.
"""

from .base import SearchStrategy
from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch  
from .mct import MonteCarloTreeSearch
from .astar import AStarSearch
from .beam_search import BeamSearch
from .best_first import BestFirstSearch


def create_search_strategy(strategy_name: str) -> SearchStrategy:
    """Create a search strategy by name."""
    strategies = {
        'bfs': BreadthFirstSearch,
        'dfs': DepthFirstSearch, 
        'mcts': MonteCarloTreeSearch,
        'astar': AStarSearch,
        'beam': BeamSearch,
        'best_first': BestFirstSearch
    }
    
    strategy_class = strategies.get(strategy_name.lower())
    if strategy_class is None:
        raise ValueError(f"Unknown strategy: {strategy_name}. Available: {list(strategies.keys())}")
    
    return strategy_class()