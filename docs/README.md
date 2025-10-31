# DSPy Tree-of-Thought Documentation

This directory contains comprehensive documentation for the DSPy Tree-of-Thought implementation.

## 📚 Documentation Structure

### 👤 User Documentation
For users who want to use the Tree-of-Thought framework:

- **[Overview](user/overview.md)** - High-level features and benefits
- **[Getting Started](user/getting-started.md)** - Quick setup and basic usage
- **[Test Running Guide](user/test-running-guide.md)** - How to run tests and analyze results

### 👨‍💻 Developer Documentation  
For developers who want to understand or extend the implementation:

- **[Summary](dev/summary.md)** - Implementation summary and achievements
- **[Implementation Details](dev/implementation/)** - Core implementation documentation
  - **[Source README](dev/implementation/src-readme.md)** - Implementation overview
  - **[Search Strategies](dev/implementation/search-strategies.md)** - Detailed algorithm comparison
  - **[Reorganization](dev/implementation/reorganization.md)** - Code organization details
- **[Testing](dev/testing/)** - Test infrastructure and development
  - **[Test README](dev/testing/test-readme.md)** - Test directory structure and usage
- **[Cleanup Complete](dev/cleanup-complete.md)** - Code reorganization summary

## 🚀 Quick Start

1. **Install**: `pip install dspy-ai numpy`
2. **Configure**: Set `OPENROUTER_API_KEY` environment variable
3. **Run**: `python run_demo.py`

For detailed setup instructions, see [Getting Started](user/getting-started.md).

## 🌟 Key Features

- **Model Agnostic**: Works with 100+ models via OpenRouter
- **6 Search Strategies**: BFS, DFS, MCTS, A*, Beam, Best-First
- **DSPy Integration**: Built on proven DSPy framework
- **Easy Model Switching**: Change models via environment variables
- **Comprehensive Testing**: Full test suite with analysis tools

## 📖 Navigation

- **New Users**: Start with [Getting Started](user/getting-started.md)
- **Researchers**: See [Search Strategies](dev/implementation/search-strategies.md) for algorithm details
- **Developers**: Check [Implementation Details](dev/implementation/) for code structure
- **Testing**: Follow [Test Running Guide](user/test-running-guide.md) for running tests