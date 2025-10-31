# Getting Started with DSPy Tree-of-Thought

## Quick Setup

### 1. Install Dependencies
```bash
pip install dspy-ai numpy
```

### 2. Get OpenRouter API Key
- Sign up at [OpenRouter](https://openrouter.ai)
- Get your API key from the dashboard

### 3. Configure Environment
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key-here"
export MODEL_ID="anthropic/claude-3.5-sonnet"  # Optional: choose your model
```

### 4. Run the Demo
```bash
# From the project root
python run_demo.py
```

## Available Models

You can use any model available on OpenRouter by setting the `MODEL_ID` environment variable:

```bash
# Anthropic models
export MODEL_ID="anthropic/claude-3.5-sonnet"
export MODEL_ID="anthropic/claude-3-haiku"

# OpenAI models  
export MODEL_ID="openai/gpt-4"
export MODEL_ID="openai/gpt-4-turbo"

# Open source models
export MODEL_ID="meta-llama/llama-3.1-8b-instruct"
export MODEL_ID="meta-llama/llama-3.1-70b-instruct"

# Google models
export MODEL_ID="google/gemini-pro-1.5"

# Mistral models
export MODEL_ID="mistralai/mistral-large"
```

## Basic Usage

```python
import dspy
from dspy_tot import TreeOfThought, create_text_generator, create_text_evaluator

# Setup (works with any model)
lm = dspy.LM("anthropic/claude-3.5-sonnet", api_base="https://openrouter.ai/api/v1")
dspy.configure(lm=lm)

# Create ToT solver
generator = create_text_generator(use_cot=True)
evaluator = create_text_evaluator()
tot = TreeOfThought(generator, evaluator)

# Use different search strategies
result_bfs = tot.solve_with_search(sentences, search_strategy="bfs")
result_mcts = tot.solve_with_search(sentences, search_strategy="mcts")
result_beam = tot.solve_with_search(sentences, search_strategy="beam")
```

## Running Tests

See [Test Running Guide](test-running-guide.md) for comprehensive testing instructions.

## Next Steps

- Read the [Overview](overview.md) for detailed features
- Check [Developer Documentation](../dev/) for implementation details
- Explore [Search Strategies](../dev/implementation/search-strategies.md) for algorithm details