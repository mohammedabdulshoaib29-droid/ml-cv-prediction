"""
Artificial Neural Network model runner.
"""

import traceback

from sklearn.neural_network import MLPRegressor

from models.pipeline_utils import empty_model_result, finalize_model_result, prepare_datasets


def run_ann(train_df, test_df, predictors=None, target=None):
    model_name = 'ANN'

    try:
        prepared = prepare_datasets(
            train_df=train_df,
            test_df=test_df,
            predictors=predictors,
            target='Capacitance',
            scale_features=True,
            split_mode='train_plus_inference' if test_df is not None else 'internal'
        )

        model = MLPRegressor(
            hidden_layer_sizes=(64, 32),
            activation='relu',
            solver='adam',
            learning_rate_init=0.001,
            max_iter=600,
            random_state=42,
            early_stopping=True,
            validation_fraction=0.15
        )
        model.fit(prepared['x_train'], prepared['y_train'])
        predictions = model.predict(prepared['x_test'])
        inference_predictions = model.predict(prepared['x_inference']) if prepared.get('x_inference') is not None else None

        return finalize_model_result(model_name, prepared, predictions, inference_predictions)

    except Exception as e:
        print(f'Error in ANN model: {traceback.format_exc()}')
        return empty_model_result(model_name, str(e))
