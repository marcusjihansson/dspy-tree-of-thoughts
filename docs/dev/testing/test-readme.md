# Test Directory Structure and Usage

This directory contains comprehensive tests for the DSPy Tree-of-Thought implementation.

## Directory Structure

```
test/
├── base_test.py           # Base test class with common functionality
├── test_astar.py         # A* search strategy tests
├── test_beam.py          # Beam search strategy tests  
├── test_best_first.py    # Best-first search strategy tests
├── test_bfs.py           # Breadth-first search strategy tests
├── test_dfs.py           # Depth-first search strategy tests
├── test_mcts.py          # Monte Carlo Tree Search strategy tests
├── common.py             # Shared utilities and configuration
├── queries.json          # Test queries organized by difficulty tier
├── results/              # Test execution results (JSON files)
└── analysis/             # Analysis scripts and tools
    └── comparative_analysis.py
```

## Running Tests

### Quick Start

```bash
# Dry run to see available tests
python run_tests.py --dry-run

# Run easy tests only (fast)
python run_tests.py --profile easy

# Run specific strategy
python run_tests.py --strategy astar --profile easy

# Run with analysis
python run_tests.py --profile smoke --analysis
```

### Test Profiles

- **easy**: Quick tests with simple queries (4 queries, max_steps=3)
- **smoke**: Medium tests including moderate complexity (6 queries, max_steps=4) 
- **stress**: Full test suite with complex queries (8 queries, max_steps=6)

### Environment Variables

- `OPENROUTER_API_KEY`: Required for running actual tests
- `MODEL_ID`: Model to use (default: "openrouter/meta-llama/llama-3.1-8b-instruct")
- `API_BASE`: API base URL (default: "https://openrouter.ai/api/v1")
- `PROFILE`: Test profile (easy/smoke/stress)

### Example Usage

```bash
# Set up environment
export OPENROUTER_API_KEY="your_key_here"
export PROFILE="easy"

# Run tests
python run_tests.py --profile easy --clean-results

# Run with coverage
python run_tests.py --profile smoke --coverage

# Analyze results
python test/analysis/comparative_analysis.py
```

## Test Implementation

All test classes inherit from `BaseToTTest` which provides:

- Common DSPy configuration
- Shared generate/evaluate/goal functions
- Consistent result formatting and storage
- Parameterized test execution across query tiers

Each strategy test file only needs to specify the `STRATEGY` class attribute.

## Results

Test results are stored as JSON files in `test/results/` with the format:
`{strategy}_{query_id}.json`

The comparative analysis script aggregates and analyzes these results across:
- Strategy performance comparison
- Tier-based analysis  
- Query-specific insights
- Success rates and efficiency metrics

## Customization

To add new search strategies:

1. Create `test_newstrategy.py` inheriting from `BaseToTTest`
2. Set `STRATEGY = 'newstrategy'`
3. Override any methods if needed (e.g., custom goal functions)
4. Ensure the strategy is registered in `methods/__init__.py`