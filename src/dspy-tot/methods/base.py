"""
Base classes and utilities for Tree-of-Thought search strategies.
"""

import random
import math
import heapq
from typing import List, Dict, Any, Optional, Tuple, Callable
from abc import ABC, abstractmethod
from dataclasses import dataclass
import numpy as np


@dataclass
class SearchNode:
    """Represents a node in the search tree."""
    state: str  # Current passage/solution state
    path: List[str]  # Path to reach this state
    depth: int  # Depth in the tree
    value: float  # Evaluation score
    visits: int = 0  # For MCTS
    total_reward: float = 0.0  # For MCTS
    parent: Optional['SearchNode'] = None
    children: List['SearchNode'] = None
    
    def __post_init__(self):
        if self.children is None:
            self.children = []
    
    @property
    def ucb_value(self) -> float:
        """Upper Confidence Bound value for MCTS."""
        if self.visits == 0:
            return float('inf')
        
        exploration_param = 1.414  # sqrt(2)
        if self.parent and self.parent.visits > 0:
            exploration = exploration_param * math.sqrt(math.log(self.parent.visits) / self.visits)
        else:
            exploration = 0
        
        exploitation = self.total_reward / self.visits
        return exploitation + exploration


class SearchStrategy(ABC):
    """Abstract base class for search strategies."""
    
    @abstractmethod
    def search(self, 
               initial_state: str,
               generate_fn: Callable[[str, int], List[str]],
               evaluate_fn: Callable[[List[str]], List[float]],
               is_goal_fn: Callable[[str], bool],
               max_steps: int,
               **kwargs) -> Dict[str, Any]:
        """
        Perform search using the strategy.
        
        Args:
            initial_state: Starting state (empty string for text generation)
            generate_fn: Function to generate candidate states
            evaluate_fn: Function to evaluate states
            is_goal_fn: Function to check if goal is reached
            max_steps: Maximum search steps
            **kwargs: Strategy-specific parameters
            
        Returns:
            Dictionary with search results
        """
        pass


# Utility functions for common goal checks
def text_completion_goal(state: str, target_sentences: List[str]) -> bool:
    """Check if text completion task is done (has all target sentences)."""
    return all(sentence.strip() in state for sentence in target_sentences)


def crossword_goal(state: str, target_pattern: str) -> bool:
    """Check if crossword task matches target pattern."""
    # Simple pattern matching - could be more sophisticated
    return len(state.strip()) >= len(target_pattern.strip())


def math_goal(state: str, target_answer: str) -> bool:
    """Check if math problem has correct answer."""
    return target_answer.strip() in state.strip()