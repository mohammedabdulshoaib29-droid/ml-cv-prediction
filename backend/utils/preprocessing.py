import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Optional


DEFAULT_TARGET_CANDIDATES = [
    'Current',
    'current',
    'Capacitance',
    'capacitance',
    'target',
    'Target'
]


class RegressionPreprocessor:
    def __init__(self):
        self.feature_scaler = StandardScaler()
        self.feature_columns: List[str] = []
        self.target_column: Optional[str] = None
        self.numeric_fill_values: Dict[str, float] = {}
        self.fitted = False

    def prepare_datasets(
        self,
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        predictors: Optional[List[str]] = None,
        target_col: Optional[str] = None,
        scale_features: bool = False
    ) -> Dict:
        train_df = train_df.copy()
        test_df = test_df.copy()

        if train_df.empty:
            raise ValueError('Training dataset is empty')
        if test_df.empty:
            raise ValueError('Testing dataset is empty')

        target_column = self._resolve_target_column(train_df, test_df, target_col)
        feature_columns = self._resolve_feature_columns(train_df, test_df, target_column, predictors)

        self.target_column = target_column
        self.feature_columns = feature_columns

        train_subset = train_df[feature_columns + [target_column]].copy()
        test_subset = test_df[feature_columns + [target_column]].copy()

        train_subset = self._coerce_numeric_columns(train_subset, feature_columns + [target_column])
        test_subset = self._coerce_numeric_columns(test_subset, feature_columns + [target_column])

        self.numeric_fill_values = {
            column: float(train_subset[column].median()) if not train_subset[column].dropna().empty else 0.0
            for column in feature_columns
        }

        for column in feature_columns:
            train_subset[column] = train_subset[column].fillna(self.numeric_fill_values[column])
            test_subset[column] = test_subset[column].fillna(self.numeric_fill_values[column])

        train_subset = train_subset.dropna(subset=[target_column]).reset_index(drop=True)
        test_subset = test_subset.dropna(subset=[target_column]).reset_index(drop=True)

        if train_subset.empty:
            raise ValueError('Training dataset has no usable rows after preprocessing')
        if test_subset.empty:
            raise ValueError('Testing dataset has no usable rows after preprocessing')

        X_train = train_subset[feature_columns].to_numpy(dtype=float)
        y_train = train_subset[target_column].to_numpy(dtype=float)
        X_test = test_subset[feature_columns].to_numpy(dtype=float)
        y_test = test_subset[target_column].to_numpy(dtype=float)

        if np.unique(y_train).shape[0] <= 1:
            raise ValueError('Target variable is constant in training data')

        if scale_features:
            X_train = self.feature_scaler.fit_transform(X_train)
            X_test = self.feature_scaler.transform(X_test)
            self.fitted = True

        return {
            'X_train': X_train,
            'y_train': y_train,
            'X_test': X_test,
            'y_test': y_test,
            'feature_columns': feature_columns,
            'target_column': target_column,
            'train_processed_df': train_subset,
            'test_processed_df': test_subset
        }

    def transform_features(self, df: pd.DataFrame, scale_features: bool = False) -> np.ndarray:
        if not self.feature_columns:
            raise ValueError('Preprocessor has not been initialized with feature columns')

        feature_df = df.copy()
        for column in self.feature_columns:
            if column not in feature_df.columns:
                feature_df[column] = self.numeric_fill_values.get(column, 0.0)

        feature_df = feature_df[self.feature_columns].copy()
        feature_df = self._coerce_numeric_columns(feature_df, self.feature_columns)

        for column in self.feature_columns:
            feature_df[column] = feature_df[column].fillna(self.numeric_fill_values.get(column, 0.0))

        X = feature_df.to_numpy(dtype=float)

        if scale_features:
            if not self.fitted:
                raise ValueError('Feature scaler has not been fitted')
            X = self.feature_scaler.transform(X)

        return X

    def _resolve_target_column(
        self,
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        target_col: Optional[str]
    ) -> str:
        if target_col and target_col in train_df.columns and target_col in test_df.columns:
            return target_col

        for candidate in DEFAULT_TARGET_CANDIDATES:
            if candidate in train_df.columns and candidate in test_df.columns:
                return candidate

        common_columns = [column for column in train_df.columns if column in test_df.columns]
        numeric_common_columns = [
            column for column in common_columns
            if pd.api.types.is_numeric_dtype(train_df[column]) or pd.api.types.is_numeric_dtype(test_df[column])
        ]

        if not numeric_common_columns:
            raise ValueError('No common numeric columns available to use as target')

        return numeric_common_columns[-1]

    def _resolve_feature_columns(
        self,
        train_df: pd.DataFrame,
        test_df: pd.DataFrame,
        target_column: str,
        predictors: Optional[List[str]]
    ) -> List[str]:
        if predictors:
            missing_columns = [
                column for column in predictors
                if column not in train_df.columns or column not in test_df.columns
            ]
            if missing_columns:
                raise ValueError(f'Missing predictor columns: {", ".join(missing_columns)}')

            numeric_predictors = []
            for column in predictors:
                train_numeric = pd.to_numeric(train_df[column], errors='coerce')
                test_numeric = pd.to_numeric(test_df[column], errors='coerce')
                if train_numeric.notna().any() and test_numeric.notna().any():
                    numeric_predictors.append(column)

            if not numeric_predictors:
                raise ValueError('Provided predictor columns are not usable numeric features')

            return numeric_predictors

        common_columns = [column for column in train_df.columns if column in test_df.columns and column != target_column]
        numeric_columns = []

        for column in common_columns:
            train_numeric = pd.to_numeric(train_df[column], errors='coerce')
            test_numeric = pd.to_numeric(test_df[column], errors='coerce')
            if train_numeric.notna().any() and test_numeric.notna().any():
                numeric_columns.append(column)

        if not numeric_columns:
            raise ValueError('No common numeric feature columns found between training and testing datasets')

        return numeric_columns

    @staticmethod
    def _coerce_numeric_columns(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
        coerced_df = df.copy()
        for column in columns:
            coerced_df[column] = pd.to_numeric(coerced_df[column], errors='coerce')
        return coerced_df