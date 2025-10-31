#!/usr/bin/env python3
"""
Test runner script for DSPy Tree-of-Thought implementation.

This script provides different test profiles:
- easy: Run only easy-tier queries (fast)
- smoke: Run easy + smoke-tier queries (medium)
- stress: Run all queries including stress-tier (slow)
- dry-run: Collect tests without running them
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Run DSPy ToT tests")
    parser.add_argument(
        "--profile", 
        choices=["easy", "smoke", "stress"], 
        help="Test profile to run (easy/smoke/stress)"
    )
    parser.add_argument(
        "--strategy", 
        choices=["astar", "beam", "best_first", "bfs", "dfs", "mcts"],
        help="Run tests for specific strategy only"
    )
    parser.add_argument(
        "--dry-run", 
        action="store_true",
        help="Collect tests without running them"
    )
    parser.add_argument(
        "--coverage", 
        action="store_true",
        help="Run with coverage reporting"
    )
    parser.add_argument(
        "--analysis", 
        action="store_true",
        help="Run comparative analysis after tests"
    )
    parser.add_argument(
        "--clean-results", 
        action="store_true",
        help="Clean results directory before running tests"
    )
    
    args = parser.parse_args()
    
    # Set environment variables
    if args.profile:
        os.environ["PROFILE"] = args.profile
        print(f"Running tests with profile: {args.profile}")
    
    # Clean results if requested
    if args.clean_results:
        results_dir = Path("test/results")
        if results_dir.exists():
            import shutil
            shutil.rmtree(results_dir)
            print("Cleaned results directory")
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    if args.dry_run:
        cmd.extend(["--collect-only", "-q"])
    
    if args.coverage:
        cmd.extend(["--cov=src", "--cov-report=html", "--cov-report=term-missing"])
    
    # Add test path filter
    if args.strategy:
        cmd.append(f"test/test_{args.strategy}.py")
        print(f"Running tests for strategy: {args.strategy}")
    else:
        cmd.append("test/")
    
    # Add standard options
    cmd.extend(["-v", "--tb=short"])
    
    # Check for API key if not dry run
    if not args.dry_run and not os.getenv("OPENROUTER_API_KEY"):
        print("Warning: OPENROUTER_API_KEY not set. Tests will be skipped.")
        print("Set OPENROUTER_API_KEY environment variable to run actual tests.")
    
    print(f"Running command: {' '.join(cmd)}")
    
    # Run pytest
    try:
        result = subprocess.run(cmd, check=False)
        
        # Run analysis if requested and tests completed
        if args.analysis and not args.dry_run and result.returncode == 0:
            print("\nRunning comparative analysis...")
            analysis_cmd = ["python", "test/analysis/comparative_analysis.py"]
            subprocess.run(analysis_cmd, check=False)
        
        return result.returncode
        
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())