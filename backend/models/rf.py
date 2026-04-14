"""
Random Forest model runner.
"""

import traceback

from sklearn.ensemble import RandomForestRegressor

from models.pipeline_utils import empty_model_result, finalize_model_result, prepare_datasets


def run_rf(train_df, test_df, predictors=None, target=None):
    model_name = 'RandomForest'

    try:
        prepared = prepare_datasets(
            train_df=train_df,
            test_df=test_df,
            predictors=predictors,
            target='Capacitance',
            scale_features=False,
            split_mode='train_plus_inference' if test_df is not None else 'internal'
        )

        model = RandomForestRegressor(
            n_estimators=300,
            max_depth=None,
            min_samples_split=2,
            min_samples_leaf=1,
            random_state=42,
            n_jobs=-1
        )
        model.fit(prepared['x_train'], prepared['y_train'])
        predictions = model.predict(prepared['x_test'])
        inference_predictions = model.predict(prepared['x_inference']) if prepared.get('x_inference') is not None else None

        result = finalize_model_result(model_name, prepared, predictions, inference_predictions)
        result['feature_importance'] = {
            column: float(importance)
            for column, importance in zip(prepared['feature_columns'], model.feature_importances_)
        }
        return result

    except Exception as e:
        print(f'Error in RandomForest model: {traceback.format_exc()}')
        return empty_model_result(model_name, str(e))
