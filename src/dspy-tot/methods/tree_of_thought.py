import itertools
import numpy as np
from typing import List, Dict, Any, Optional, Callable
import dspy
from .factory import create_search_strategy
from .base import text_completion_goal, crossword_goal, math_goal


class TreeOfThought:
    """DSPy implementation of Tree-of-Thought reasoning for text generation."""

    def __init__(self,
                 generate_module: dspy.Module,
                 evaluate_module: dspy.Module,
                 vote_module: Optional[dspy.Module] = None,
                 compare_module: Optional[dspy.Module] = None):
        """
        Initialize Tree-of-Thought with DSPy modules.

        Args:
            generate_module: Module for generating text (standard or CoT)
            evaluate_module: Module for evaluating text quality
            vote_module: Optional module for voting among candidates
            compare_module: Optional module for comparing passages
        """
        self.generate_module = generate_module
        self.evaluate_module = evaluate_module
        self.vote_module = vote_module
        self.compare_module = compare_module

    def get_value(self, passage: str, n_evaluate_sample: int = 3) -> float:
        """Evaluate a single passage and return its value score."""
        scores = []
        for _ in range(n_evaluate_sample):
            try:
                result = self.evaluate_module(passage=passage)
                # Extract score from result - assuming it's an integer 1-10
                score_str = str(result.score).strip()
                # Try to extract number from the response
                import re
                match = re.search(r'(\d+)', score_str)
                if match:
                    score = int(match.group(1))
                    if 1 <= score <= 10:
                        scores.append(score)
            except Exception as e:
                print(f"Evaluation error: {e}")
                continue

        if scores:
            return sum(scores) / len(scores)
        return 0.0

    def get_values(self, passages: List[str], n_evaluate_sample: int = 3) -> List[float]:
        """Evaluate multiple passages and return their value scores."""
        return [self.get_value(passage, n_evaluate_sample) for passage in passages]

    def get_votes(self, instruction: str, candidates: List[str], n_evaluate_sample: int = 3) -> List[int]:
        """Get votes for the best candidate among multiple options."""
        if not self.vote_module:
            raise ValueError("vote_module is required for voting evaluation method")

        vote_counts = [0] * len(candidates)
        for _ in range(n_evaluate_sample):
            try:
                result = self.vote_module(instruction=instruction, candidates=candidates)
                # Extract the best choice index
                choice_str = str(result.best_choice).strip()
                import re
                match = re.search(r'(\d+)', choice_str)
                if match:
                    choice_idx = int(match.group(1)) - 1  # Convert to 0-based indexing
                    if 0 <= choice_idx < len(candidates):
                        vote_counts[choice_idx] += 1
            except Exception as e:
                print(f"Voting error: {e}")
                continue

        return vote_counts

    def generate_samples(self, ending_sentences: List[str], current_passage: str = "",
                        n_generate_sample: int = 3, use_cot: bool = False) -> List[str]:
        """Generate multiple passage samples."""
        samples = []
        for _ in range(n_generate_sample):
            try:
                if use_cot:
                    # Use CoT generation
                    result = self.generate_module(ending_sentences=ending_sentences)
                    if hasattr(result, 'passage'):
                        samples.append(result.passage)
                    else:
                        samples.append(str(result))
                else:
                    # Use standard generation
                    result = self.generate_module(ending_sentences=ending_sentences)
                    samples.append(result.passage)
            except Exception as e:
                print(f"Generation error: {e}")
                continue

        return samples

    def solve(self,
              ending_sentences: List[str],
              steps: int = 2,
              method_generate: str = "sample",
              method_evaluate: str = "value",
              method_select: str = "greedy",
              n_generate_sample: int = 3,
              n_evaluate_sample: int = 3,
              n_select_sample: int = 2,
              use_cot: bool = False,
              verbose: bool = True) -> Dict[str, Any]:
        """
        Solve the text generation task using tree-of-thought reasoning.

        Args:
            ending_sentences: List of 4 sentences that must end each paragraph
            steps: Number of reasoning steps
            method_generate: "sample" for generating multiple candidates
            method_evaluate: "value" for scoring or "vote" for voting
            method_select: "greedy" for best candidates or "sample" for probabilistic selection
            n_generate_sample: Number of candidates to generate per step
            n_evaluate_sample: Number of evaluation samples per candidate
            n_select_sample: Number of candidates to select for next step
            use_cot: Whether to use chain-of-thought generation
            verbose: Whether to print progress

        Returns:
            Dictionary with final passages and step information
        """
        instruction = f"Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {' '.join(ending_sentences)}"

        ys = [""]  # current output candidates
        infos = []

        for step in range(steps):
            if verbose:
                print(f"\n=== Step {step + 1} ===")

            # generation
            if method_generate == "sample":
                new_ys = []
                for y in ys:
                    samples = self.generate_samples(
                        ending_sentences=ending_sentences,
                        current_passage=y,
                        n_generate_sample=n_generate_sample,
                        use_cot=use_cot
                    )
                    new_ys.extend(samples)
            else:
                raise ValueError(f"Unsupported generation method: {method_generate}")

            if not new_ys:
                if verbose:
                    print("No new candidates generated, keeping current ones")
                new_ys = ys

            ids = list(range(len(new_ys)))

            # evaluation
            if method_evaluate == "vote":
                values = self.get_votes(instruction, new_ys, n_evaluate_sample)
            elif method_evaluate == "value":
                values = self.get_values(new_ys, n_evaluate_sample)
            else:
                raise ValueError(f"Unsupported evaluation method: {method_evaluate}")

            # selection
            if method_select == "sample":
                if sum(values) > 0:
                    ps = np.array(values) / sum(values)
                    select_ids = np.random.choice(ids, size=min(n_select_sample, len(ids)), p=ps).tolist()
                else:
                    select_ids = ids[:n_select_sample]
            elif method_select == "greedy":
                select_ids = sorted(ids, key=lambda x: values[x], reverse=True)[:n_select_sample]
            else:
                raise ValueError(f"Unsupported selection method: {method_select}")

            select_new_ys = [new_ys[select_id] for select_id in select_ids]

            # log
            if verbose:
                print(f"Generated {len(new_ys)} candidates")
                print(f"Selected {len(select_new_ys)} best candidates")
                if len(select_new_ys) > 0:
                    print(f"Best candidate preview: {select_new_ys[0][:100]}...")

            infos.append({
                "step": step,
                "ys": ys,
                "new_ys": new_ys,
                "values": values,
                "select_new_ys": select_new_ys,
            })

            ys = select_new_ys

            # If we have no candidates left, break
            if not ys:
                break

        final_passages = ys if ys else [""]

        return {
            "passages": final_passages,
            "steps": infos,
            "instruction": instruction
        }

    def solve_with_search(self,
                         ending_sentences: List[str],
                         search_strategy: str = "bfs",
                         max_steps: int = 5,
                         n_generate_sample: int = 3,
                         n_evaluate_sample: int = 3,
                         use_cot: bool = False,
                         verbose: bool = True,
                         goal_check: Optional[str] = None,
                         **strategy_kwargs) -> Dict[str, Any]:
        """
        Solve using different search strategies.
        
        Args:
            ending_sentences: List of sentences that must end each paragraph
            search_strategy: Search algorithm - 'bfs', 'dfs', 'mcts', 'astar', 'beam', 'best_first'
            max_steps: Maximum search steps
            n_generate_sample: Number of candidates to generate per step
            n_evaluate_sample: Number of evaluation samples per candidate
            use_cot: Whether to use chain-of-thought generation
            verbose: Whether to print progress
            goal_check: Type of goal checking - 'text', 'crossword', 'math', or None
            **strategy_kwargs: Additional parameters for specific strategies
            
        Returns:
            Dictionary with search results
        """
        if verbose:
            print(f"\n=== Tree-of-Thought with {search_strategy.upper()} Search ===")
            print(f"Target endings: {ending_sentences}")
            print(f"Max steps: {max_steps}, Strategy: {search_strategy}")
        
        # Create search strategy
        strategy = create_search_strategy(search_strategy)
        
        # Define generation function
        def generate_fn(current_state: str, n_samples: int) -> List[str]:
            return self.generate_samples(
                ending_sentences=ending_sentences,
                current_passage=current_state,
                n_generate_sample=n_samples,
                use_cot=use_cot
            )
        
        # Define evaluation function
        def evaluate_fn(states: List[str]) -> List[float]:
            return self.get_values(states, n_evaluate_sample)
        
        # Define goal function
        def goal_fn(state: str) -> bool:
            if goal_check == 'text':
                return text_completion_goal(state, ending_sentences)
            elif goal_check == 'crossword':
                return crossword_goal(state, " ".join(ending_sentences))
            elif goal_check == 'math':
                return math_goal(state, " ".join(ending_sentences))
            else:
                # Default: check if we have a reasonable length passage
                return len(state.strip()) > 200 and any(sentence in state for sentence in ending_sentences)
        
        # Run search
        result = strategy.search(
            initial_state="",
            generate_fn=generate_fn,
            evaluate_fn=evaluate_fn,
            is_goal_fn=goal_fn,
            max_steps=max_steps,
            n_generate=n_generate_sample,
            **strategy_kwargs
        )
        
        if verbose:
            print(f"\nSearch completed:")
            print(f"Strategy: {result['strategy']}")
            print(f"Steps taken: {result['steps_taken']}")
            print(f"Success: {result['success']}")
            print(f"Final states: {len(result['final_states'])}")
            if result['final_states']:
                print(f"Best result preview: {result['final_states'][0][:100]}...")
        
        return result

    def naive_solve(self,
                   ending_sentences: List[str],
                   n_generate_sample: int = 5,
                   use_cot: bool = False,
                   verbose: bool = True) -> Dict[str, Any]:
        """Solve using naive generation without tree-of-thought."""
        if verbose:
            print("=== Naive Generation ===")

        samples = self.generate_samples(
            ending_sentences=ending_sentences,
            n_generate_sample=n_generate_sample,
            use_cot=use_cot
        )

        instruction = f"Write a coherent passage of 4 short paragraphs. The end sentence of each paragraph must be: {' '.join(ending_sentences)}"

        return {
            "passages": samples,
            "steps": [],
            "instruction": instruction
        } 
