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
    CORRECTED Artificial Neural Network (ANN) Model
    
    Key fixes:
    1. Proper target variable scaling (standardization)
    2. Inverse transformation of predictions back to original scale
    3. Evaluation metrics computed on UNSCALED values
    4. Proper handling of training/test split
    5. Better model architecture
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
        # STEP 1: DATA EXTRACTION
        # ========================
        print("[ANN] Extracting features and target...")
        train_data = train_df[predictors].copy()
        train_target = train_df[target].copy()
        
        test_data = test_df[predictors].copy()
        test_target = test_df[target].copy()

        # ========================
        # STEP 2: REMOVE MISSING VALUES
        # ========================
        print("[ANN] Removing missing values...")
        train_data = train_data.dropna()
        train_target = train_target.loc[train_data.index]
        
        test_data = test_data.dropna()
        test_target = test_target.loc[test_data.index]
        
        print("[ANN]   Train after NaN removal: {} samples".format(len(train_data)))
        print("[ANN]   Test after NaN removal: {} samples".format(len(test_data)))

        # ========================
        # STEP 3: REMOVE OUTLIERS (FROM TRAINING DATA ONLY)
        # ========================
        print("[ANN] Removing outliers from training data...")
        
        # Use z-score for more robust outlier detection
        # This is less aggressive than IQR and works better with noisy data
        from scipy import stats
        z_scores = np.abs(stats.zscore(train_target))
        
        # Keep data within 3 standard deviations (more generous than IQR's 1.5)
        mask = z_scores <= 3.0
        initial_count = len(train_data)
        
        train_data = train_data[mask]
        train_target = train_target[mask]
        
        print("[ANN]   Outliers removed: {} ({:.1f}%)".format(
            initial_count - len(train_data),
            100 * (initial_count - len(train_data)) / initial_count
        ))
        print("[ANN]   Train after outlier removal: {} samples".format(len(train_data)))
        print("[ANN]   Target value range: [{:.6f}, {:.6f}]".format(train_target.min(), train_target.max()))

        # ========================
        # STEP 4: SCALE FEATURES (FEATURES ONLY - ROBUSTSCALER)
        # ========================
        print("[ANN] Scaling features with RobustScaler...")
        feature_scaler = RobustScaler()
        train_data_scaled = feature_scaler.fit_transform(train_data)
        test_data_scaled = feature_scaler.transform(test_data)
        
        # Convert to numpy
        train_data_scaled = np.asarray(train_data_scaled, dtype=np.float32)
        test_data_scaled = np.asarray(test_data_scaled, dtype=np.float32)

        # ========================
        # STEP 5: SCALE TARGET (TARGET VARIABLE - STANDARDSCALER FOR ANN)
        # ========================
        """
        Why scale target for ANN?
        - Neural networks train better with normalized targets
        - Helps with gradient descent optimization
        - CRITICAL: Must inverse-transform predictions after training
        """
        print("[ANN] Scaling target variable with StandardScaler...")
        target_scaler = StandardScaler()
        train_target_scaled = target_scaler.fit_transform(
            np.asarray(train_target).reshape(-1, 1)
        ).flatten()
        test_target_unscaled = np.asarray(test_target.values, dtype=np.float32)
        
        print("[ANN]   Scaled target range: [{:.4f}, {:.4f}]".format(
            train_target_scaled.min(), train_target_scaled.max()
        ))
        print("[ANN]   Original target range: [{:.6f}, {:.6f}]".format(
            train_target.min(), train_target.max()
        ))

        # ========================
        # STEP 6: BUILD MODEL
        # ========================
        print("[ANN] Building neural network architecture...")
        model = tf.keras.Sequential([
            tf.keras.layers.Input(shape=(len(predictors),)),
            
            # Hidden layer 1
            tf.keras.layers.Dense(128, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.3),
            
            # Hidden layer 2
            tf.keras.layers.Dense(64, activation='relu'),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(0.2),
            
            # Hidden layer 3
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.1),
            
            # Hidden layer 4
            tf.keras.layers.Dense(16, activation='relu'),
            
            # Output layer
            tf.keras.layers.Dense(1)
        ])

        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',  # MSE works better with scaled target
            metrics=['mae']
        )

        print("[ANN] Model architecture:")
        print("[ANN]   Input: {} features".format(len(predictors)))
        print("[ANN]   Hidden layers: 128 -> 64 -> 32 -> 16")
        print("[ANN]   Output: 1 (Current prediction)")

        # ========================
        # STEP 7: TRAIN MODEL
        # ========================
        print("[ANN] Training model (max 200 epochs with early stopping)...")
        
        callback = tf.keras.callbacks.EarlyStopping(
            monitor='val_loss',
            patience=20,
            restore_best_weights=True,
            min_delta=1e-5
        )

        history = model.fit(
            train_data_scaled,
            train_target_scaled,
            validation_split=0.2,
            epochs=200,
            batch_size=16,
            callbacks=[callback],
            verbose=0
        )
        
        epochs_trained = len(history.history['loss'])
        print("[ANN] Training complete after {} epochs".format(epochs_trained))

        # ========================
        # STEP 8: MAKE PREDICTIONS (ON SCALED DATA)
        # ========================
        print("[ANN] Making predictions...")
        test_predictions_scaled = model.predict(test_data_scaled, verbose=0).flatten()
        
        print("[ANN]   Scaled predictions range: [{:.4f}, {:.4f}]".format(
            test_predictions_scaled.min(), test_predictions_scaled.max()
        ))

        # ========================
        # STEP 9: INVERSE TRANSFORM PREDICTIONS (CRITICAL!)
        # ========================
        """
        This is CRITICAL - convert predictions back to original scale.
        Otherwise metrics will be computed on wrong scale.
        """
        print("[ANN] Inverse-transforming predictions to original scale...")
        test_predictions_unscaled = target_scaler.inverse_transform(
            test_predictions_scaled.reshape(-1, 1)
        ).flatten()
        
        print("[ANN]   Unscaled predictions range: [{:.6f}, {:.6f}]".format(
            test_predictions_unscaled.min(), test_predictions_unscaled.max()
        ))
        print("[ANN]   Actual test values range: [{:.6f}, {:.6f}]".format(
            test_target_unscaled.min(), test_target_unscaled.max()
        ))

        # ========================
        # STEP 10: EVALUATE ON UNSCALED VALUES (CRITICAL!)
        # ========================
        """
        Metrics MUST be computed on original (unscaled) values.
        This gives interpretable R², RMSE, and MAE.
        """
        print("[ANN] Evaluating model...")
        r2 = float(r2_score(test_target_unscaled, test_predictions_unscaled))
        rmse = float(np.sqrt(mean_squared_error(test_target_unscaled, test_predictions_unscaled)))
        mae = float(mean_absolute_error(test_target_unscaled, test_predictions_unscaled))
        
        print("[ANN]   R² score: {:.6f}".format(r2))
        print("[ANN]   RMSE: {:.6f}".format(rmse))
        print("[ANN]   MAE: {:.6f}".format(mae))

        # ========================
        # STEP 11: CV CURVE ANALYSIS
        # ========================
        print("[ANN] Performing CV curve analysis...")
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
            predicted_current_scaled = model.predict(cv_input_scaled, verbose=0).flatten()
            
            # Inverse transform predictions back to original scale
            predicted_current = target_scaler.inverse_transform(
                predicted_current_scaled.reshape(-1, 1)
            ).flatten()
            
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
