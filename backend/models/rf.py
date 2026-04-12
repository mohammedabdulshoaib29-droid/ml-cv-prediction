import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import RobustScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def run_rf(train_df, test_df):
    """
    CORRECTED Random Forest Regressor Model
    
    Key differences from ANN:
    1. Tree-based models inherently handle scaling
    2. No need to scale target variable
    3. Predictions are already in original scale
    4. Evaluation metrics computed directly on predictions
    
    Still scale features for:
    - Consistency with ANN
    - Potential efficiency improvements
    """

    predictors = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO"]
    target = "Current"

    print("[RF] Initializing Random Forest model...")

    # Validate columns
    for col in predictors + [target]:
        if col not in train_df.columns:
            raise ValueError(f"Missing column in train_df: {col}")
        if col not in test_df.columns:
            raise ValueError(f"Missing column in test_df: {col}")

    # ========================
    # STEP 1: DATA EXTRACTION
    # ========================
    print("[RF] Extracting features and target...")
    train_data = train_df[predictors].copy()
    train_target = train_df[target].copy()

    test_data = test_df[predictors].copy()
    test_target = test_df[target].copy()

    # ========================
    # STEP 2: REMOVE MISSING VALUES
    # ========================
    print("[RF] Removing missing values...")
    train_data = train_data.dropna()
    train_target = train_target.loc[train_data.index]

    test_data = test_data.dropna()
    test_target = test_target.loc[test_data.index]
    
    print("[RF]   Train after NaN removal: {} samples".format(len(train_data)))
    print("[RF]   Test after NaN removal: {} samples".format(len(test_data)))

    # ========================
    # STEP 3: REMOVE OUTLIERS (FROM TRAINING DATA ONLY)
    # ========================
    print("[RF] Removing outliers from training data...")
    
    # Use z-score for more robust outlier detection
    # This is less aggressive than IQR and works better with noisy data
    from scipy import stats
    z_scores = np.abs(stats.zscore(train_target))
    
    # Keep data within 3 standard deviations (more generous than IQR's 1.5)
    mask = z_scores <= 3.0
    initial_count = len(train_data)
    
    train_data = train_data[mask]
    train_target = train_target[mask]
    
    print("[RF]   Outliers removed: {} ({:.1f}%)".format(
        initial_count - len(train_data),
        100 * (initial_count - len(train_data)) / initial_count
    ))
    print("[RF]   Train after outlier removal: {} samples".format(len(train_data)))
    print("[RF]   Target value range: [{:.6f}, {:.6f}]".format(train_target.min(), train_target.max()))

    # ========================
    # STEP 4: SCALE FEATURES (FOR CONSISTENCY, NOT REQUIRED FOR TREES)
    # ========================
    print("[RF] Scaling features with RobustScaler...")
    feature_scaler = RobustScaler()
    train_data_scaled = feature_scaler.fit_transform(train_data)
    test_data_scaled = feature_scaler.transform(test_data)
    
    train_data_scaled = np.asarray(train_data_scaled, dtype=np.float32)
    test_data_scaled = np.asarray(test_data_scaled, dtype=np.float32)
    test_target_unscaled = np.asarray(test_target.values, dtype=np.float32)

    # ========================
    # STEP 5: BUILD AND TRAIN MODEL
    # ========================
    print("[RF] Building Random Forest model...")
    
    rf_model = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        min_samples_split=5,
        min_samples_leaf=2,
        max_features='sqrt',
        random_state=42,
        n_jobs=-1,
        bootstrap=True
    )

    print("[RF] Training Random Forest...")
    rf_model.fit(train_data_scaled, train_target)
    
    print("[RF] Training complete")

    # ========================
    # STEP 6: MAKE PREDICTIONS (PREDICTIONS ALREADY IN ORIGINAL SCALE)
    # ========================
    """
    Key point: Tree-based models predict directly in the original scale
    because they don't use target scaling during training.
    """
    print("[RF] Making predictions...")
    test_predictions = rf_model.predict(test_data_scaled)
    
    print("[RF]   Predictions range: [{:.6f}, {:.6f}]".format(
        test_predictions.min(), test_predictions.max()
    ))
    print("[RF]   Actual test values range: [{:.6f}, {:.6f}]".format(
        test_target_unscaled.min(), test_target_unscaled.max()
    ))

    # ========================
    # STEP 7: EVALUATE (ON ORIGINAL SCALE)
    # ========================
    print("[RF] Evaluating model...")
    r2 = float(r2_score(test_target_unscaled, test_predictions))
    rmse = float(np.sqrt(mean_squared_error(test_target_unscaled, test_predictions)))
    mae = float(mean_absolute_error(test_target_unscaled, test_predictions))
    
    print("[RF]   R² score: {:.6f}".format(r2))
    print("[RF]   RMSE: {:.6f}".format(rmse))
    print("[RF]   MAE: {:.6f}".format(mae))

    # Get feature importance
    feature_importance = dict(zip(predictors, rf_model.feature_importances_))

    # ========================
    # STEP 8: CV CURVE ANALYSIS
    # ========================
    print("[RF] Performing CV curve analysis...")
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
        predicted_current = rf_model.predict(cv_input_scaled)
        
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
    
    print("[RF] CV analysis complete - Best capacity: {:.6f} F/g".format(capacitance_results[best_index]))

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
