import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from typing import Tuple

class DataPreprocessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = None
        self.target_column = None
        
    def load_data(self, file_path: str) -> pd.DataFrame:
        """Load data from Excel or CSV file"""
        try:
            if file_path.endswith('.xlsx') or file_path.endswith('.xls'):
                df = pd.read_excel(file_path)
            elif file_path.endswith('.csv'):
                df = pd.read_csv(file_path)
            else:
                raise ValueError("File must be Excel or CSV format")
            return df
        except Exception as e:
            raise ValueError(f"Error loading file: {str(e)}")
    
    def preprocess(self, df: pd.DataFrame, target_col: str = None, fit: bool = False) -> Tuple[np.ndarray, np.ndarray]:
        """
        Preprocess data: handle missing values, encode categorical, scale features
        
        Args:
            df: Input dataframe
            target_col: Name of target column (if None, last column is assumed)
            fit: Whether to fit the preprocessor (training data)
        
        Returns:
            X, y: Features and target arrays
        """
        df = df.copy()
        
        # Determine target column
        if target_col is None:
            target_col = df.columns[-1]
        
        if target_col not in df.columns:
            # Try to use last column as target
            target_col = df.columns[-1]
        
        self.target_column = target_col
        
        # Handle missing values
        df = self._handle_missing_values(df)
        
        # Separate features and target
        X = df.drop(columns=[target_col])
        y = df[target_col]
        
        # Store feature columns
        if fit:
            self.feature_columns = X.columns.tolist()
        
        # Encode categorical variables
        X = self._encode_categorical(X, fit=fit)
        y = self._encode_target(y, fit=fit)
        
        # Scale features
        if fit:
            X = self.scaler.fit_transform(X)
        else:
            X = self.scaler.transform(X)
        
        return X, y.values if isinstance(y, pd.Series) else y
    
    def _handle_missing_values(self, df: pd.DataFrame) -> pd.DataFrame:
        """Handle missing values using mean for numerical and mode for categorical"""
        for col in df.columns:
            if df[col].isnull().sum() > 0:
                if df[col].dtype in ['float64', 'int64']:
                    df[col].fillna(df[col].mean(), inplace=True)
                else:
                    df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown', inplace=True)
        return df
    
    def _encode_categorical(self, X: pd.DataFrame, fit: bool = False) -> np.ndarray:
        """Encode categorical variables"""
        X = X.copy()
        
        for col in X.columns:
            if X[col].dtype == 'object':
                if fit:
                    self.label_encoders[col] = LabelEncoder()
                    X[col] = self.label_encoders[col].fit_transform(X[col].astype(str))
                else:
                    if col in self.label_encoders:
                        X[col] = self.label_encoders[col].transform(X[col].astype(str))
        
        return X.values
    
    def _encode_target(self, y: pd.Series, fit: bool = False) -> pd.Series:
        """Encode target variable if categorical"""
        if y.dtype == 'object':
            if fit:
                self.label_encoders['target'] = LabelEncoder()
                return pd.Series(self.label_encoders['target'].fit_transform(y.astype(str)))
            else:
                if 'target' in self.label_encoders:
                    return pd.Series(self.label_encoders['target'].transform(y.astype(str)))
        return y
    
    def inverse_transform_predictions(self, y_pred: np.ndarray) -> np.ndarray:
        """Inverse transform predictions if target was encoded"""
        if 'target' in self.label_encoders:
            return self.label_encoders['target'].inverse_transform(y_pred.astype(int))
        return y_pred
