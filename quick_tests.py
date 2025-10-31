#!/usr/bin/env python3
"""
Quick test runner for common scenarios.
Provides simple commands for running all profiles and strategies.
"""

import subprocess
import sys
import os


def main():
    if len(sys.argv) < 2:
        print("Quick Test Runner for DSPy Tree-of-Thought")
        print("=" * 50)
        print("Usage:")
        print("  python quick_tests.py all-profiles      # Run all 3 profiles")
        print("  python quick_tests.py all-strategies    # Run all 6 strategies") 
        print("  python quick_tests.py everything        # Run complete matrix")
        print("  python quick_tests.py dry-run          # Dry run of everything")
        print("  python quick_tests.py easy             # Just easy profile")
        print("  python quick_tests.py astar            # Just astar strategy")
        return
    
    command = sys.argv[1].lower()
    
    if command == "all-profiles":
        # Run each profile with all strategies
        profiles = ["easy", "smoke", "stress"]
        for profile in profiles:
            print(f"\n🎯 Running {profile} profile...")
            subprocess.run(["python", "run_tests.py", "--profile", profile])
        print("\n🔍 Running analysis...")
        subprocess.run(["python", "test/analysis/comparative_analysis.py"])
        
    elif command == "all-strategies":
        # Run each strategy with all profiles
        strategies = ["astar", "beam", "best_first", "bfs", "dfs", "mcts"]
        for strategy in strategies:
            print(f"\n🎯 Running {strategy} strategy...")
            subprocess.run(["python", "run_tests.py", "--strategy", strategy])
        print("\n🔍 Running analysis...")
        subprocess.run(["python", "test/analysis/comparative_analysis.py"])
        
    elif command == "everything":
        # Run comprehensive test suite
        subprocess.run(["python", "run_all_tests.py"])
        
    elif command == "dry-run":
        # Dry run of everything
        profiles = ["easy", "smoke", "stress"]
        strategies = ["astar", "beam", "best_first", "bfs", "dfs", "mcts"]
        
        print("🔍 Dry run - All Profiles:")
        for profile in profiles:
            subprocess.run(["python", "run_tests.py", "--profile", profile, "--dry-run"])
            
        print("\n🔍 Dry run - All Strategies:")
        for strategy in strategies:
            subprocess.run(["python", "run_tests.py", "--strategy", strategy, "--dry-run"])
            
    elif command in ["easy", "smoke", "stress"]:
        # Run specific profile
        print(f"🎯 Running {command} profile...")
        subprocess.run(["python", "run_tests.py", "--profile", command, "--analysis"])
        
    elif command in ["astar", "beam", "best_first", "bfs", "dfs", "mcts"]:
        # Run specific strategy
        print(f"🎯 Running {command} strategy...")
        subprocess.run(["python", "run_tests.py", "--strategy", command, "--analysis"])
        
    else:
        print(f"❌ Unknown command: {command}")
        print("Use 'python quick_tests.py' to see available options")


if __name__ == "__main__":
    main()