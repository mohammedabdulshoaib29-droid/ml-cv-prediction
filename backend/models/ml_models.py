import numpy as np
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.neural_network import MLPClassifier, MLPRegressor
import xgboost as xgb
from typing import Tuple

class MLModels:
    def __init__(self, task_type: str = 'classification'):
        """
        Initialize ML models
        
        Args:
            task_type: 'classification' or 'regression'
        """
        self.task_type = task_type
        self.models = {
            'ann': None,
            'rf': None,
            'xgb': None
        }
        self._build_models()
    
    def _build_models(self):
        """Build model instances based on task type"""
        if self.task_type == 'classification':
            self.models['ann'] = MLPClassifier(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42,
                early_stopping=True
            )
            self.models['rf'] = RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
            self.models['xgb'] = xgb.XGBClassifier(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
        else:  # regression
            self.models['ann'] = MLPRegressor(
                hidden_layer_sizes=(100, 50),
                max_iter=500,
                random_state=42,
                early_stopping=True
            )
            self.models['rf'] = RandomForestRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
            self.models['xgb'] = xgb.XGBRegressor(
                n_estimators=100,
                random_state=42,
                n_jobs=-1
            )
    
    def train(self, X_train: np.ndarray, y_train: np.ndarray) -> dict:
        """
        Train all models
        
        Args:
            X_train: Training features
            y_train: Training targets
        
        Returns:
            Dictionary with training status
        """
        results = {}
        
        try:
            # Train ANN
            self.models['ann'].fit(X_train, y_train)
            results['ann'] = 'trained'
        except Exception as e:
            results['ann'] = f'error: {str(e)}'
        
        try:
            # Train Random Forest
            self.models['rf'].fit(X_train, y_train)
            results['rf'] = 'trained'
        except Exception as e:
            results['rf'] = f'error: {str(e)}'
        
        try:
            # Train XGBoost
            self.models['xgb'].fit(X_train, y_train)
            results['xgb'] = 'trained'
        except Exception as e:
            results['xgb'] = f'error: {str(e)}'
        
        return results
    
    def predict(self, X_test: np.ndarray) -> dict:
        """
        Make predictions with all models
        
        Args:
            X_test: Test features
        
        Returns:
            Dictionary with predictions from all models
        """
        predictions = {}
        
        try:
            predictions['ann'] = self.models['ann'].predict(X_test)
        except Exception as e:
            predictions['ann'] = None
        
        try:
            predictions['rf'] = self.models['rf'].predict(X_test)
        except Exception as e:
            predictions['rf'] = None
        
        try:
            predictions['xgb'] = self.models['xgb'].predict(X_test)
        except Exception as e:
            predictions['xgb'] = None
        
        return predictions
    
    def get_feature_importance(self, feature_names: list = None) -> dict:
        """
        Get feature importance from RF and XGB
        
        Args:
            feature_names: List of feature names
        
        Returns:
            Dictionary with feature importance for each model
        """
        importance = {}
        
        # Random Forest importance
        if self.models['rf'] is not None:
            rf_importance = self.models['rf'].feature_importances_
            if feature_names:
                importance['rf'] = sorted(
                    zip(feature_names, rf_importance),
                    key=lambda x: x[1],
                    reverse=True
                )
            else:
                importance['rf'] = rf_importance.tolist()
        
        # XGBoost importance
        if self.models['xgb'] is not None:
            xgb_importance = self.models['xgb'].feature_importances_
            if feature_names:
                importance['xgb'] = sorted(
                    zip(feature_names, xgb_importance),
                    key=lambda x: x[1],
                    reverse=True
                )
            else:
                importance['xgb'] = xgb_importance.tolist()
        
        return importance
