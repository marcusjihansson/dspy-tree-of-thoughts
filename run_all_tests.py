#!/usr/bin/env python3
"""
Comprehensive test runner for all profiles and strategies.
Runs complete test matrix and generates comprehensive analysis.
"""

import subprocess
import sys
import time
from pathlib import Path


def run_command(cmd, description):
    """Run a command and return success status."""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {' '.join(cmd)}")
    print('='*60)
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, check=False)
        end_time = time.time()
        duration = end_time - start_time
        
        status = "✅ SUCCESS" if result.returncode == 0 else "❌ FAILED"
        print(f"\n{status} - {description} (took {duration:.1f}s)")
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ ERROR running {description}: {e}")
        return False


def main():
    """Run comprehensive test suite."""
    print("🚀 DSPy Tree-of-Thought Comprehensive Test Suite")
    print("=" * 60)
    
    # Test configurations
    profiles = ["easy", "smoke", "stress"]
    strategies = ["astar", "beam", "best_first", "bfs", "dfs", "mcts"]
    
    total_tests = 0
    passed_tests = 0
    
    # Summary of what will be tested
    print(f"\n📊 Test Matrix:")
    print(f"   Profiles: {len(profiles)} ({', '.join(profiles)})")
    print(f"   Strategies: {len(strategies)} ({', '.join(strategies)})")
    print(f"   Total combinations: {len(profiles) * len(strategies)}")
    
    # Option 1: Run all profiles (one command per profile)
    print(f"\n🎯 Option 1: Run by Profile (3 commands)")
    for profile in profiles:
        cmd = ["python", "run_tests.py", "--profile", profile, "--analysis"]
        success = run_command(cmd, f"All strategies with {profile} profile")
        total_tests += 1
        if success:
            passed_tests += 1
    
    print(f"\n" + "="*60)
    print(f"🎯 Option 2: Run by Strategy (6 commands)")
    
    # Option 2: Run all strategies (one command per strategy)
    for strategy in strategies:
        cmd = ["python", "run_tests.py", "--strategy", strategy]
        success = run_command(cmd, f"{strategy} strategy with all profiles")
        total_tests += 1
        if success:
            passed_tests += 1
    
    print(f"\n" + "="*60)
    print(f"🎯 Option 3: Individual Strategy-Profile Combinations")
    
    # Option 3: Run each combination individually (18 commands)
    combination_results = []
    for profile in profiles:
        for strategy in strategies:
            cmd = ["python", "run_tests.py", "--strategy", strategy, "--profile", profile]
            success = run_command(cmd, f"{strategy} strategy with {profile} profile")
            combination_results.append((strategy, profile, success))
            total_tests += 1
            if success:
                passed_tests += 1
    
    # Final comprehensive analysis
    print(f"\n" + "="*60)
    print("🔍 Running Final Comprehensive Analysis")
    print("="*60)
    
    analysis_cmd = ["python", "test/analysis/comparative_analysis.py"]
    run_command(analysis_cmd, "Comprehensive results analysis")
    
    # Summary report
    print(f"\n" + "🎉 COMPREHENSIVE TEST SUMMARY " + "="*30)
    print(f"Total test runs: {total_tests}")
    print(f"Successful runs: {passed_tests}")
    print(f"Failed runs: {total_tests - passed_tests}")
    print(f"Success rate: {(passed_tests/total_tests*100):.1f}%")
    
    # Detailed combination results
    print(f"\n📋 Individual Combination Results:")
    for strategy, profile, success in combination_results:
        status = "✅" if success else "❌"
        print(f"   {status} {strategy:12} + {profile:6}")
    
    print(f"\n🏆 All tests completed!")
    
    # Results summary
    results_cmd = ["python", "manage_results.py", "--summary"]
    run_command(results_cmd, "Results summary")


if __name__ == "__main__":
    main()