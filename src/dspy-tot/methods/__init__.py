"""
Search strategy factory and imports for Tree-of-Thought methods.
"""

from .base import SearchStrategy, SearchNode, text_completion_goal, crossword_goal, math_goal
from .bfs import BreadthFirstSearch
from .dfs import DepthFirstSearch  
from .mct import MonteCarloTreeSearch
from .astar import AStarSearch
from .beam_search import BeamSearch
from .best_first import BestFirstSearch
from .factory import create_search_strategy
from .tree_of_thought import TreeOfThought


# Export all classes and functions
__all__ = [
    'SearchStrategy',
    'SearchNode', 
    'BreadthFirstSearch',
    'DepthFirstSearch',
    'MonteCarloTreeSearch', 
    'AStarSearch',
    'BeamSearch',
    'BestFirstSearch',
    'TreeOfThought',
    'create_search_strategy',
    'text_completion_goal',
    'crossword_goal', 
    'math_goal'
]