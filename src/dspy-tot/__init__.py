"""
DSPy Tree-of-Thought Implementation

A proof-of-concept implementation of tree-of-thought reasoning in DSPy
for text generation tasks.
"""

__version__ = "0.1.0"

# Support both package and direct module imports (pytest collection safety)
try:
    from .dataset import TextGenerationDataset, text_dataset
    from .evaluation import TextEvaluatorDSPy, create_text_evaluator
    from .modules import TextComparator, TextEvaluator, TextGenerator, TextVoter
    from .modules import create_text_evaluator as _create_text_evaluator
    from .modules import create_text_generator, create_text_voter
    from .tree_of_thought import TreeOfThought
except ImportError:  # Fallback when not imported as a package
    from dataset import TextGenerationDataset, text_dataset
    from evaluation import TextEvaluatorDSPy, create_text_evaluator
    from modules import TextComparator, TextEvaluator, TextGenerator, TextVoter
    from modules import create_text_evaluator as _create_text_evaluator
    from modules import create_text_generator, create_text_voter
    from tree_of_thought import TreeOfThought

__all__ = [
    "TextGenerationDataset",
    "text_dataset",
    "TextGenerator",
    "TextEvaluator",
    "TextVoter",
    "TextComparator",
    "create_text_generator",
    "create_text_evaluator",
    "create_text_voter",
    "TreeOfThought",
    "TextEvaluatorDSPy",
    "create_text_evaluator",
]
