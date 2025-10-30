# DSPy Tree-of-Thought - Model Agnostic Implementation

This directory contains a model-agnostic implementation of Tree-of-Thought reasoning using DSPy and OpenRouter. Unlike the original implementation that was tied to specific model APIs, this version can work with any model available through OpenRouter.

## Key Features

- **Model Agnostic**: Works with any model supported by OpenRouter (OpenAI, Anthropic, Meta, Google, Mistral, etc.)
- **DSPy Framework**: Built on DSPy for better modularity and composability
- **OpenRouter Integration**: Single API for accessing multiple model providers
- **Easy Model Switching**: Change models via environment variables
- **Consistent Interface**: Same code works across different model architectures

## Files

- `main.py` - Main demo script showing tree-of-thought reasoning
- `tree_of_thought.py` - Core tree-of-thought algorithm adapted for DSPy
- `modules.py` - DSPy modules for generation, evaluation, voting, comparison
- `signatures.py` - DSPy signatures defining input/output interfaces
- `evaluation.py` - Evaluation system using DSPy LM calls
- `dataset.py` - DSPy-compatible dataset for text generation tasks
- `test_models.py` - Script to test multiple models
- `test_tot.py` - Structural overview and proof of concept

## Setup

1. **Install dependencies**:
   ```bash
   pip install dspy-ai numpy
   ```

2. **Get OpenRouter API key**:
   - Sign up at [OpenRouter](https://openrouter.ai)
   - Get your API key from the dashboard

3. **Configure environment**:
   ```bash
   export OPENROUTER_API_KEY="your-openrouter-api-key-here"
   export MODEL_ID="anthropic/claude-3.5-sonnet"  # Optional: choose your model
   ```

## Usage

### Basic Usage

```bash
# From the project root
python run_demo.py

# Or directly
cd src/dspy-tot
python main.py
```

### Testing Multiple Models

```bash
cd src/dspy-tot
python test_models.py
```

### Available Models

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
export MODEL_ID="mistralai/mistral-small"
```

## Architecture

### Tree-of-Thought Algorithm

The implementation maintains the core tree-of-thought algorithm structure:

1. **Generation**: Create multiple candidate solutions
2. **Evaluation**: Score each candidate for quality
3. **Selection**: Choose the best candidates to continue
4. **Iteration**: Repeat for multiple steps

### DSPy Integration

The implementation uses DSPy's module system:

- **Signatures**: Define the interface between modules
- **Modules**: Encapsulate specific reasoning capabilities
- **LM Abstraction**: Model-agnostic language model interface

### Model Independence

Key aspects that make this model-agnostic:

- Uses DSPy's `LM` class for unified model access
- OpenRouter provides a single API for multiple providers
- No direct API calls to specific model providers
- Consistent prompt formatting across models

## Performance Notes

Different models may perform differently on tree-of-thought tasks:

- **Large models** (Claude 3.5 Sonnet, GPT-4) typically perform better on complex reasoning
- **Smaller models** (Llama 3.1 8B) may be faster but less capable
- **Specialized models** might excel at specific types of reasoning

The framework allows you to easily test and compare different models for your specific use case.

## Customization

### Adding New Evaluation Methods

Create new DSPy signatures and modules in `modules.py`:

```python
class CustomEvaluation(dspy.Signature):
    """Your custom evaluation criteria."""
    passage = dspy.InputField(desc="Text to evaluate")
    custom_score = dspy.OutputField(desc="Your custom scoring")

class CustomEvaluator(dspy.Module):
    def __init__(self):
        super().__init__()
        self.evaluate = dspy.Predict(CustomEvaluation)
```

### Different Task Types

The framework can be extended for different reasoning tasks by:

1. Creating new signatures for your task
2. Implementing task-specific modules
3. Adapting the tree-of-thought algorithm in `tree_of_thought.py`

## Benefits over Original Implementation

1. **No Vendor Lock-in**: Not tied to any specific model API
2. **Easy Model Switching**: Change models without code changes
3. **Better Abstractions**: DSPy provides cleaner interfaces
4. **Composable**: Easy to combine with other DSPy modules
5. **Future-Proof**: Works with new models as they become available

## Limitations

- Requires OpenRouter API key (but gives access to many models)
- Some models may not support all features equally
- Performance varies significantly between models
- May need prompt tuning for specific models

## Contributing

This implementation demonstrates how to make tree-of-thought reasoning model-agnostic. Contributions for:

- Additional evaluation methods
- New task types
- Performance optimizations
- Model-specific prompt optimizations

are welcome!