"""
Random Forest Model for Capacitance Prediction
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


def run_rf(train_df, test_df, predictors=None, target=None):
    """
    Train and evaluate Random Forest model
    
    Args:
        train_df: Training dataframe
        test_df: Testing dataframe
        predictors: List of feature columns (default CV features)
        target: Target column name (default: 'Current')
    
    Returns:
        Dictionary with results, predictions, and graphs
    """
    
    if predictors is None:
        predictors = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO"]
    if target is None:
        target = "Current"
    
    try:
        # ==================== DATA PREPARATION ====================
        required_cols = predictors + [target]
        train_df = train_df[required_cols].dropna().copy()
        test_df = test_df[required_cols].dropna().copy()
        
        if len(train_df) == 0 or len(test_df) == 0:
            raise ValueError("Training or testing data is empty after cleaning")
        
        X_train = train_df[predictors].values
        y_train = train_df[target].values
        
        X_test = test_df[predictors].values
        y_test = test_df[target].values
        
        # Check for constant target
        if np.unique(y_train).shape[0] <= 1:
            raise ValueError("Target variable is constant in training data")
        
        # ==================== MODEL TRAINING ====================
        # Random Forest doesn't require scaling
        model = RandomForestRegressor(
            n_estimators=200,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1,
            verbose=0
        )
        
        model.fit(X_train, y_train)
        
        # ==================== PREDICTION ====================
        y_pred = model.predict(X_test)
        
        # ==================== EVALUATION ====================
        r2 = float(r2_score(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(np.mean(np.abs(y_test - y_pred)))
        
        # Clamp R² to [0, 1]
        r2 = max(0.0, min(1.0, r2))
        
        # ==================== FEATURE IMPORTANCE ====================
        feature_importance = dict(zip(predictors, model.feature_importances_.tolist()))
        
        # ==================== CAPACITANCE CALCULATION ====================
        voltages = np.linspace(
            train_df["Potential"].min(),
            train_df["Potential"].max(),
            200
        )
        
        scan_rate = train_df["SCAN_RATE"].mean()
        v = scan_rate / 1000 if scan_rate != 0 else 1e-6
        
        mass = 0.002  # kg (2g)
        delta_V = voltages.max() - voltages.min()
        
        concentrations = np.linspace(0, 10, 21)
        capacitance_values = []
        
        for c in concentrations:
            df_pred = pd.DataFrame({
                col: train_df[col].mean() for col in predictors
            }, index=[0])
            df_pred["Zn/Co_Conc"] = c
            
            pred_current = model.predict(df_pred.values)[0]
            area = np.trapz(np.abs([pred_current]), [voltages[0]])
            C = area / (2 * mass * delta_V * v) if (2 * mass * delta_V * v) != 0 else 0
            capacitance_values.append(float(max(0, C)))  # Ensure non-negative
        
        best_idx = int(np.argmax(capacitance_values))
        
        return {
            'success': True,
            'model': 'Random Forest',
            'metrics': {
                'r2_score': r2,
                'rmse': rmse,
                'mae': mae,
                'train_samples': len(train_df),
                'test_samples': len(test_df)
            },
            'predictions': {
                'actual': y_test.tolist(),
                'predicted': y_pred.tolist()
            },
            'feature_importance': feature_importance,
            'best_concentration': float(concentrations[best_idx]),
            'best_capacitance': capacitance_values[best_idx],
            'capacitance_profile': {
                'concentrations': concentrations.tolist(),
                'capacitance_values': capacitance_values
            }
        }
    
    except Exception as e:
        import traceback
        print(f"Random Forest Error: {traceback.format_exc()}")
        return {
            'success': False,
            'model': 'Random Forest',
            'error': str(e)
        }
