#!/usr/bin/env python3
"""
Results management utilities for organizing test results.
"""

import json
import shutil
from collections import defaultdict
from pathlib import Path
from datetime import datetime


def archive_results():
    """Archive current results with timestamp."""
    results_dir = Path("test/results")
    if not results_dir.exists():
        print("No results directory found")
        return
    
    # Create archive directory
    archive_dir = Path("test/results_archive")
    archive_dir.mkdir(exist_ok=True)
    
    # Create timestamped archive
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_path = archive_dir / f"results_{timestamp}"
    
    shutil.copytree(results_dir, archive_path)
    print(f"Results archived to: {archive_path}")


def clean_results():
    """Clean the results directory."""
    results_dir = Path("test/results")
    if results_dir.exists():
        shutil.rmtree(results_dir)
        print("Results directory cleaned")
    else:
        print("No results directory found")


def summarize_results():
    """Print a summary of current results."""
    results_dir = Path("test/results")
    if not results_dir.exists():
        print("No results directory found")
        return
    
    # Count files by strategy
    strategy_counts = defaultdict(int)
    total_files = 0
    
    for file_path in results_dir.glob("*.json"):
        if "_" in file_path.stem:
            strategy = file_path.stem.split("_")[0]
            strategy_counts[strategy] += 1
            total_files += 1
    
    print(f"Results Summary ({total_files} total files):")
    print("-" * 40)
    for strategy, count in sorted(strategy_counts.items()):
        print(f"{strategy:15}: {count:3} files")
    
    # Check for summary files
    summary_files = list(results_dir.glob("*_results.json"))
    if summary_files:
        print(f"\nSummary files: {len(summary_files)}")
        for f in summary_files:
            print(f"  - {f.name}")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Manage test results")
    parser.add_argument("--archive", action="store_true", help="Archive current results")
    parser.add_argument("--clean", action="store_true", help="Clean results directory")
    parser.add_argument("--summary", action="store_true", help="Show results summary")
    
    args = parser.parse_args()
    
    if args.archive:
        archive_results()
    elif args.clean:
        clean_results()
    elif args.summary:
        summarize_results()
    else:
        summarize_results()  # default action


if __name__ == "__main__":
    main()