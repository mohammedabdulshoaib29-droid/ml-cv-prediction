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
            target=target,
            scale_features=False
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

        result = finalize_model_result(model_name, prepared, predictions)
        result['feature_importance'] = {
            column: float(importance)
            for column, importance in zip(prepared['feature_columns'], model.feature_importances_)
        }
        return result

    except Exception as e:
        print(f'Error in RandomForest model: {traceback.format_exc()}')
        return empty_model_result(model_name, str(e))