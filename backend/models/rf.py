import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_score, KFold

def run_rf(train_df, test_df):
    """
    Random Forest Regressor Model
    Ensemble method with multiple decision trees
    """

    predictors = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO"]
    target = "Current"

    # -------------------------------
    # 0. VALIDATION
    # -------------------------------
    for col in predictors + [target]:
        if col not in train_df.columns:
            raise ValueError(f"Missing column in train_df: {col}")
        if col not in test_df.columns:
            raise ValueError(f"Missing column in test_df: {col}")

    # -------------------------------
    # 1. SPLIT DATA
    # -------------------------------
    train_data = train_df[predictors].copy()
    train_target = train_df[target].copy()

    test_data = test_df[predictors].copy()
    test_target = test_df[target].copy()

    # Handle missing values
    train_data = train_data.dropna()
    train_target = train_target.loc[train_data.index]

    test_data = test_data.dropna()
    test_target = test_target.loc[test_data.index]

    # -------------------------------
    # 2. MODEL
    # -------------------------------
    rf_model = RandomForestRegressor(
        n_estimators=200,          # increased for stability
        max_depth=10,              # slightly safer
        min_samples_split=5,       # reduce overfitting
        random_state=42,
        n_jobs=-1                  # faster training
    )

    # Cross-validation with shuffle
    cv = KFold(n_splits=5, shuffle=True, random_state=42)

    scores = cross_val_score(
        rf_model,
        train_data,
        train_target,
        cv=cv,
        scoring='r2'
    )

    cv_score = float(np.mean(scores))

    # Train model
    rf_model.fit(train_data, train_target)

    # -------------------------------
    # 3. PREDICTIONS
    # -------------------------------
    test_predictions = rf_model.predict(test_data)

    # -------------------------------
    # 4. METRICS
    # -------------------------------
    r2 = float(r2_score(test_target, test_predictions))
    rmse = float(np.sqrt(mean_squared_error(test_target, test_predictions)))

    # -------------------------------
    # 5. OPTIMIZATION (CV Curve Analysis)
    # -------------------------------
    voltages = np.linspace(
        train_df["Potential"].min(),
        train_df["Potential"].max(),
        200
    )

    delta_V = voltages.max() - voltages.min()
    mass = 0.002

    scan_rate = train_df["SCAN_RATE"].mean()
    v = scan_rate / 1000 if scan_rate != 0 else 1e-6   # avoid division by zero

    oxidation = 1
    zn = 1
    co = 0

    concentrations = np.linspace(0, 10, 21)
    capacitance_results = []

    for conc in concentrations:

        cv_input = pd.DataFrame({
            "Potential": voltages,
            "OXIDATION": oxidation,
            "Zn/Co_Conc": conc,
            "SCAN_RATE": scan_rate,
            "ZN": zn,
            "CO": co
        })

        predicted_current = rf_model.predict(cv_input)

        # Fixed integration with trapz
        area = np.trapz(np.abs(predicted_current), voltages)

        # Safe capacitance calculation
        denominator = 2 * mass * delta_V * v
        C = area / denominator if denominator != 0 else 0

        capacitance_results.append(C)

    best_index = int(np.argmax(capacitance_results))

    # -------------------------------
    # 6. RETURN RESULT
    # -------------------------------
    return {
        "r2": r2,
        "rmse": rmse,
        "cv_score": cv_score,
        "best_concentration": float(concentrations[best_index]),
        "capacitance": float(capacitance_results[best_index]),
        "graph": {
            "x": concentrations.tolist(),
            "y": [float(val) for val in capacitance_results]
        }
    }
