# Tree-of-Thought Search Strategies

This document explains the different search algorithms implemented for Tree-of-Thought reasoning and when to use each one.

## Overview

Tree-of-Thought (ToT) reasoning involves searching through a space of possible solution paths. Different search strategies explore this space in different ways, each with their own strengths and trade-offs.

## Implemented Search Strategies

### 1. Breadth-First Search (BFS) 
**Type**: Uninformed Search  
**Original ToT Approach**: ✅ This is the original method from the paper

**How it works:**
- Explores all nodes at the current depth before moving to the next level
- Generates candidates from all current states simultaneously
- Selects top-k candidates based on evaluation scores
- Guarantees finding the shortest path to a solution

**Best for:**
- Text generation tasks where you want diverse exploration
- When solution quality at each step is important
- Problems where optimal solutions tend to be found quickly

**Parameters:**
- `n_select`: Number of candidates to keep at each step (default: 2)

**Pros:**
- Systematic exploration
- Good for finding high-quality solutions quickly
- Well-tested in original ToT paper

**Cons:**
- Can be memory intensive with many candidates
- May not explore deeply enough for complex problems

### 2. Depth-First Search (DFS)
**Type**: Uninformed Search  
**Mentioned in Paper**: ✅ Specifically recommended for crossword tasks

**How it works:**
- Explores as far as possible along each branch before backtracking
- Recursively expands the most promising candidate at each step
- Backtracks when no more expansion is possible
- Memory efficient as it only stores the current path

**Best for:**
- Crossword puzzles and constraint satisfaction problems
- Sequential reasoning tasks
- When solutions tend to be deep rather than wide

**Parameters:**
- `max_depth`: Maximum depth to explore (default: 10)

**Pros:**
- Memory efficient
- Good for problems with deep solution spaces
- Can find solutions quickly if they exist deep in the tree

**Cons:**
- May get stuck in suboptimal paths
- No guarantee of finding optimal solutions
- Can take long time if solution is in a different branch

### 3. Monte Carlo Tree Search (MCTS)
**Type**: Informed Search / Reinforcement Learning  
**Importance**: 🌟 Highly Significant - Cornerstone of modern AI planning

**How it works:**
- Balances exploration (trying new paths) and exploitation (following promising paths)
- Uses four phases: Selection, Expansion, Simulation, Backpropagation
- Employs Upper Confidence Bound (UCB) to select nodes
- Runs multiple simulations to estimate value of each path

**Best for:**
- Complex reasoning tasks requiring exploration/exploitation balance
- Creative writing where diverse solutions are valuable
- Problems where simulation can provide good estimates

**Parameters:**
- `simulations_per_step`: Number of simulations per search step (default: 10)

**Pros:**
- Excellent exploration/exploitation balance
- Proven successful in games (AlphaGo, AlphaZero)
- Handles uncertainty well
- Anytime algorithm (can stop and return best found)

**Cons:**
- More complex to implement and tune
- Requires more computational resources
- Performance depends on quality of simulation

### 4. A* Search
**Type**: Informed Search  
**Importance**: 📚 Academically Relevant - Classical algorithm with LLM applications

**How it works:**
- Uses heuristic function to estimate cost to goal
- Maintains open set prioritized by f(n) = g(n) + h(n)
- g(n) = cost from start, h(n) = heuristic estimate to goal
- Guarantees optimal solution if heuristic is admissible

**Best for:**
- Math problem solving where steps have clear costs
- Logical reasoning with well-defined goal states
- When you have good heuristic estimates

**Parameters:**
- `heuristic_fn`: Custom heuristic function (optional, uses evaluation by default)

**Pros:**
- Optimal solutions (with admissible heuristic)
- Efficient with good heuristics
- Well-studied algorithm

**Cons:**
- Requires good heuristic function
- Can be memory intensive
- May not be suitable for all LLM reasoning tasks

### 5. Beam Search
**Type**: Heuristic Search  
**Importance**: 🔧 Core Technique - Essential for efficient ToT

**How it works:**
- Keeps top-k candidates at each step (the "beam")
- Generates candidates from all beam states
- Selects best candidates to form new beam
- Essentially ToT + BFS with limited beam width

**Best for:**
- Balancing quality and efficiency
- Text generation with quality constraints
- When you want controlled exploration

**Parameters:**
- `beam_width`: Number of candidates to keep (default: 3)

**Pros:**
- Good balance of exploration and efficiency
- Memory usage controlled by beam width
- Fast convergence to good solutions

**Cons:**
- May miss optimal solutions outside beam
- Performance sensitive to beam width
- Can converge prematurely

### 6. Best-First Search (Greedy)
**Type**: Informed Search  
**Importance**: 🚀 Common in Agents - Quick heuristic-guided decisions

**How it works:**
- Always selects node with best heuristic value
- Uses priority queue to maintain candidates
- Expands most promising node first
- Greedy approach focused on immediate best options

**Best for:**
- Quick decision making
- When heuristic is very reliable
- Real-time applications requiring fast responses

**Parameters:**
- None (uses evaluation function as heuristic)

**Pros:**
- Very fast
- Simple to implement
- Good when heuristic is reliable

**Cons:**
- Can get stuck in local optima
- No optimality guarantees
- Heavily dependent on heuristic quality

## Strategy Selection Guide

### By Task Type

| Task Type | Recommended Strategies | Reason |
|-----------|----------------------|---------|
| **Text Generation** | BFS, Beam | Need diverse, coherent exploration |
| **Crossword Solving** | DFS, A* | Constraint satisfaction benefits from depth |
| **Math Problems** | MCTS, A* | Balance exploration with heuristic guidance |
| **Creative Writing** | MCTS, Beam | Benefits from diverse exploration |
| **Logical Reasoning** | DFS, Best-First | Sequential reasoning, reliable heuristics |
| **Real-time Applications** | Best-First, Beam | Speed is critical |

### By Problem Characteristics

| Characteristic | Best Strategy | Why |
|----------------|---------------|-----|
| **Deep solution space** | DFS, MCTS | Explore deeply before backtracking |
| **Wide solution space** | BFS, Beam | Systematic breadth exploration |
| **Good heuristics available** | A*, Best-First | Leverage domain knowledge |
| **Uncertain environment** | MCTS | Handles uncertainty well |
| **Limited computation** | Best-First, Beam | Fast convergence |
| **Need optimal solution** | A*, BFS | Optimality guarantees |

## Parameter Tuning Guidelines

### Beam Search
- **Small beam (2-3)**: Fast, focused search
- **Medium beam (5-8)**: Good balance
- **Large beam (10+)**: More exploration, slower

### MCTS
- **Few simulations (5-10)**: Fast decisions
- **Medium simulations (20-50)**: Good estimates
- **Many simulations (100+)**: High quality, slow

### DFS
- **Shallow depth (3-5)**: Quick exploration
- **Medium depth (8-12)**: Balanced search
- **Deep search (15+)**: Thorough but slow

## Implementation Examples

### Basic Usage
```python
from tree_of_thought import TreeOfThought
from modules import create_text_generator, create_text_evaluator

# Setup
generator = create_text_generator(use_cot=True)
evaluator = create_text_evaluator()
tot = TreeOfThought(generate_module=generator, evaluate_module=evaluator)

# Use different strategies
result_bfs = tot.solve_with_search(
    ending_sentences=sentences,
    search_strategy="bfs",
    max_steps=5
)

result_mcts = tot.solve_with_search(
    ending_sentences=sentences, 
    search_strategy="mcts",
    simulations_per_step=20
)

result_beam = tot.solve_with_search(
    ending_sentences=sentences,
    search_strategy="beam", 
    beam_width=5
)
```

### Custom Goals
```python
# Text completion goal
result = tot.solve_with_search(
    ending_sentences=sentences,
    search_strategy="bfs",
    goal_check="text"  # Check if all ending sentences present
)

# Custom goal function
def custom_goal(state):
    return len(state.split()) > 100 and "conclusion" in state.lower()

# Would need to modify search strategies to accept custom goal functions
```

## Performance Characteristics

| Strategy | Speed | Memory | Optimality | Exploration |
|----------|--------|---------|------------|-------------|
| BFS | Medium | High | Good | Systematic |
| DFS | Fast | Low | Poor | Deep |
| MCTS | Slow | Medium | Good | Balanced |
| A* | Medium | High | Best* | Guided |
| Beam | Fast | Low | Good | Controlled |
| Best-First | Fastest | Low | Poor | Greedy |

*A* optimality requires admissible heuristic

## Advanced Topics

### Hybrid Strategies
You could combine strategies, for example:
- Start with Best-First for quick initial solutions
- Switch to MCTS for refinement
- Use DFS for final deep exploration

### Dynamic Strategy Selection
Adapt strategy based on:
- Problem complexity discovered during search
- Available computation time
- Quality of intermediate results

### Custom Heuristics
Implement domain-specific heuristics for A* and Best-First:
```python
def math_heuristic(state):
    # Estimate how close to solution based on mathematical progress
    return calculate_progress_score(state)

def text_heuristic(state):
    # Estimate coherency and completeness
    return coherency_score(state) + completeness_score(state)
```

## Conclusion

Different search strategies offer different trade-offs between speed, quality, and exploration. The choice depends on:

1. **Task characteristics** (deep vs wide, sequential vs parallel)
2. **Quality requirements** (optimal vs good enough)
3. **Computational constraints** (time and memory limits)
4. **Uncertainty** (how reliable are evaluations?)

The flexible architecture allows easy experimentation to find the best strategy for your specific use case.