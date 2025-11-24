#!/usr/bin/env python3
"""
Demo script showcasing different search strategies for Tree-of-Thought reasoning.

This script demonstrates how different search algorithms can be used with the same
Tree-of-Thought framework to solve reasoning tasks in different ways.
"""

import os
import sys
import time

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

import dspy
from modules import create_text_evaluator, create_text_generator
from tree_of_thought import TreeOfThought
from dataset import text_dataset


def setup_dspy():
    """Setup DSPy with OpenRouter configuration."""
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("ERROR: OPENROUTER_API_KEY environment variable is not set!")
        print("Please set your OpenRouter API key:")
        print("export OPENROUTER_API_KEY='your-openrouter-api-key-here'")
        sys.exit(1)

    model_id = os.getenv("MODEL_ID", "anthropic/claude-3.5-sonnet")
    api_base = os.getenv("API_BASE", "https://openrouter.ai/api/v1")

    os.environ.setdefault("OPENAI_API_KEY", api_key)

    try:
        lm = dspy.LM(
            model_id,
            max_tokens=8000,
            temperature=0.7,
            api_base=api_base,
        )
        dspy.configure(lm=lm)
        print(f"✓ Configured DSPy with model: {model_id}")
        return True
    except Exception as e:
        print(f"✗ Failed to configure DSPy: {e}")
        return False


def compare_search_strategies():
    """Compare different search strategies on the same task."""

    print("🔍 Tree-of-Thought Search Strategy Comparison")
    print("=" * 60)

    # Load examples from dataset
    examples = text_dataset.examples[:3]  # Use first 3 examples for demo

    # Create modules
    generator = create_text_generator(use_cot=True)
    evaluator = create_text_evaluator()
    tot = TreeOfThought(generate_module=generator, evaluate_module=evaluator)

    # Search strategies to test
    strategies = [
        {
            "name": "Breadth-First Search (BFS)",
            "strategy": "bfs",
            "description": "Explores all nodes at current depth before going deeper",
            "kwargs": {"n_select": 2},
        },
        {
            "name": "Depth-First Search (DFS)",
            "strategy": "dfs",
            "description": "Explores as far as possible before backtracking",
            "kwargs": {"max_depth": 4},
        },
        {
            "name": "Beam Search",
            "strategy": "beam",
            "description": "Keeps top-k candidates at each step",
            "kwargs": {"beam_width": 3},
        },
        {
            "name": "Best-First Search",
            "strategy": "best_first",
            "description": "Always picks best heuristic value",
            "kwargs": {},
        },
        {
            "name": "Monte Carlo Tree Search (MCTS)",
            "strategy": "mcts",
            "description": "Balances exploration and exploitation",
            "kwargs": {"simulations_per_step": 5},
        },
        {
            "name": "A* Search",
            "strategy": "astar",
            "description": "Uses heuristic to guide optimal search",
            "kwargs": {},
        },
    ]

    results = []  # Initialize outside loop

    for example_idx, example in enumerate(examples):
        ending_sentences = example.ending_sentences
        print(f"\n📝 Example {example_idx + 1}")
        print(f"Ending sentences: {ending_sentences}")
        print("=" * 60)

        results = []  # Reset for each example

        for strategy_config in strategies:
            print(f"\n🔍 Testing {strategy_config['name']}")
            print(f"   {strategy_config['description']}")
            print("-" * 50)

            start_time = time.time()

            try:
                result = tot.solve_with_search(
                    ending_sentences=ending_sentences,
                    search_strategy=strategy_config["strategy"],
                    max_steps=3,  # Shorter for demo
                    n_generate_sample=2,
                    n_evaluate_sample=1,
                    verbose=True,
                    goal_check="text",
                    **strategy_config["kwargs"],
                )

                end_time = time.time()
                duration = end_time - start_time

                # Analyze results
                success = result.get("success", False)
                steps_taken = result.get("steps_taken", 0)
                final_states = result.get("final_states", [])

                strategy_result = {
                    "strategy": strategy_config["name"],
                    "success": success,
                    "steps": steps_taken,
                    "duration": duration,
                    "final_count": len(final_states),
                    "quality": len(final_states[0]) if final_states else 0,
                }

                results.append(strategy_result)

                print(f"   ✓ Completed in {duration:.2f}s")
                print(f"   Steps: {steps_taken}, Success: {success}")

                if final_states:
                    preview = (
                        final_states[0][:100] + "..."
                        if len(final_states[0]) > 100
                        else final_states[0]
                    )
                    print(f"   Preview: {preview}")

            except Exception as e:
                print(f"   ✗ Failed: {e}")
                results.append(
                    {
                        "strategy": strategy_config["name"],
                        "success": False,
                        "error": str(e),
                    }
                )

        # Summary comparison per example
        print("Strategy Comparison Summary for this example:")
        print("-" * 50)
        print(
            f"{'Strategy':<25} {'Success':<8} {'Steps':<6} {'Time':<8} {'Quality':<8}"
        )
        print("-" * 70)

        successful_results = [
            r for r in results if "error" not in r and r.get("success")
        ]
        if successful_results:
            # Show quality differences
            qualities = [r["quality"] for r in successful_results]
            max_quality = max(qualities)
            min_quality = min(qualities)
            quality_range = max_quality - min_quality
            print(
                f"Quality range: {quality_range} (min: {min_quality}, max: {max_quality})"
            )

            # Show time differences
            times = [r["duration"] for r in successful_results]
            fastest = min(times)
            slowest = max(times)
            time_range = slowest - fastest
            print(
                f"Time range: {time_range:.2f}s (fastest: {fastest:.2f}s, slowest: {slowest:.2f}s)"
            )

        for result in results:
            if "error" not in result:
                success_mark = "✓" if result["success"] else "✗"
                print(
                    f"{result['strategy']:<25} {success_mark:<8} {result['steps']:<6} "
                    f"{result['duration']:.2f}s{'':<3} {result['quality']:<8}"
                )
            else:
                print(
                    f"{result['strategy']:<25} {'ERROR':<8} {'-':<6} {'-':<8} {'-':<8}"
                )

    return results  # Return results from last example


def demonstrate_task_specific_strategies():
    """Show how different strategies work better for different task types."""

    print("\n🎯 Task-Specific Strategy Recommendations")
    print("=" * 50)

    tasks = [
        {
            "name": "Text Generation",
            "description": "Creating coherent passages",
            "recommended": ["bfs", "beam"],
            "reason": "Need to explore multiple coherent paths",
        },
        {
            "name": "Crossword Solving",
            "description": "Filling word puzzles with constraints",
            "recommended": ["dfs", "astar"],
            "reason": "Constraint satisfaction benefits from depth exploration",
        },
        {
            "name": "Math Problem Solving",
            "description": "Multi-step mathematical reasoning",
            "recommended": ["mcts", "astar"],
            "reason": "Need to balance exploration with heuristic guidance",
        },
        {
            "name": "Creative Writing",
            "description": "Generating diverse, creative content",
            "recommended": ["mcts", "beam"],
            "reason": "Benefits from exploration of diverse possibilities",
        },
        {
            "name": "Logical Reasoning",
            "description": "Step-by-step logical deduction",
            "recommended": ["dfs", "best_first"],
            "reason": "Sequential reasoning benefits from depth-first approach",
        },
    ]

    for task in tasks:
        print(f"\n📋 {task['name']}")
        print(f"   Description: {task['description']}")
        print(f"   Recommended: {', '.join(task['recommended']).upper()}")
        print(f"   Reason: {task['reason']}")


def demonstrate_strategy_parameters():
    """Show how strategy parameters affect performance."""

    print("\n⚙️  Strategy Parameter Effects")
    print("=" * 40)

    parameters = [
        {
            "strategy": "Beam Search",
            "parameter": "beam_width",
            "effect": "Wider beam = more diverse exploration but slower",
            "values": [2, 3, 5, 10],
        },
        {
            "strategy": "MCTS",
            "parameter": "simulations_per_step",
            "effect": "More simulations = better estimates but slower",
            "values": [5, 10, 20, 50],
        },
        {
            "strategy": "DFS",
            "parameter": "max_depth",
            "effect": "Deeper search = more thorough but may get stuck",
            "values": [3, 5, 8, 12],
        },
    ]

    for param in parameters:
        print(f"\n🔧 {param['strategy']}")
        print(f"   Parameter: {param['parameter']}")
        print(f"   Effect: {param['effect']}")
        print(f"   Typical values: {param['values']}")


def main():
    """Main demonstration function."""

    print("🌳 Tree-of-Thought Search Strategies Demo")
    print("=" * 60)
    print("This demo showcases different search algorithms for ToT reasoning:")
    print("• BFS - Breadth-first exploration")
    print("• DFS - Depth-first exploration")
    print("• MCTS - Monte Carlo tree search")
    print("• A* - Heuristic-guided optimal search")
    print("• Beam - Top-k candidate selection")
    print("• Best-First - Greedy heuristic search")
    print()

    # Setup
    if not setup_dspy():
        return

    try:
        # Main comparison
        results = compare_search_strategies()

        # Additional demonstrations
        demonstrate_task_specific_strategies()
        demonstrate_strategy_parameters()

        print("\n🎉 Demo completed! Key takeaways:")
        print("• Different search strategies have different strengths")
        print("• Task type should inform strategy choice")
        print("• Parameters can be tuned for specific needs")
        print("• The same ToT framework works with all strategies")

    except KeyboardInterrupt:
        print("\n\n⚠️  Demo interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Demo failed: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
