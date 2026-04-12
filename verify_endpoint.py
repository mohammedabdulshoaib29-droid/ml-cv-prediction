#!/usr/bin/env python3
"""Verify that the ML pipeline endpoints work correctly."""

import sys
import pandas as pd
from backend.models.comparison import run_all_models

def main():
    try:
        print("[ENDPOINT] Testing ML pipeline...")
        
        # Load sample data
        train = pd.read_excel('backend/datasets/60MV_CV (1) (3).xlsx')
        test = pd.read_excel('backend/datasets/60MV_CV (1) (4).xlsx')
        
        # Run all models
        results = run_all_models(train, test)
        
        # Show key results
        print("\n=== FINAL RESULTS ===")
        print("Best Model: {}".format(results['best_model']))
        print("Best R²: {:.4f}".format(results['best_r2']))
        print("Best Capacitance: {:.2f} F/g".format(results['capacitance']))
        print("Energy Density: {:.2f} Wh/kg".format(results['energy']))
        print("Power Density: {:.2f} W/kg".format(results['power']))
        
        print("\n✅ Endpoint test PASSED!")
        return True
        
    except Exception as e:
        print("\n❌ Endpoint test FAILED!")
        print("Error: {}".format(str(e)))
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
