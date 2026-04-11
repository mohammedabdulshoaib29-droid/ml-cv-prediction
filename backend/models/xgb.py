import pandas as pd
import numpy as np
from sklearn.model_selection import cross_val_score, KFold
from sklearn.metrics import mean_squared_error, r2_score
from xgboost import XGBRegressor

def run_xgb(train_df, test_df):
    """
    Tensor Neural Network (TNN) - XGBoost Implementation
    Gradient boosting with tensor-based operations
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
    # 2. DEFINE MODEL
    # -------------------------------
    xgb_model = XGBRegressor(
        objective='reg:squarederror',
        eval_metric='rmse',
        learning_rate=0.05,     # smoother learning
        max_depth=6,
        n_estimators=300,       # more trees
        subsample=0.8,          # reduce overfitting
        colsample_bytree=0.8,
        random_state=42,
        n_jobs=-1
    )

    # -------------------------------
    # 3. CROSS VALIDATION
    # -------------------------------
    cv = KFold(n_splits=5, shuffle=True, random_state=42)

    cv_scores = cross_val_score(
        xgb_model,
        train_data,
        train_target,
        scoring='r2',
        cv=cv
    )

    cv_score = float(np.mean(cv_scores))

    # -------------------------------
    # 4. TRAIN MODEL
    # -------------------------------
    xgb_model.fit(train_data, train_target)

    # -------------------------------
    # 5. PREDICTIONS
    # -------------------------------
    test_predictions = xgb_model.predict(test_data)

    # -------------------------------
    # 6. METRICS
    # -------------------------------
    rmse = float(np.sqrt(mean_squared_error(test_target, test_predictions)))
    r2 = float(r2_score(test_target, test_predictions))

    # -------------------------------
    # 7. OPTIMIZATION (CV Curve Analysis)
    # -------------------------------
    voltages = np.linspace(
        train_df["Potential"].min(),
        train_df["Potential"].max(),
        200
    )

    delta_V = voltages.max() - voltages.min()
    mass = 0.002

    scan_rate = train_df["SCAN_RATE"].mean()
    v = scan_rate / 1000 if scan_rate != 0 else 1e-6

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

        predicted_current = xgb_model.predict(cv_input)

        # Fixed integration with trapz
        area = np.trapz(np.abs(predicted_current), voltages)

        denominator = 2 * mass * delta_V * v
        C = area / denominator if denominator != 0 else 0

        capacitance_results.append(C)

    best_index = int(np.argmax(capacitance_results))

    # -------------------------------
    # 8. RETURN RESULT
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
