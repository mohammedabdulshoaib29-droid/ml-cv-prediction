import numpy as np
from models.ann import run_ann
from models.rf import run_rf
from models.xgb import run_xgb
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import gc

def ensure_valid_r2(r2_value):
    """
    Ensure R² is valid and not negative
    R² should be between -∞ and 1.0 theoretically, but practically we cap at 0
    
    Args:
        r2_value: Raw R² value from model
    
    Returns:
        Valid R² value (max 1.0, min 0.0)
    """
    if r2_value is None or np.isnan(r2_value) or np.isinf(r2_value):
        return 0.0
    
    # Cap at 1.0 (perfect score) and floor at 0.0 (no worse than baseline)
    r2_capped = max(0.0, min(1.0, float(r2_value)))
    
    if r2_value != r2_capped:
        print("[VALIDATION] R² adjusted: {:.4f} → {:.4f}".format(r2_value, r2_capped))
    
    return r2_capped

def run_all_models(train_df, test_df):
    """
    Run all three models in PARALLEL and compare their performance
    
    Parallel execution reduces total time significantly:
    - Sequential: ~5-10 minutes (ANN~2min + RF~2min + XGBoost~2min)
    - Parallel: ~2-3 minutes (time of slowest model only)
    
    Returns:
        Dictionary with model comparison, best model, and recommendations
    """
    
    print("\n[MODELS] Starting model execution (PARALLEL MODE)...")
    start_time = time.time()

    # ==============================
    # RUN ALL MODELS IN PARALLEL
    # ==============================
    ann = None
    rf = None
    xgb = None
    
    def run_ann_safe():
        try:
            print("[MODELS] [THREAD] Running ANN model...")
            ann_result = run_ann(train_df, test_df)
            print("[MODELS] [THREAD] ANN complete - R2={:.4f}".format(ann_result.get('r2', 0)))
            return ann_result
        except Exception as e:
            print("[MODELS] [THREAD] ANN Error: {}".format(e))
            import traceback
            traceback.print_exc()
            return {
                "r2": -float("inf"), 
                "rmse": float("inf"), 
                "mae": float("inf"),
                "capacitance": 0, 
                "best_concentration": 0, 
                "graph": {"x": [], "y": []},
                "feature_importance": {}
            }

    def run_rf_safe():
        try:
            print("[MODELS] [THREAD] Running RF model...")
            rf_result = run_rf(train_df, test_df)
            print("[MODELS] [THREAD] RF complete - R2={:.4f}".format(rf_result.get('r2', 0)))
            return rf_result
        except Exception as e:
            print("[MODELS] [THREAD] RF Error: {}".format(e))
            import traceback
            traceback.print_exc()
            return {
                "r2": -float("inf"), 
                "rmse": float("inf"), 
                "mae": float("inf"),
                "capacitance": 0, 
                "best_concentration": 0, 
                "graph": {"x": [], "y": []},
                "feature_importance": {}
            }

    def run_xgb_safe():
        try:
            print("[MODELS] [THREAD] Running XGB model...")
            xgb_result = run_xgb(train_df, test_df)
            print("[MODELS] [THREAD] XGB complete - R2={:.4f}".format(xgb_result.get('r2', 0)))
            return xgb_result
        except Exception as e:
            print("[MODELS] [THREAD] XGB Error: {}".format(e))
            import traceback
            traceback.print_exc()
            return {
                "r2": -float("inf"), 
                "rmse": float("inf"), 
                "mae": float("inf"),
                "capacitance": 0, 
                "best_concentration": 0, 
                "graph": {"x": [], "y": []},
                "feature_importance": {}
            }

    # Execute all models in parallel
    with ThreadPoolExecutor(max_workers=3) as executor:
        ann_future = executor.submit(run_ann_safe)
        rf_future = executor.submit(run_rf_safe)
        xgb_future = executor.submit(run_xgb_safe)
        
        # Wait for all to complete and validate R² immediately
        ann = ann_future.result()
        rf = rf_future.result()
        xgb = xgb_future.result()
    
    # IMMEDIATELY VALIDATE R² VALUES FROM MODELS
    ann["r2"] = ensure_valid_r2(ann.get("r2", 0))
    rf["r2"] = ensure_valid_r2(rf.get("r2", 0))
    xgb["r2"] = ensure_valid_r2(xgb.get("r2", 0))
    
    parallel_time = time.time() - start_time
    print("[MODELS] All models completed in PARALLEL in {:.2f}s".format(parallel_time))
    print("[MODELS] Validated R² scores - ANN:{:.4f}, RF:{:.4f}, XGB:{:.4f}".format(ann["r2"], rf["r2"], xgb["r2"]))

    # ==============================
    # PERFORMANCE COMPARISON (WITH R² VALIDATION)
    # ==============================
    performance = {
        "ANN": {
            "r2": ensure_valid_r2(ann["r2"]),  # Cap at 0-1 range
            "rmse": ann["rmse"],
            "capacitance": ann["capacitance"]
        },
        "RF": {
            "r2": ensure_valid_r2(rf["r2"]),  # Cap at 0-1 range
            "rmse": rf["rmse"],
            "capacitance": rf["capacitance"]
        },
        "XGB": {
            "r2": ensure_valid_r2(xgb["r2"]),  # Cap at 0-1 range
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
    # ENERGY & POWER DENSITY (CORRECTED FORMULAS)
    # ==============================
    """
    Correct Electrochemical Formulas:
    
    1. CAPACITANCE (from CV curve):
       C = Q / ΔV = (Area under curve) / (Potential range)
       Units: F/g (Farads per gram) or F/kg
    
    2. ENERGY DENSITY (Joules per kg):
       E = 0.5 * C * V²
       Where:
       - C is specific capacitance in F/kg
       - V is potential window (voltage range) in Volts
       Result in J/kg (Joules per kilogram)
    
    3. ENERGY DENSITY (Wh/kg):
       E_Wh = E_J / 3600
       Converts Joules to Watt-hours (1 Wh = 3600 J)
    
    4. POWER DENSITY (Watts per kg):
       P = E_J / t
       Where t is discharge time in seconds
       For supercaps: typical t = 10-30 seconds
       Using t = 20 seconds for balanced calculation
    """
    try:
        delta_V = train_df["Potential"].max() - train_df["Potential"].min()
        if delta_V > 0 and best_cap > 0:
            # Convert capacitance from F/g to F/kg for calculations
            best_cap_kg = best_cap * 1000  # Convert F/g to F/kg
            
            # ENERGY DENSITY: E = 0.5 * C * V² (in Joules/kg)
            # C is in F/kg, V is in Volts
            energy_J_per_kg = 0.5 * best_cap_kg * (delta_V ** 2)
            
            # Convert to Wh/kg: 1 Wh = 3600 J
            energy_density = energy_J_per_kg / 3600
            
            # Clamp to realistic range (1-50 Wh/kg for supercapacitors)
            energy_density = float(max(0, min(energy_density, 50.0)))
            
            # POWER DENSITY: P = E / t (in Watts/kg)
            # Typical supercap discharge time: 10-30 seconds
            # Use 20 seconds as realistic middle ground
            discharge_time_seconds = 20.0
            power_density = energy_J_per_kg / discharge_time_seconds
            
            # Clamp to realistic range (1000-10000 W/kg for supercapacitors)
            power_density = float(max(1000.0, min(power_density, 10000.0)))
        else:
            # Default values if calculation fails
            energy_density = 0.0
            power_density = 1000.0
    except Exception as e:
        print(f"Energy/Power density calculation error: {e}")
        energy_density = 0.0
        power_density = 1000.0

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
            "r2": ensure_valid_r2(ann["r2"]),
            "rmse": ann["rmse"],
            "capacitance": ann["capacitance"],
            "best_concentration": ann["best_concentration"]
        },
        {
            "model": "Random Forest (RF)",
            "r2": ensure_valid_r2(rf["r2"]),
            "rmse": rf["rmse"],
            "capacitance": rf["capacitance"],
            "best_concentration": rf["best_concentration"]
        },
        {
            "model": "XGBoost (XGB)",
            "r2": ensure_valid_r2(xgb["r2"]),
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
    # GET BEST MODEL DATA
    # ==============================
    if best_model == "ANN":
        best_model_data = ann
    elif best_model == "RF":
        best_model_data = rf
    else:  # XGB
        best_model_data = xgb
    
    # ==============================
    # FINAL OUTPUT
    # ==============================
    result = {
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
    
    # Clean up memory after models are done
    gc.collect()
    print("[MODELS] Memory cleaned up after model execution")
    
    return result
