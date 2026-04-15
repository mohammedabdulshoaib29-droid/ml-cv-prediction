"""
Artificial Neural Network model runner.
"""

import traceback

import numpy as np
import pandas as pd
from sklearn.neural_network import MLPRegressor

from models.pipeline_utils import empty_model_result, finalize_model_result, prepare_datasets


def _build_cv_optimization_result(model, prepared, train_df):
    voltages = np.linspace(
        float(pd.to_numeric(train_df["Potential"], errors="coerce").min()),
        float(pd.to_numeric(train_df["Potential"], errors="coerce").max()),
        200,
    )

    delta_v = float(np.max(voltages) - np.min(voltages))
    mass = 0.002
    scan_rate = float(pd.to_numeric(train_df["SCAN_RATE"], errors="coerce").dropna().mean())
    v = scan_rate / 1000 if scan_rate > 1 else scan_rate
    v = max(v, 1e-5)

    zn_present = pd.to_numeric(train_df["ZN"], errors="coerce").fillna(0).sum() > 0
    co_present = pd.to_numeric(train_df["CO"], errors="coerce").fillna(0).sum() > 0
    concentrations = np.linspace(0, 10, 21)
    results_all = []

    for dopant_type in ["Zn", "Co"]:
        if dopant_type == "Zn" and not zn_present:
            continue
        if dopant_type == "Co" and not co_present:
            continue

        for conc in concentrations:
            zn = 1 if dopant_type == "Zn" else 0
            co = 1 if dopant_type == "Co" else 0

            cv_input = pd.DataFrame(
                {
                    "Potential": voltages,
                    "OXIDATION": 1,
                    "Zn/Co_Conc": conc,
                    "SCAN_RATE": scan_rate,
                    "ZN": zn,
                    "CO": co,
                }
            )

            for column in prepared["feature_columns"]:
                if column not in cv_input.columns:
                    cv_input[column] = 0.0

            cv_input = cv_input[prepared["feature_columns"]]
            predicted_current = model.predict(cv_input)

            area = np.trapezoid(np.abs(predicted_current), voltages)
            denominator = 2 * mass * delta_v * v
            if denominator == 0:
                continue

            capacitance = area / denominator
            energy_density = 0.5 * capacitance * (delta_v ** 2) / 3600
            power_density = energy_density * scan_rate * 1000

            results_all.append(
                {
                    "dopant": dopant_type,
                    "conc": float(conc),
                    "C": float(capacitance),
                    "E": float(energy_density),
                    "P": float(power_density),
                    "current": predicted_current,
                }
            )

    if not results_all:
        raise ValueError("No valid dopant data found")

    best = max(results_all, key=lambda item: item["C"])
    graph_data = {
        "Zn": {
            "x": [item["conc"] for item in results_all if item["dopant"] == "Zn"],
            "y": [item["C"] for item in results_all if item["dopant"] == "Zn"],
        },
        "Co": {
            "x": [item["conc"] for item in results_all if item["dopant"] == "Co"],
            "y": [item["C"] for item in results_all if item["dopant"] == "Co"],
        },
    }

    return {
        "best_dopant": best["dopant"],
        "best_concentration": best["conc"],
        "capacitance": best["C"],
        "energy_density": best["E"],
        "power_density": best["P"],
        "graph": graph_data,
        "cv_curve": {
            "voltage": voltages.tolist(),
            "current": best["current"].tolist(),
        },
    }


def run_ann(train_df, test_df, predictors=None, target=None):
    model_name = 'ANN'

    try:
        required_cols = ["Potential", "Current", "ZN", "CO", "SCAN_RATE"]
        for col in required_cols:
            if col not in train_df.columns:
                raise ValueError(f"Missing column: {col}")

        prepared = prepare_datasets(
            train_df=train_df,
            test_df=test_df,
            predictors=predictors,
            target='Capacitance',
            scale_features=True,
            split_mode='train_plus_inference' if test_df is not None else 'internal'
        )

        model = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            solver='adam',
            learning_rate_init=0.001,
            max_iter=600,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.15
        )
        model.fit(prepared['x_train'], prepared['y_train'])
        predictions = model.predict(prepared['x_test'])
        inference_predictions = model.predict(prepared['x_inference']) if prepared.get('x_inference') is not None else None

        result = finalize_model_result(model_name, prepared, predictions, inference_predictions)
        metrics = result.get("metrics", {})
        result["capacitance"] = float(metrics.get("predicted_capacitance_max", 0.0))
        result["best_concentration"] = None
        result["best_dopant"] = None
        return result

    except Exception as e:
        print(f'Error in ANN model: {traceback.format_exc()}')
        return empty_model_result(model_name, str(e))
