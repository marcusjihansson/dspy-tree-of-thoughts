import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

import dspy
from modules import create_text_evaluator, create_text_generator
from tree_of_thought import TreeOfThought
from dataset import text_dataset

# Configure DSPy with a non-OpenAI provider via OpenRouter
# Make sure OPENROUTER_API_KEY is set in your environment
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    print("ERROR: OPENROUTER_API_KEY environment variable is not set!")
    print("Please set your OpenRouter API key:")
    print("export OPENROUTER_API_KEY='your-openrouter-api-key-here'")
    sys.exit(1)

# Allow model and API base to be overridden via env vars, with sane defaults
# You can use any model available on OpenRouter - examples:
# - "openrouter/anthropic/claude-3.5-sonnet"
# - "openrouter/openai/gpt-4"
# - "openrouter/meta-llama/llama-3.1-8b-instruct"
# - "openrouter/google/gemini-pro-2.5"
# - "openrouter/mistralai/mistral-large"

model_id = os.getenv("MODEL_ID", "openrouter/meta-llama/llama-3.1-8b-instruct")
api_base = os.getenv("API_BASE", "https://openrouter.ai/api/v1")

# Some DSPy versions expect an OpenAI-compatible key env var. As a compatibility fallback,
# propagate OPENROUTER_API_KEY to OPENAI_API_KEY without importing the openai package.
os.environ.setdefault("OPENAI_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))

try:
    # Configure DSPy LM for OpenRouter without importing openai
    lm = dspy.LM(
        model_id,
        max_tokens=16000,
        temperature=1.0,
        api_base=api_base,
    )
    dspy.configure(lm=lm)
    print(f"Configured DSPy with LM: {model_id} via {api_base}")
except Exception as e:
    print(f"Failed to configure DSPy LM: {e}")
    print("Make sure you have the correct DSPy version and API key.")
    print(
        "You may need to adjust the LM configuration in main.py based on your DSPy version."
    )
    sys.exit(1)

# Create modules
generator = create_text_generator(use_cot=True)
evaluator = create_text_evaluator()

# Create tree-of-thought solver
tot = TreeOfThought(generate_module=generator, evaluate_module=evaluator)

# Load examples from dataset
examples = text_dataset.examples[:5]  # Use first 5 examples for demo

# Solve a text generation task using BFS (original approach) for each example
for i, example in enumerate(examples):
    ending_sentences = example.ending_sentences
    print(f"\n=== Example {i + 1} ===")
    print(f"Ending sentences: {ending_sentences}")

    print("\n--- Original BFS Approach ---")
    result = tot.solve(
        ending_sentences=ending_sentences,
        steps=2,
        n_generate_sample=3,
        n_evaluate_sample=2,
        verbose=True,
    )

    print("\nBFS Generated passages:")
    for j, passage in enumerate(result["passages"]):
        print(f"\nPassage {j + 1}:")
        print(passage)

    # Test different search strategies
    print("\n" + "-" * 40)
    print("TESTING DIFFERENT SEARCH STRATEGIES")
    print("-" * 40)

    search_strategies = [
        ("dfs", "Depth-First Search", {"max_depth": 4}),
        ("beam", "Beam Search", {"beam_width": 3}),
        ("mcts", "Monte Carlo Tree Search", {"simulations_per_step": 5}),
        ("best_first", "Best-First Search", {}),
    ]

    for strategy, name, kwargs in search_strategies:
        print(f"\n--- {name} ---")
        try:
            strategy_result = tot.solve_with_search(
                ending_sentences=ending_sentences,
                search_strategy=strategy,
                max_steps=2,
                n_generate_sample=2,
                n_evaluate_sample=1,
                verbose=True,
                goal_check="text",
                **kwargs,
            )

            print(f"\n{name} results:")
            for j, passage in enumerate(strategy_result["final_states"]):
                print(f"\nResult {j + 1}:")
                print(passage[:200] + "..." if len(passage) > 200 else passage)

        except Exception as e:
            print(f"❌ {name} failed: {e}")

print("\n" + "=" * 60)
print("All search strategies demonstrated on all examples!")
print("Each strategy explores the solution space differently:")
print("• BFS: Breadth-first, explores all options at each level")
print("• DFS: Depth-first, explores deeply before backtracking")
print("• Beam: Keeps top-k candidates, balances quality and diversity")
print("• MCTS: Balances exploration/exploitation with simulations")
print("• Best-First: Greedy selection based on heuristic values")

# Compare outputs across examples
print("\n" + "=" * 60)
print("OUTPUT COMPARISON ACROSS EXAMPLES")
print("=" * 60)

comparison_data = []
for i, example in enumerate(examples):
    ending_sentences = example.ending_sentences
    # Get the BFS result for this example (assuming it's stored or regenerate)
    # For simplicity, we'll regenerate a quick BFS result
    bfs_result = tot.solve(
        ending_sentences=ending_sentences,
        steps=1,  # Quick for comparison
        n_generate_sample=2,
        n_evaluate_sample=1,
        verbose=False,
    )
    passage = bfs_result["passages"][0] if bfs_result["passages"] else ""
    word_count = len(passage.split()) if passage else 0
    char_count = len(passage) if passage else 0
    unique_words = len(set(passage.lower().split())) if passage else 0

    comparison_data.append(
        {
            "example": i + 1,
            "ending_sentences": len(ending_sentences),
            "passage_length_chars": char_count,
            "passage_length_words": word_count,
            "unique_words": unique_words,
            "avg_word_length": char_count / word_count if word_count > 0 else 0,
        }
    )

print(
    f"{'Example':<8} {'End Sentences':<12} {'Chars':<6} {'Words':<6} {'Unique Words':<12} {'Avg Word Len':<12}"
)
print("-" * 70)
for data in comparison_data:
    print(
        f"{data['example']:<8} {data['ending_sentences']:<12} {data['passage_length_chars']:<6} {data['passage_length_words']:<6} {data['unique_words']:<12} {data['avg_word_length']:<12.2f}"
    )

# Show diversity
total_passages = len(comparison_data)
avg_length = sum(d["passage_length_words"] for d in comparison_data) / total_passages
unique_lengths = len(set(d["passage_length_words"] for d in comparison_data))
print(f"\nDiversity metrics:")
print(f"- Average passage length: {avg_length:.1f} words")
print(f"- Unique passage lengths: {unique_lengths}/{total_passages}")
print(
    f"- Length variation: {'High' if unique_lengths > total_passages * 0.5 else 'Low'}"
)
