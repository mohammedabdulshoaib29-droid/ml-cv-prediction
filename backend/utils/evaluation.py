import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from typing import Dict, List


def _to_float_list(values: np.ndarray) -> List[float]:
    return [float(value) for value in np.asarray(values).flatten().tolist()]


class ModelEvaluator:
    @staticmethod
    def evaluate_regression(y_true: np.ndarray, y_pred: np.ndarray, train_samples: int, test_samples: int) -> Dict:
        y_true = np.asarray(y_true, dtype=float).flatten()
        y_pred = np.asarray(y_pred, dtype=float).flatten()

        rmse = float(np.sqrt(mean_squared_error(y_true, y_pred)))
        mae = float(mean_absolute_error(y_true, y_pred))

        if len(y_true) > 1 and np.unique(y_true).shape[0] > 1:
            r2 = float(r2_score(y_true, y_pred))
        else:
            r2 = 0.0

        metrics = {
            'r2_score': r2,
            'rmse': rmse,
            'mae': mae,
            'predicted_capacitance_mean': float(np.mean(y_pred)) if len(y_pred) else 0.0,
            'predicted_capacitance_min': float(np.min(y_pred)) if len(y_pred) else 0.0,
            'predicted_capacitance_max': float(np.max(y_pred)) if len(y_pred) else 0.0,
            'train_samples': int(train_samples),
            'test_samples': int(test_samples)
        }

        return metrics

    @staticmethod
    def build_plot_data(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        y_true = np.asarray(y_true, dtype=float).flatten()
        y_pred = np.asarray(y_pred, dtype=float).flatten()
        errors = y_true - y_pred

        actual_vs_predicted = [
            {
                'actual': float(actual),
                'predicted': float(predicted)
            }
            for actual, predicted in zip(y_true.tolist(), y_pred.tolist())
        ]

        error_distribution = [
            {
                'error': float(error)
            }
            for error in errors.tolist()
        ]

        capacitance_series = [
            {
                'index': int(index),
                'predicted': float(predicted)
            }
            for index, predicted in enumerate(y_pred.tolist(), start=1)
        ]

        return {
            'actual_vs_predicted': actual_vs_predicted,
            'error_distribution': error_distribution,
            'capacitance_series': capacitance_series
        }

    @staticmethod
    def build_prediction_payload(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        return {
            'actual': _to_float_list(y_true),
            'predicted': _to_float_list(y_pred)
        }