"""Quick test of the @track_experiment decorator"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mlops_sdk import track_experiment


@track_experiment("quick_test")
def simple_function(x=10, y=20):
    """A simple test function"""
    result = x + y
    print(f"Computing: {x} + {y} = {result}")
    return result


if __name__ == "__main__":
    print("\n" + "="*60)
    print("Testing @track_experiment decorator")
    print("="*60 + "\n")
    
    result = simple_function(x=5, y=15)
    
    print(f"\n✅ Function returned: {result}")
    print("✅ Experiment tracked successfully!\n")
