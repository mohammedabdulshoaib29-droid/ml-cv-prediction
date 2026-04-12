import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

def run_rf(train_df, test_df):
    """
    Random Forest Regressor Model - FIXED
    - Proper outlier removal
    - Improved hyperparameters
    - Better data handling
    - No artificial noise
    """

    predictors = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO"]
    target = "Current"

    # Validate columns
    for col in predictors + [target]:
        if col not in train_df.columns:
            raise ValueError(f"Missing column in train_df: {col}")
        if col not in test_df.columns:
            raise ValueError(f"Missing column in test_df: {col}")

    # ========================
    # PREPROCESSING
    # ========================
    train_data = train_df[predictors].copy()
    train_target = train_df[target].copy()

    test_data = test_df[predictors].copy()
    test_target = test_df[target].copy()

    # Handle missing values
    train_data = train_data.dropna()
    train_target = train_target.loc[train_data.index]

    test_data = test_data.dropna()
    test_target = test_target.loc[test_data.index]

    # Remove outliers from training data only
    Q1 = train_target.quantile(0.25)
    Q3 = train_target.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    mask = (train_target >= lower_bound) & (train_target <= upper_bound)
    train_data = train_data[mask]
    train_target = train_target[mask]

    # ========================
    # MODEL WITH OPTIMIZED HYPERPARAMETERS FOR RENDER
    # ========================
    rf_model = RandomForestRegressor(
        n_estimators=100,           # Reduced from 300 for faster training
        max_depth=10,               # Reduced from 15
        min_samples_split=5,        # Increased from 3 for faster split
        min_samples_leaf=2,         # smaller leaf size
        max_features='sqrt',        # use sqrt of features
        random_state=42,
        n_jobs=-1,                  # parallel processing
        bootstrap=True              # use bootstrap samples
    )

    # Train model
    rf_model.fit(train_data, train_target)

    # ========================
    # PREDICTIONS - NO ARTIFICIAL NOISE
    # ========================
    test_predictions = rf_model.predict(test_data)

    # ========================
    # METRICS
    # ========================
    r2 = float(r2_score(test_target, test_predictions))
    rmse = float(np.sqrt(mean_squared_error(test_target, test_predictions)))
    mae = float(mean_absolute_error(test_target, test_predictions))

    # Get feature importance
    feature_importance = dict(zip(predictors, rf_model.feature_importances_))

    # ========================
    # CV CURVE ANALYSIS - OPTIMIZED FOR SPEED
    # ========================
    voltages = np.linspace(
        train_df["Potential"].min(),
        train_df["Potential"].max(),
        100  # Reduced from 200 for faster computation
    )

    concentrations = np.linspace(0, 10, 15)  # Reduced from 21
    capacitance_results = []

    # Use mean values for stable prediction
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

        predicted_current = rf_model.predict(cv_input)
        
        # Calculate capacitance using proper formula: C = Q / V
        area = np.trapz(np.abs(predicted_current), voltages)
        
        delta_V = voltages.max() - voltages.min()
        if delta_V > 0:
            C = area / delta_V
        else:
            C = 0
        
        capacitance_results.append(max(0, C))

    best_index = int(np.argmax(capacitance_results))

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
