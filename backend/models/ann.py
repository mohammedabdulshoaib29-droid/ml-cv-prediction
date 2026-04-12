import pandas as pd
import numpy as np
import os
import traceback

# Optimize TensorFlow for CPU and low-memory environments (MUST BE BEFORE IMPORT)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Force CPU-only
tf.config.set_visible_devices([], 'GPU')

def run_ann(train_df, test_df):
    """
    Artificial Neural Network (ANN) Model - FIXED
    - Proper preprocessing with outlier handling
    - Robust scaling for better generalization
    - Improved model architecture
    - No artificial noise addition
    """
    print("[ANN] Initializing ANN model...")
    try:
        predictors = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO"]
        target = "Current"

        tf.random.set_seed(42)
        np.random.seed(42)

        # Validate columns
        for col in predictors + [target]:
            if col not in train_df.columns:
                raise ValueError(f"Missing column in train_df: {col}")
            if col not in test_df.columns:
                raise ValueError(f"Missing column in test_df: {col}")

        # ========================
        # PREPROCESSING
        # ========================
        print("[ANN] Preprocessing data...")
        train_data = train_df[predictors].copy()
        train_target = train_df[target].copy()
        
        test_data = test_df[predictors].copy()
        test_target = test_df[target].copy()

        # Handle missing values
        train_data = train_data.dropna()
        train_target = train_target.loc[train_data.index]
        
        test_data = test_data.dropna()
        test_target = test_target.loc[test_data.index]

        # Remove outliers using IQR method (only on training data)
        Q1 = train_target.quantile(0.25)
        Q3 = train_target.quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        mask = (train_target >= lower_bound) & (train_target <= upper_bound)
        train_data = train_data[mask]
        train_target = train_target[mask]
        print("[ANN] Preprocessed: {} training samples, {} test samples".format(len(train_data), len(test_data)))

        # ========================
        # SCALING - Use RobustScaler for better handling of outliers
        # ========================
        print("[ANN] Scaling data with RobustScaler...")
        scaler = RobustScaler()
        train_data_scaled = scaler.fit_transform(train_data)
        test_data_scaled = scaler.transform(test_data)

        train_target = np.array(train_target)
        test_target = np.array(test_target)

        # ========================
        # MODEL ARCHITECTURE - Improved
        # ========================
        print("[ANN] Building neural network architecture...")
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(len(predictors),)),
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.15),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1)
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.005),
            loss='huber',  # Better for outliers than MSE
            metrics=['mae']
        )

        # Early stopping with patience - aggressive for faster training
        callback = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=8,  # Reduced from 15 for faster training
            restore_best_weights=True,
            min_delta=1e-4
        )

        # ========================
        # TRAINING - OPTIMIZED FOR RENDER
        # ========================
        print("[ANN] Training model (max 50 epochs)...")
        model.fit(
            train_data_scaled,
            train_target,
            validation_split=0.2,
            epochs=50,  # Reduced from 100 for faster execution
            batch_size=8,
            callbacks=[callback],
            verbose=0
        )
        print("[ANN] Training complete")

        # ========================
        # PREDICTIONS - NO ARTIFICIAL NOISE
        # ========================
        test_predictions = model.predict(test_data_scaled, verbose=0).flatten()

        # ========================
        # METRICS
        # ========================
        r2 = float(r2_score(test_target, test_predictions))
        rmse = float(np.sqrt(mean_squared_error(test_target, test_predictions)))
        mae = float(mean_absolute_error(test_target, test_predictions))

        # ========================
        # CV CURVE ANALYSIS - OPTIMIZED FOR SPEED
        # ========================
        voltages = np.linspace(
            train_df["Potential"].min(),
            train_df["Potential"].max(),
            100  # Reduced from 200 for faster computation
        )

        concentrations = np.linspace(10, 90, 40)  # Reduced from 80
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

            cv_input_scaled = scaler.transform(cv_input)
            predicted_current = model.predict(cv_input_scaled, verbose=0).flatten()
            
            # Calculate capacitance using proper formula: C = Q / V
            # where Q is charge (area under curve) and V is voltage
            area = np.trapz(np.abs(predicted_current), voltages)
            
            delta_V = voltages.max() - voltages.min()
            if delta_V > 0:
                # Capacitance in Farads (from area/voltage)
                C = area / delta_V if delta_V > 0 else 0
            else:
                C = 0
            
            capacitance_results.append(max(0, C))  # Ensure non-negative

        best_index = int(np.argmax(capacitance_results))

        print("[ANN] CV analysis complete - Best capacity: {:.6f} F/g".format(capacitance_results[best_index]))
        
        return {
            "r2": r2,
            "rmse": rmse,
            "mae": mae,
            "best_concentration": float(concentrations[best_index]),
            "capacitance": float(capacitance_results[best_index]),
            "graph": {
                "x": concentrations.tolist(),
                "y": [float(val) for val in capacitance_results]
            }
        }

    except Exception as e:
        print("[ANN] Model Error: {}".format(str(e)))
        traceback.print_exc()
        # Return safe fallback values
        return {
            "r2": 0.0,
            "rmse": float('inf'),
            "mae": float('inf'),
            "best_concentration": 50.0,
            "capacitance": 0.0,
            "graph": {"x": [], "y": []}
        }
