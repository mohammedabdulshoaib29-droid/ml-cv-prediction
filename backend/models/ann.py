"""
Artificial Neural Network Model for Capacitance Prediction
"""

import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')


def run_ann(train_df, test_df, predictors=None, target=None):
    """
    Train and evaluate ANN model
    
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
        # Filter columns and drop NaNs
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
        
        # ==================== SCALING ====================
        # Scale features
        feature_scaler = StandardScaler()
        X_train_scaled = feature_scaler.fit_transform(X_train)
        X_test_scaled = feature_scaler.transform(X_test)
        
        # Scale target (IMPORTANT for ANN)
        target_scaler = StandardScaler()
        y_train_scaled = target_scaler.fit_transform(y_train.reshape(-1, 1)).flatten()
        
        # ==================== MODEL BUILDING ====================
        model = tf.keras.Sequential([
            tf.keras.layers.Dense(64, activation='relu', input_shape=(len(predictors),)),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.1),
            tf.keras.layers.Dense(16, activation='relu'),
            tf.keras.layers.Dense(1, activation='linear')
        ])
        
        model.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss='mse',
            metrics=['mae']
        )
        
        # ==================== TRAINING ====================
        history = model.fit(
            X_train_scaled, y_train_scaled,
            epochs=100,
            batch_size=32,
            validation_split=0.2,
            verbose=0,
            callbacks=[
                tf.keras.callbacks.EarlyStopping(
                    monitor='val_loss',
                    patience=15,
                    restore_best_weights=True
                )
            ]
        )
        
        # ==================== PREDICTION ====================
        y_pred_scaled = model.predict(X_test_scaled, verbose=0).flatten()
        y_pred = target_scaler.inverse_transform(y_pred_scaled.reshape(-1, 1)).flatten()
        
        # ==================== EVALUATION ====================
        r2 = float(r2_score(y_test, y_pred))
        rmse = float(np.sqrt(mean_squared_error(y_test, y_pred)))
        mae = float(np.mean(np.abs(y_test - y_pred)))
        
        # Clamp R² to [0, 1]
        r2 = max(0.0, min(1.0, r2))
        
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
            
            df_pred_scaled = feature_scaler.transform(df_pred)
            pred_scaled = model.predict(df_pred_scaled, verbose=0).flatten()
            pred_current = target_scaler.inverse_transform(pred_scaled.reshape(-1, 1)).flatten()
            
            area = np.trapz(np.abs(pred_current), [voltages[0]])
            C = area / (2 * mass * delta_V * v) if (2 * mass * delta_V * v) != 0 else 0
            capacitance_values.append(float(max(0, C)))  # Ensure non-negative
        
        best_idx = int(np.argmax(capacitance_values))
        
        return {
            'success': True,
            'model': 'ANN',
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
            'best_concentration': float(concentrations[best_idx]),
            'best_capacitance': capacitance_values[best_idx],
            'capacitance_profile': {
                'concentrations': concentrations.tolist(),
                'capacitance_values': capacitance_values
            },
            'training_history': {
                'epochs': len(history.history['loss']),
                'final_loss': float(history.history['loss'][-1]),
                'final_val_loss': float(history.history['val_loss'][-1])
            }
        }
    
    except Exception as e:
        import traceback
        print(f"ANN Error: {traceback.format_exc()}")
        return {
            'success': False,
            'model': 'ANN',
            'error': str(e)
        }
