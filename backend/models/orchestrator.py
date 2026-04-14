"""
Model Orchestrator - Coordinates training of all models
"""

import pandas as pd
import numpy as np
from models.ann import run_ann
from models.rf import run_rf
from models.xgb import run_xgb
import traceback


def train_all_models(train_df, test_df, predictors=None, target=None, model_type='all'):
    """
    Train models - can be all or specific ones
    
    Args:
        train_df: Training dataframe
        test_df: Testing dataframe
        predictors: List of feature columns
        target: Target column name
        model_type: Which models to train: 'all', 'ann', 'rf', 'xgb'
    
    Returns:
        Dictionary with results from trained models
    """
    
    results = {
        'success': True,
        'models': {},
        'best_model': None,
        'timestamp': pd.Timestamp.now().isoformat()
    }
    
    try:
        # Train based on model_type
        if model_type in ['all', 'ann']:
            # Train ANN
            print("[*] Training ANN...")
            ann_result = run_ann(train_df, test_df, predictors, target)
            results['models']['ANN'] = ann_result
        
        if model_type in ['all', 'rf']:
            # Train Random Forest
            print("[*] Training Random Forest...")
            rf_result = run_rf(train_df, test_df, predictors, target)
            results['models']['RandomForest'] = rf_result
        
        if model_type in ['all', 'xgb']:
            # Train XGBoost
            print("[*] Training XGBoost...")
            xgb_result = run_xgb(train_df, test_df, predictors, target)
            results['models']['XGBoost'] = xgb_result
        
        # Find best model
        best_r2 = -np.inf
        best_model_name = None
        
        for model_name, model_result in results['models'].items():
            if model_result.get('success'):
                r2 = model_result['metrics']['r2_score']
                if r2 > best_r2:
                    best_r2 = r2
                    best_model_name = model_name
        
        if best_model_name:
            results['best_model'] = {
                'name': best_model_name,
                'r2_score': best_r2,
                'result': results['models'][best_model_name]
            }
        
        # Summarize results
        results['summary'] = {
            'total_models': 3,
            'successful': sum(1 for r in results['models'].values() if r.get('success')),
            'failed': sum(1 for r in results['models'].values() if not r.get('success'))
        }
        
        print("[✓] All models trained successfully")
        return results
    
    except Exception as e:
        print(f"Error training models: {traceback.format_exc()}")
        return {
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc()
        }
