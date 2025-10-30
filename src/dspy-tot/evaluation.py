import re
from typing import List, Dict, Any, Optional
import dspy


class TextEvaluator(dspy.Module):
    """Module for evaluating text passage coherency."""

    def __init__(self):
        super().__init__()
        self.evaluate = dspy.Predict(TextEvaluation)

    def forward(self, passage):
        result = self.evaluate(passage=passage)
        return result


class TextComparison(dspy.Signature):
    """Compare the coherency of two text passages."""

    passage1 = dspy.InputField(desc="First passage to compare")
    passage2 = dspy.InputField(desc="Second passage to compare")
    comparison = dspy.OutputField(desc="Analysis of which passage is more coherent: '1' if passage1 is better, '2' if passage2 is better, or 'equal' if they are similarly coherent")


class TextEvaluation(dspy.Signature):
    """Evaluate the coherency of a text passage."""

    passage = dspy.InputField(desc="The text passage to evaluate")
    score = dspy.OutputField(desc="Coherency score from 1 to 10 (integer)")


class TextComparator(dspy.Module):
    """Module for comparing coherency of two passages."""

    def __init__(self):
        super().__init__()
        self.compare = dspy.Predict(TextComparison)

    def forward(self, passage1, passage2):
        result = self.compare(passage1=passage1, passage2=passage2)
        return result


class TextEvaluatorDSPy:
    """DSPy-based text evaluation system for coherency scoring."""

    def __init__(self):
        self.evaluator = TextEvaluator()
        self.comparator = TextComparator()

    def evaluate_passage(self, passage: str, n_samples: int = 5) -> Dict[str, Any]:
        """
        Evaluate a single passage for coherency.

        Args:
            passage: The text passage to evaluate
            n_samples: Number of evaluation samples to average

        Returns:
            Dictionary with scores and metadata
        """
        scores = []

        for _ in range(n_samples):
            try:
                result = self.evaluator(passage=passage)
                score = self._extract_score(result.score)
                if score is not None:
                    scores.append(score)
            except Exception as e:
                print(f"Evaluation error: {e}")
                continue

        avg_score = sum(scores) / len(scores) if scores else 0.0

        return {
            'score': avg_score,
            'individual_scores': scores,
            'n_evaluations': len(scores),
            'passage_length': len(passage.split())
        }

    def compare_passages(self, passage1: str, passage2: str, n_samples: int = 3) -> Dict[str, Any]:
        """
        Compare two passages for coherency.

        Args:
            passage1: First passage
            passage2: Second passage
            n_samples: Number of comparison samples

        Returns:
            Dictionary with comparison results
        """
        comparisons = []

        for _ in range(n_samples):
            try:
                result = self.comparator(passage1=passage1, passage2=passage2)
                comparison = self._extract_comparison(result.comparison)
                if comparison is not None:
                    comparisons.append(comparison)
            except Exception as e:
                print(f"Comparison error: {e}")
                continue

        # Count preferences
        p1_wins = sum(1 for c in comparisons if c == 1)
        p2_wins = sum(1 for c in comparisons if c == 2)
        ties = sum(1 for c in comparisons if c == 0)

        # Determine winner
        if p1_wins > p2_wins:
            winner = 1
        elif p2_wins > p1_wins:
            winner = 2
        else:
            winner = 0  # tie

        return {
            'winner': winner,
            'p1_wins': p1_wins,
            'p2_wins': p2_wins,
            'ties': ties,
            'total_comparisons': len(comparisons),
            'confidence': max(p1_wins, p2_wins, ties) / len(comparisons) if comparisons else 0
        }

    def evaluate_multiple_passages(self, passages: List[str], n_samples: int = 3) -> List[Dict[str, Any]]:
        """
        Evaluate multiple passages.

        Args:
            passages: List of passages to evaluate
            n_samples: Number of evaluation samples per passage

        Returns:
            List of evaluation results
        """
        return [self.evaluate_passage(passage, n_samples) for passage in passages]

    def rank_passages(self, passages: List[str], n_eval_samples: int = 3) -> List[Dict[str, Any]]:
        """
        Rank passages by coherency score.

        Args:
            passages: List of passages to rank
            n_eval_samples: Number of evaluation samples per passage

        Returns:
            Ranked list with scores and rankings
        """
        evaluations = self.evaluate_multiple_passages(passages, n_eval_samples)

        # Add ranking information
        ranked_results = []
        for i, eval_result in enumerate(evaluations):
            eval_result['original_index'] = i
            eval_result['passage'] = passages[i]
            ranked_results.append(eval_result)

        # Sort by score (descending)
        ranked_results.sort(key=lambda x: x['score'], reverse=True)

        # Add rank
        for rank, result in enumerate(ranked_results, 1):
            result['rank'] = rank

        return ranked_results

    def _extract_score(self, score_output: str) -> Optional[int]:
        """
        Extract numerical score from evaluator output.

        Args:
            score_output: Raw output from evaluator

        Returns:
            Integer score 1-10, or None if extraction fails
        """
        if isinstance(score_output, int):
            return score_output
        if isinstance(score_output, str):
            # Try to find a number in the string
            match = re.search(r'(\d+)', score_output.strip())
            if match:
                score = int(match.group(1))
                if 1 <= score <= 10:
                    return score
        return None

    def _extract_comparison(self, comparison_output: str) -> Optional[int]:
        """
        Extract comparison result from comparator output.

        Args:
            comparison_output: Raw output from comparator

        Returns:
            1 if passage1 is better, 2 if passage2 is better, 0 if tie, None if extraction fails
        """
        output = str(comparison_output).strip().lower()

        if '1' in output or 'first' in output or 'passage 1' in output:
            return 1
        elif '2' in output or 'second' in output or 'passage 2' in output:
            return 2
        elif 'equal' in output or 'similar' in output or 'tie' in output:
            return 0

        return None


# Convenience function
def create_text_evaluator():
    """Create a text evaluator instance."""
    return TextEvaluatorDSPy()