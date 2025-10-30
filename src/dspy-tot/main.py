import os
import sys

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

import dspy
from modules import create_text_evaluator, create_text_generator
from tree_of_thought import TreeOfThought

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

# Solve a text generation task using BFS (original approach)
ending_sentences = [
    "It caught him off guard that space smelled of seared steak.",
    "People keep telling me orange but I still prefer pink.",
    "Each person who knows you has a different perception of who you are.",
]

print("\n=== Original BFS Approach ===")
result = tot.solve(
    ending_sentences=ending_sentences,
    steps=2,
    n_generate_sample=3,
    n_evaluate_sample=2,
    verbose=True,
)

print("\nBFS Generated passages:")
for i, passage in enumerate(result["passages"]):
    print(f"\nPassage {i + 1}:")
    print(passage)

# Test different search strategies
print("\n" + "=" * 60)
print("TESTING DIFFERENT SEARCH STRATEGIES")
print("=" * 60)

search_strategies = [
    ("dfs", "Depth-First Search", {"max_depth": 4}),
    ("beam", "Beam Search", {"beam_width": 3}),
    ("mcts", "Monte Carlo Tree Search", {"simulations_per_step": 5}),
    ("best_first", "Best-First Search", {}),
]

for strategy, name, kwargs in search_strategies:
    print(f"\n=== {name} ===")
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
        for i, passage in enumerate(strategy_result["final_states"]):
            print(f"\nResult {i + 1}:")
            print(passage[:200] + "..." if len(passage) > 200 else passage)

    except Exception as e:
        print(f"❌ {name} failed: {e}")

print("\n" + "=" * 60)
print("All search strategies demonstrated!")
print("Each strategy explores the solution space differently:")
print("• BFS: Breadth-first, explores all options at each level")
print("• DFS: Depth-first, explores deeply before backtracking")
print("• Beam: Keeps top-k candidates, balances quality and diversity")
print("• MCTS: Balances exploration/exploitation with simulations")
print("• Best-First: Greedy selection based on heuristic values")
