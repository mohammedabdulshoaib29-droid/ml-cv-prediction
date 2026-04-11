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
        
        # Check if classification or regression
        if len(np.unique(y_true)) < len(y_true) / 5:  # Likely classification
            # Classification metrics
            metrics['accuracy'] = float(accuracy_score(y_true, y_pred))
            metrics['type'] = 'classification'
        else:
            # Regression metrics
            metrics['r2_score'] = float(r2_score(y_true, y_pred))
            metrics['accuracy'] = float(r2_score(y_true, y_pred))  # Using R² as accuracy
            metrics['type'] = 'regression'
        
        # Common metrics for both
        metrics['rmse'] = float(np.sqrt(mean_squared_error(y_true, y_pred)))
        metrics['mae'] = float(mean_absolute_error(y_true, y_pred))
        
        return metrics
    
    @staticmethod
    def get_predictions_with_confidence(y_pred: np.ndarray) -> list:
        """Convert predictions to list format"""
        return y_pred.tolist()
