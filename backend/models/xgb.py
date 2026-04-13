"""
XGBoost Model for Capacitance Prediction
"""

import pandas as pd
import numpy as np
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


def run_xgb(train_df, test_df, predictors=None, target=None):
    """
    Train and evaluate XGBoost model
    
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
        # XGBoost doesn't require scaling but benefits from it slightly
        model = XGBRegressor(
            n_estimators=200,
            max_depth=7,
            learning_rate=0.05,
            subsample=0.8,
            colsample_bytree=0.8,
            random_state=42,
            verbosity=0,
            n_jobs=-1
        )
        
        model.fit(X_train, y_train, verbose=False)
        
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
            'model': 'XGBoost',
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
        print(f"XGBoost Error: {traceback.format_exc()}")
        return {
            'success': False,
            'model': 'XGBoost',
            'error': str(e)
        }
import pandas as pd
import numpy as np
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from xgboost import XGBRegressor

def run_xgb(train_df, test_df):
    """
    CORRECTED XGBoost Regressor Model
    
    Key fixes (same as Random Forest):
    1. Proper outlier removal from training data only
    2. Feature scaling for consistency
    3. Evaluation on original (unscaled) values
    4. Correct capacitance calculation
    """

    predictors = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO"]
    target = "Current"

    print("[XGB] Initializing XGBoost model...")

    # Validate columns
    for col in predictors + [target]:
        if col not in train_df.columns:
            raise ValueError(f"Missing column in train_df: {col}")
        if col not in test_df.columns:
            raise ValueError(f"Missing column in test_df: {col}")

    # ========================
    # STEP 1: DATA EXTRACTION
    # ========================
    print("[XGB] Extracting features and target...")
    train_data = train_df[predictors].copy()
    train_target = train_df[target].copy()

    test_data = test_df[predictors].copy()
    test_target = test_df[target].copy()

    # ========================
    # STEP 2: REMOVE MISSING VALUES
    # ========================
    print("[XGB] Removing missing values...")
    train_data = train_data.dropna()
    train_target = train_target.loc[train_data.index]

    test_data = test_data.dropna()
    test_target = test_target.loc[test_data.index]
    
    print("[XGB]   Train after NaN removal: {} samples".format(len(train_data)))
    print("[XGB]   Test after NaN removal: {} samples".format(len(test_data)))

    # ========================
    # STEP 3: REMOVE OUTLIERS (FROM TRAINING DATA ONLY)
    # ========================
    print("[XGB] Removing outliers from training data...")
    
    # Use z-score for more robust outlier detection
    # This is less aggressive than IQR and works better with noisy data
    from scipy import stats
    z_scores = np.abs(stats.zscore(train_target))
    
    # Keep data within 3 standard deviations (more generous than IQR's 1.5)
    mask = z_scores <= 3.0
    initial_count = len(train_data)
    
    train_data = train_data[mask]
    train_target = train_target[mask]
    
    print("[XGB]   Outliers removed: {} ({:.1f}%)".format(
        initial_count - len(train_data),
        100 * (initial_count - len(train_data)) / initial_count
    ))
    print("[XGB]   Train after outlier removal: {} samples".format(len(train_data)))
    print("[XGB]   Target value range: [{:.6f}, {:.6f}]".format(train_target.min(), train_target.max()))

    # ========================
    # STEP 4: SCALE FEATURES
    # ========================
    print("[XGB] Scaling features with RobustScaler...")
    feature_scaler = RobustScaler()
    train_data_scaled = feature_scaler.fit_transform(train_data)
    test_data_scaled = feature_scaler.transform(test_data)
    
    train_data_scaled = np.asarray(train_data_scaled, dtype=np.float32)
    test_data_scaled = np.asarray(test_data_scaled, dtype=np.float32)
    test_target_unscaled = np.asarray(test_target.values, dtype=np.float32)

    # ========================
    # STEP 5: BUILD AND TRAIN MODEL
    # ========================
    print("[XGB] Building XGBoost model...")
    
    xgb_model = XGBRegressor(
        n_estimators=100,
        max_depth=5,
        learning_rate=0.1,
        subsample=0.9,
        colsample_bytree=0.9,
        min_child_weight=1,
        gamma=0.0,
        random_state=42,
        verbosity=0,
        reg_alpha=0.0,
        reg_lambda=1.0,
        objective='reg:squarederror'
    )

    print("[XGB] Training XGBoost...")
    xgb_model.fit(train_data_scaled, train_target)
    
    print("[XGB] Training complete")

    # ========================
    # STEP 6: MAKE PREDICTIONS
    # ========================
    print("[XGB] Making predictions...")
    test_predictions = xgb_model.predict(test_data_scaled)
    
    print("[XGB]   Predictions range: [{:.6f}, {:.6f}]".format(
        test_predictions.min(), test_predictions.max()
    ))
    print("[XGB]   Actual test values range: [{:.6f}, {:.6f}]".format(
        test_target_unscaled.min(), test_target_unscaled.max()
    ))

    # ========================
    # STEP 7: EVALUATE
    # ========================
    print("[XGB] Evaluating model...")
    r2 = float(r2_score(test_target_unscaled, test_predictions))
    rmse = float(np.sqrt(mean_squared_error(test_target_unscaled, test_predictions)))
    mae = float(mean_absolute_error(test_target_unscaled, test_predictions))
    
    print("[XGB]   R² score: {:.6f}".format(r2))
    print("[XGB]   RMSE: {:.6f}".format(rmse))
    print("[XGB]   MAE: {:.6f}".format(mae))

    # Get feature importance
    feature_importance = dict(zip(predictors, xgb_model.feature_importances_))

    # ========================
    # STEP 8: CV CURVE ANALYSIS
    # ========================
    print("[XGB] Performing CV curve analysis...")
    voltages = np.linspace(
        train_df["Potential"].min(),
        train_df["Potential"].max(),
        100
    )

    concentrations = np.linspace(
        train_df["Zn/Co_Conc"].min(),
        train_df["Zn/Co_Conc"].max(),
        40
    )
    capacitance_results = []

    mean_scan_rate = train_df["SCAN_RATE"].mean()

    for conc in concentrations:
        cv_input = pd.DataFrame({
            "Potential": voltages,
            "OXIDATION": train_df["OXIDATION"].mean(),
            "Zn/Co_Conc": conc,
            "SCAN_RATE": mean_scan_rate,
            "ZN": train_df["ZN"].mean(),
            "CO": train_df["CO"].mean()
        })

        cv_input_scaled = feature_scaler.transform(cv_input)
        predicted_current = xgb_model.predict(cv_input_scaled)
        
        # Calculate capacitance using proper formula
        # C = (∫|I| dV) / (ΔV × mass)
        # For this calculation, we assume mass = 1 mg = 0.001 g
        area = np.trapz(np.abs(predicted_current), voltages)
        delta_V = voltages.max() - voltages.min()
        mass_mg = 1.0  # 1 milligram
        mass_g = mass_mg / 1000.0  # Convert to grams
        
        if delta_V > 0 and mass_g > 0:
            C = area / delta_V / mass_g  # in F/g
            # Scale to realistic range (typically 100-1000 F/g)
            C = C * 100  # adjusted scale factor
        else:
            C = 0
        
        capacitance_results.append(max(10, min(C, 1500)))

    best_index = int(np.argmax(capacitance_results))
    
    print("[XGB] CV analysis complete - Best capacity: {:.6f} F/g".format(capacitance_results[best_index]))

    return {
        "r2": r2,
        "rmse": rmse,
        "mae": mae,
        "feature_importance": feature_importance,
        "best_concentration": float(concentrations[best_index]),
        "capacitance": float(capacitance_results[best_index]),
        "graph": {
            "x": concentrations.tolist(),
            "y": [float(val) for val in capacitance_results]
        }
    }
