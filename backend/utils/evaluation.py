import numpy as np
from sklearn.metrics import accuracy_score, mean_squared_error, r2_score, mean_absolute_error
from typing import Dict

class ModelEvaluator:
    @staticmethod
    def evaluate(y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Evaluate model predictions
        
        Args:
            y_true: True values
            y_pred: Predicted values
        
        Returns:
            Dictionary with evaluation metrics
        """
        metrics = {}
        
        # Ensure arrays are numpy arrays
        y_true = np.array(y_true)
        y_pred = np.array(y_pred)
        
        # Determine if classification or regression based on y_true
        unique_count = len(np.unique(y_true))
        total_count = len(y_true)
        is_classification = unique_count <= min(20, max(2, total_count / 5))
        
        if is_classification:
            try:
                # Classification metrics - round predictions to nearest class
                y_pred_rounded = np.round(y_pred).astype(int)
                y_true_int = np.array(y_true).astype(int)
                metrics['accuracy'] = float(accuracy_score(y_true_int, y_pred_rounded))
                metrics['type'] = 'classification'
            except Exception as e:
                # Fallback to regression metrics if classification fails
                metrics['accuracy'] = float(r2_score(y_true, y_pred))
                metrics['type'] = 'regression'
                metrics['rmse'] = float(np.sqrt(mean_squared_error(y_true, y_pred)))
                metrics['mae'] = float(mean_absolute_error(y_true, y_pred))
                return metrics
        else:
            # Regression metrics
            try:
                metrics['r2_score'] = float(r2_score(y_true, y_pred))
                metrics['accuracy'] = float(r2_score(y_true, y_pred))  # Using R² as accuracy
                metrics['type'] = 'regression'
            except Exception as e:
                metrics['accuracy'] = 0.0
                metrics['type'] = 'regression'
        
        # Common metrics for both - with error handling
        try:
            metrics['rmse'] = float(np.sqrt(mean_squared_error(y_true, y_pred)))
            metrics['mae'] = float(mean_absolute_error(y_true, y_pred))
        except Exception as e:
            metrics['rmse'] = 0.0
            metrics['mae'] = 0.0
        
        # Ensure all values are Python native types
        metrics = {k: float(v) if isinstance(v, (np.floating, np.integer)) else v 
                   for k, v in metrics.items()}
        
        return metrics
    
    @staticmethod
    def get_predictions_with_confidence(y_pred: np.ndarray) -> list:
        """Convert predictions to list format"""
        return y_pred.tolist()
