#!/usr/bin/env python3
"""
Test DSPy Tree-of-Thought with different models via OpenRouter.

This script demonstrates the model-agnostic nature of the implementation
by allowing easy switching between different reasoning models.
"""

import os
import sys
from typing import List

# Add the current directory to Python path for imports
sys.path.insert(0, os.path.dirname(__file__))

import dspy
from modules import create_text_evaluator, create_text_generator
from tree_of_thought import TreeOfThought


def run_model_test(model_id: str, test_case: dict) -> dict:
    """Test a specific model with a given test case."""
    
    # Configure DSPy with the specified model
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("OPENROUTER_API_KEY environment variable is not set!")
    
    api_base = os.getenv("API_BASE", "https://openrouter.ai/api/v1")
    
    # Propagate API key for DSPy compatibility
    os.environ["OPENAI_API_KEY"] = api_key
    
    try:
        lm = dspy.LM(
            model_id,
            max_tokens=8000,
            temperature=0.7,
            api_base=api_base,
        )
        dspy.configure(lm=lm)
        print(f"✓ Configured model: {model_id}")
    except Exception as e:
        print(f"✗ Failed to configure model {model_id}: {e}")
        return {"model": model_id, "error": str(e)}
    
    # Create modules
    generator = create_text_generator(use_cot=True)
    evaluator = create_text_evaluator()
    
    # Create tree-of-thought solver
    tot = TreeOfThought(generate_module=generator, evaluate_module=evaluator)
    
    try:
        # Run a simplified test
        result = tot.solve(
            ending_sentences=test_case["ending_sentences"],
            steps=1,  # Just one step for testing
            n_generate_sample=2,
            n_evaluate_sample=1,
            verbose=False,
        )
        
        if result["passages"]:
            return {
                "model": model_id,
                "success": True,
                "passage_length": len(result["passages"][0]),
                "num_passages": len(result["passages"])
            }
        else:
            return {
                "model": model_id,
                "success": False,
                "error": "No passages generated"
            }
            
    except Exception as e:
        return {
            "model": model_id,
            "success": False,
            "error": str(e)
        }


def main():
    """Test multiple models to demonstrate model-agnostic implementation."""
    
    print("DSPy Tree-of-Thought Model-Agnostic Test")
    print("=" * 50)
    print()
    
    # Test case
    test_case = {
        "ending_sentences": [
            "The experiment had unexpected results.",
            "Sometimes the best discoveries happen by accident.",
            "Science is full of surprises."
        ]
    }
    
    # Models to test (uncomment the ones you want to test)
    models_to_test = [
        "anthropic/claude-3.5-sonnet",  # Default
        # "openai/gpt-4",                  # OpenAI GPT-4
        # "meta-llama/llama-3.1-8b-instruct",  # Open source
        # "google/gemini-pro-1.5",         # Google Gemini
        # "mistralai/mistral-large",       # Mistral
    ]
    
    # Get model from environment if specified
    env_model = os.getenv("MODEL_ID")
    if env_model and env_model not in models_to_test:
        models_to_test.insert(0, env_model)
    
    print(f"Testing {len(models_to_test)} model(s):")
    for model in models_to_test:
        print(f"  - {model}")
    print()
    
    results = []
    
    for model_id in models_to_test:
        print(f"Testing {model_id}...")
        result = run_model_test(model_id, test_case)
        results.append(result)
        
        if result.get("success"):
            print(f"  ✓ Success - Generated {result['num_passages']} passage(s)")
        else:
            print(f"  ✗ Failed - {result.get('error', 'Unknown error')}")
        print()
    
    # Summary
    print("Test Summary:")
    print("-" * 30)
    successful = [r for r in results if r.get("success")]
    failed = [r for r in results if not r.get("success")]
    
    print(f"Successful: {len(successful)}/{len(results)}")
    for result in successful:
        print(f"  ✓ {result['model']}")
    
    if failed:
        print(f"Failed: {len(failed)}/{len(results)}")
        for result in failed:
            print(f"  ✗ {result['model']}: {result.get('error', 'Unknown error')}")
    
    print()
    print("This demonstrates that DSPy Tree-of-Thought works with")
    print("multiple different models through OpenRouter!")


if __name__ == "__main__":
    main()