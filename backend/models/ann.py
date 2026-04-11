import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

def run_ann(train_df, test_df):
    """
    Artificial Neural Network (ANN) Model
    Uses TensorFlow/Keras with multi-layer architecture
    """

    predictors = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO"]
    target = "Current"

    tf.random.set_seed(42)
    np.random.seed(42)

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
    # 2. SCALE FEATURES
    # -------------------------------
    scaler = StandardScaler()

    train_data_scaled = scaler.fit_transform(train_data)
    test_data_scaled = scaler.transform(test_data)

    train_target = np.array(train_target)
    test_target = np.array(test_target)

    # -------------------------------
    # 3. BUILD MODEL
    # -------------------------------
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(len(predictors),)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.2),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='mean_squared_error'
    )

    callback = tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True
    )

    # -------------------------------
    # 4. TRAIN MODEL
    # -------------------------------
    model.fit(
        train_data_scaled,
        train_target,
        validation_split=0.2,
        epochs=100,
        batch_size=32,
        callbacks=[callback],
        verbose=0
    )

    # -------------------------------
    # 5. PREDICTIONS
    # -------------------------------
    test_predictions = model.predict(test_data_scaled, verbose=0).flatten()

    # -------------------------------
    # 6. METRICS
    # -------------------------------
    r2 = float(r2_score(test_target, test_predictions))
    rmse = float(np.sqrt(mean_squared_error(test_target, test_predictions)))

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

        cv_input_scaled = scaler.transform(cv_input)
        predicted_current = model.predict(cv_input_scaled, verbose=0).flatten()

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
        "best_concentration": float(concentrations[best_index]),
        "capacitance": float(capacitance_results[best_index]),
        "graph": {
            "x": concentrations.tolist(),
            "y": [float(val) for val in capacitance_results]
        }
    }
