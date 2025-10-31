# Complete Test Running Guide

## ✅ Yes, you can run `run_tests.py` for all 3 profiles and all 6 strategies!

Here are all the ways you can run comprehensive tests:

## 🚀 Quick Start Options

### **Basic Test Runner**
```bash
# Run all tests (all profiles, all strategies)
python run_tests.py

# Run specific profile (24 tests for easy, 12 for smoke/stress)
python run_tests.py --profile easy
python run_tests.py --profile smoke  
python run_tests.py --profile stress

# Run specific strategy (8 tests across all query types)
python run_tests.py --strategy astar
python run_tests.py --strategy beam
python run_tests.py --strategy best_first
python run_tests.py --strategy bfs
python run_tests.py --strategy dfs
python run_tests.py --strategy mcts

# Run specific combination
python run_tests.py --strategy astar --profile easy

# See what would run without executing
python run_tests.py --dry-run
python run_tests.py --strategy beam --profile smoke --dry-run
```

### **Quick Test Runner** (Simplified Interface)
```bash
# Show available options
python quick_tests.py

# Run all 3 profiles (easy, smoke, stress)
python quick_tests.py all-profiles

# Run all 6 strategies (astar, beam, best_first, bfs, dfs, mcts)
python quick_tests.py all-strategies

# Run everything (comprehensive matrix)
python quick_tests.py everything

# Dry run of all combinations
python quick_tests.py dry-run

# Run specific profile or strategy
python quick_tests.py easy
python quick_tests.py astar
```

### **Comprehensive Test Suite** (Full Matrix)
```bash
# Run complete test matrix with detailed reporting
python run_all_tests.py
```

## 📊 Test Matrix Overview

| Profile | Queries | Max Steps | Description |
|---------|---------|-----------|-------------|
| **easy** | 4 queries | 3 steps | Quick validation tests |
| **smoke** | 2 queries | 4 steps | Medium complexity tests |
| **stress** | 2 queries | 6 steps | Complex, thorough tests |

| Strategy | Description |
|----------|-------------|
| **astar** | A* search with heuristic guidance |
| **beam** | Beam search with top-k selection |
| **best_first** | Greedy best-first search |
| **bfs** | Breadth-first search (systematic) |
| **dfs** | Depth-first search (deep exploration) |
| **mcts** | Monte Carlo Tree Search |

## 🎯 Common Scenarios

### **Development Testing**
```bash
# Quick validation during development
python run_tests.py --profile easy --dry-run

# Test specific changes
python run_tests.py --strategy astar --profile easy
```

### **CI/CD Integration** 
```bash
# Fast CI tests
python run_tests.py --profile easy --clean-results

# Comprehensive CI tests
python quick_tests.py all-profiles
```

### **Performance Analysis**
```bash
# Run with analysis
python run_tests.py --profile smoke --analysis

# Full analysis with all combinations
python run_all_tests.py
```

### **Research/Benchmarking**
```bash
# Complete test matrix
python quick_tests.py everything

# Individual strategy comparison
python run_tests.py --strategy astar --analysis
python run_tests.py --strategy beam --analysis
```

## 🔧 Additional Options

### **With Coverage**
```bash
python run_tests.py --coverage --profile easy
 unordered list```

### **Clean Results First**
```bash
python run_tests.py --clean-results --profile smoke
```

### **Results Management**
```bash
# See current results
python manage_results.py --summary

# Archive results before new run
python manage_results.py --archive
python run_tests.py --profile stress

# Clean results
python manage_results.py --clean
```

### **Analysis Only**
```bash
# Run analysis on existing results
python test/analysis/comparative_analysis.py
```

## 🌟 Pro Tips

1. **Start with dry-run** to see what tests will run:
   ```bash
   python quick_tests.py dry-run
   ```

2. **Use profiles for different needs**:
   - `easy` for quick validation (24 tests)
   - `smoke` for moderate testing (12 tests)  
   - `stress` for thorough testing (12 tests)

3. **Set API key for actual execution**:
   ```bash
   export OPENROUTER_API_KEY="your_key_here"
   python run_tests.py --profile easy
   ```

4. **Combine with analysis** for insights:
   ```bash
   python run_tests.py --profile smoke --analysis
   ```

## 📈 Expected Test Counts

- **All profiles**: 48 total tests (24 easy + 12 smoke + 12 stress)
- **All strategies**: 48 total tests (8 per strategy × 6 strategies)
- **Complete matrix**: 48 unique tests covering all combinations

The test infrastructure is fully ready and you can run any combination of profiles and strategies efficiently!
