"""
XGBoost model runner.
"""

import traceback

from xgboost import XGBRegressor

from models.pipeline_utils import empty_model_result, finalize_model_result, prepare_datasets


def run_xgb(train_df, test_df, predictors=None, target=None):
    model_name = 'XGBoost'

    try:
        prepared = prepare_datasets(
            train_df=train_df,
            test_df=test_df,
            predictors=predictors,
            target=target,
            scale_features=False
        )

        model = XGBRegressor(
            n_estimators=400,
            max_depth=6,
            learning_rate=0.05,
            subsample=0.9,
            colsample_bytree=0.9,
            objective='reg:squarederror',
            random_state=42
        )
        model.fit(prepared['x_train'], prepared['y_train'])
        predictions = model.predict(prepared['x_test'])

        result = finalize_model_result(model_name, prepared, predictions)
        if hasattr(model, 'feature_importances_'):
            result['feature_importance'] = {
                column: float(importance)
                for column, importance in zip(prepared['feature_columns'], model.feature_importances_)
            }
        return result

    except Exception as e:
        print(f'Error in XGBoost model: {traceback.format_exc()}')
        return empty_model_result(model_name, str(e))