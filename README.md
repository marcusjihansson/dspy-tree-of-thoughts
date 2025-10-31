# DSPy Tree-of-Thought - Model Agnostic Implementation

A comprehensive, model-agnostic implementation of tree-of-thought reasoning using DSPy and OpenRouter, adapted from the original [tree-of-thought-llm](https://github.com/princeton-nlp/tree-of-thought-llm) repository.

## 🌟 Key Features

- **🔄 Model Agnostic**: Works with 100+ models via OpenRouter (OpenAI, Anthropic, Meta, Google, Mistral, etc.)
- **🧩 6 Search Strategies**: BFS, DFS, MCTS, A*, Beam, Best-First - most comprehensive ToT implementation
- **🌐 DSPy Framework**: Built on proven DSPy for better modularity and composability  
- **⚡ Easy Model Switching**: Change models via environment variables without code changes
- **🔧 Consistent Interface**: Same code works across different model architectures
- **📊 Comprehensive Testing**: Full test suite with analysis tools

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install dspy-ai numpy
```

### 2. Configure Environment
```bash
export OPENROUTER_API_KEY="your-openrouter-api-key-here"
export MODEL_ID="anthropic/claude-3.5-sonnet"  # Optional
```

### 3. Run Demo
```bash
python run_demo.py
```

## 📚 Documentation

- **[📖 Full Documentation](docs/)** - Comprehensive guides and API reference
- **[👤 User Guide](docs/user/)** - Setup, usage, and testing
- **[👨‍💻 Developer Docs](docs/dev/)** - Implementation details and extension

## 🎯 Available Search Strategies

| Strategy | Type | Best For |
|----------|------|----------|
| **BFS** | Breadth-First | Text generation, systematic exploration |
| **DFS** | Depth-First | Crosswords, constraint problems |
| **MCTS** | Monte Carlo | Complex reasoning, creative tasks |
| **A*** | Heuristic-guided | Math problems, optimal solutions |
| **Beam** | Top-K selection | Efficient quality balance |
| **Best-First** | Greedy heuristic | Real-time applications |

## 🌐 Model Support

Works with any model on OpenRouter:
- **Anthropic**: Claude 3.5 Sonnet, Claude 3 Haiku
- **OpenAI**: GPT-4, GPT-4 Turbo, GPT-3.5 Turbo
- **Meta**: Llama 3.1 (8B, 70B), Llama 2
- **Google**: Gemini Pro 1.5, Gemini Flash
- **Mistral**: Mistral Large, Mistral Small
- **And many more...**

## 📁 Project Structure

```
dspy-tot/
├── src/dspy-tot/              # Core implementation
│   ├── methods/               # Search strategies (BFS, DFS, MCTS, etc.)
│   ├── modules.py            # DSPy modules (generator, evaluator, etc.)
│   ├── evaluation.py         # Evaluation system
│   └── data/                # Dataset files
├── test/                    # Comprehensive test suite
├── docs/                    # 📚 Full documentation
└── run_demo.py              # Quick demo runner
```

## 🎯 Basic Usage

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
result = tot.solve_with_search(sentences, search_strategy="mcts")
```

## 🔧 Advanced Usage

- **[📖 Full Documentation](docs/)** - Comprehensive guides and API reference
- **[👤 User Guide](docs/user/)** - Setup, usage, and testing
- **[👨‍💻 Developer Docs](docs/dev/)** - Implementation details and extension

## 📊 Key Features

### Tree-of-Thought Algorithm
- **Generation**: Creates multiple passage candidates per step
- **Evaluation**: Scores candidates using coherency metrics
- **Selection**: Chooses best candidates for next iteration
- **Iteration**: Refines solutions over multiple steps

### DSPy Integration
- **Signatures**: Structured I/O for different reasoning tasks
- **Modules**: Reusable components with learnable parameters
- **LM Abstraction**: Works with any DSPy-supported language model
- **Optimization**: Can be optimized using DSPy's teleprompters

## 🏆 Comparison with Original

| Aspect | Original Implementation | This Implementation |
|--------|------------------------|-------------------|
| **Model Support** | OpenAI only | 100+ models via OpenRouter |
| **Search Strategies** | BFS only | 6 algorithms |
| **Switching Cost** | Code changes | Environment variable |
| **Extensibility** | Limited | High (DSPy modules) |
| **Documentation** | Basic | Comprehensive |

## 📜 License

This implementation is based on the tree-of-thought-llm repository. Please refer to the original repository for licensing information.