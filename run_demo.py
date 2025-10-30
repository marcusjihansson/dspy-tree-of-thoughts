#!/usr/bin/env python3
"""
Run the DSPy Tree-of-Thought demo from the project root.

Usage: 
  python run_demo.py              # Run main demo
  python run_demo.py search       # Run search strategies demo  
  python run_demo.py models       # Run model comparison demo
"""

import os
import sys
import subprocess

def main():
    """Run the appropriate demo based on command line arguments."""
    demo_dir = os.path.join(os.path.dirname(__file__), 'src', 'dspy-tot')

    if not os.path.exists(demo_dir):
        print(f"Error: Demo directory not found: {demo_dir}")
        return 1

    # Determine which demo to run
    demo_type = sys.argv[1] if len(sys.argv) > 1 else "main"
    
    if demo_type == "search":
        script = "demo_search_strategies.py"
        print("Running DSPy Tree-of-Thought Search Strategies Demo...")
    elif demo_type == "models":
        script = "test_models.py" 
        print("Running DSPy Tree-of-Thought Model Comparison Demo...")
    else:
        script = "main.py"
        print("Running DSPy Tree-of-Thought Main Demo...")
    
    print(f"Demo directory: {demo_dir}")
    print(f"Script: {script}")
    print()

    # Change to the demo directory and run the appropriate script
    result = subprocess.run([sys.executable, script], cwd=demo_dir)

    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help']:
        print(__doc__)
        sys.exit(0)
    
    sys.exit(main())