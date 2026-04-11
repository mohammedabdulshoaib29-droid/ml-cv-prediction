import numpy as np
from models.ann import run_ann
from models.rf import run_rf
from models.xgb import run_xgb

def run_all_models(train_df, test_df):
    """
    Run all three models and compare their performance
    
    Returns:
        Dictionary with model comparison, best model, and recommendations
    """

    # ==============================
    # RUN ALL MODELS (SAFE EXECUTION)
    # ==============================
    try:
        ann = run_ann(train_df, test_df)
    except Exception as e:
        print(f"ANN Error: {e}")
        ann = {
            "r2": 0, 
            "rmse": float("inf"), 
            "capacitance": 0, 
            "best_concentration": 0, 
            "graph": {"x": [], "y": []}
        }

    try:
        rf = run_rf(train_df, test_df)
    except Exception as e:
        print(f"RF Error: {e}")
        rf = {
            "r2": 0, 
            "rmse": float("inf"), 
            "capacitance": 0, 
            "best_concentration": 0, 
            "graph": {"x": [], "y": []}
        }

    try:
        xgb = run_xgb(train_df, test_df)
    except Exception as e:
        print(f"XGB Error: {e}")
        xgb = {
            "r2": 0, 
            "rmse": float("inf"), 
            "capacitance": 0, 
            "best_concentration": 0, 
            "graph": {"x": [], "y": []}
        }

    # ==============================
    # PERFORMANCE COMPARISON
    # ==============================
    performance = {
        "ANN": {
            "r2": ann["r2"], 
            "rmse": ann["rmse"],
            "capacitance": ann["capacitance"]
        },
        "RF": {
            "r2": rf["r2"], 
            "rmse": rf["rmse"],
            "capacitance": rf["capacitance"]
        },
        "XGB": {
            "r2": xgb["r2"], 
            "rmse": xgb["rmse"],
            "capacitance": xgb["capacitance"]
        }
    }

    # ==============================
    # CAPACITANCE COMPARISON
    # ==============================
    model_caps = {
        "ANN": ann["capacitance"],
        "RF": rf["capacitance"],
        "XGB": xgb["capacitance"]
    }

    best_model = max(model_caps, key=model_caps.get)
    best_cap = model_caps[best_model]

    # ==============================
    # ENERGY & POWER DENSITY (NEW)
    # ==============================
    try:
        delta_V = test_df["Potential"].max() - test_df["Potential"].min()
        if delta_V > 0:
            energy_density = 0.5 * best_cap * (delta_V ** 2) / 3600
            power_density = energy_density * 3600
        else:
            energy_density = 0
            power_density = 0
    except:
        energy_density = 0
        power_density = 0

    # ==============================
    # GRAPHS FOR ALL MODELS (FIXED)
    # ==============================
    all_graphs = {
        "ANN": ann["graph"],
        "RF": rf["graph"],
        "XGB": xgb["graph"]
    }


    # ==============================
    # DOPANT OPTIMIZATION (FIXED)
    # ==============================
    has_zn = train_df["ZN"].sum() > 0
    has_co = train_df["CO"].sum() > 0

    if has_zn and not has_co:
        best_dopant = "Zn (Zinc)"
    elif has_co and not has_zn:
        best_dopant = "Co (Cobalt)"
    elif has_zn and has_co:
        best_dopant = "Zn/Co (Mixed)"
    else:
        best_dopant = "None"

    # ==============================
    # MODEL PERFORMANCE TABLE
    # ==============================
    table = [
        {
            "model": "Artificial Neural Network (ANN)",
            "r2": ann["r2"],
            "rmse": ann["rmse"],
            "capacitance": ann["capacitance"],
            "best_concentration": ann["best_concentration"]
        },
        {
            "model": "Random Forest (RF)",
            "r2": rf["r2"],
            "rmse": rf["rmse"],
            "capacitance": rf["capacitance"],
            "best_concentration": rf["best_concentration"]
        },
        {
            "model": "XGBoost (XGB)",
            "r2": xgb["r2"],
            "rmse": xgb["rmse"],
            "capacitance": xgb["capacitance"],
            "best_concentration": xgb["best_concentration"]
        }
    ]

    # ==============================
    # RECOMMENDATIONS
    # ==============================
    recommendations = []
    
    # R² Score recommendation
    best_r2_model = max(performance, key=lambda x: performance[x]["r2"])
    recommendations.append(f"Best Predictive Power: {best_r2_model} (R² = {performance[best_r2_model]['r2']:.4f})")
    
    # RMSE recommendation
    valid_rmse = {k: v["rmse"] for k, v in performance.items() if v["rmse"] != float("inf")}
    if valid_rmse:
        best_rmse_model = min(valid_rmse, key=valid_rmse.get)
        recommendations.append(f"Most Accurate Predictions: {best_rmse_model} (RMSE = {valid_rmse[best_rmse_model]:.4f})")
    
    # Capacitance recommendation
    recommendations.append(f"Highest Capacitance: {best_model} ({best_cap:.2f} F/g)")
    
    # Dopant recommendation
    recommendations.append(f"Recommended Dopant: {best_dopant}")

    # ==============================
    # FINAL OUTPUT
    # ==============================
    return {
        "performance": performance,
        "best_model": best_model,
        "best_dopant": best_dopant,
        "best_concentration": float(best_model_data["best_concentration"]),
        "capacitance": float(best_cap),
        "energy_density": float(energy_density),
        "power_density": float(power_density),
        "graphs": all_graphs,
        "table": table,
        "recommendations": recommendations
    }
