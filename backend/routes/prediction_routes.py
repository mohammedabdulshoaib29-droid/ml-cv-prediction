from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pathlib import Path
from utils.preprocessing import DataPreprocessor
from utils.evaluation import ModelEvaluator
from models.ml_models import MLModels
import numpy as np
import tempfile

router = APIRouter()

DATASETS_DIR = Path("datasets")

@router.post("/predict")
async def predict(
    dataset_name: str = Form(...),
    test_file: UploadFile = File(...),
    model_type: str = Form(default="all")
):
    """
    Train models and make predictions
    
    Args:
        dataset_name: Name of training dataset
        test_file: Uploaded test dataset
        model_type: 'all', 'ann', 'rf', or 'xgb'
    
    Returns:
        Predictions and accuracy metrics
    """
    try:
        # Validate dataset exists
        train_path = DATASETS_DIR / dataset_name
        if not train_path.exists():
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_name} not found")
        
        # Load and preprocess training data
        preprocessor = DataPreprocessor()
        X_train, y_train = preprocessor.preprocess(
            preprocessor.load_data(str(train_path)),
            fit=True
        )
        
        # Load and preprocess test data
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(test_file.filename).suffix) as tmp:
            content = await test_file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            test_df = preprocessor.load_data(tmp_path)
            
            # Handle case where test data might not have target column
            if preprocessor.target_column in test_df.columns:
                X_test, y_test = preprocessor.preprocess(test_df, fit=False)
            else:
                # If no target column, use all columns as features
                X_test = preprocessor._encode_categorical(test_df, fit=False)
                X_test = preprocessor.scaler.transform(X_test)
                y_test = None
            
            # Determine task type based on y_train
            if len(np.unique(y_train)) < len(y_train) / 5:
                task_type = 'classification'
            else:
                task_type = 'regression'
            
            # Initialize and train models
            models = MLModels(task_type=task_type)
            train_results = models.train(X_train, y_train)
            
            # Make predictions
            predictions_dict = models.predict(X_test)
            
            # Evaluate models
            results = {
                "task_type": task_type,
                "training_dataset": dataset_name,
                "test_samples": len(X_test),
                "models": {}
            }
            
            evaluator = ModelEvaluator()
            selected_models = ['ann', 'rf', 'xgb'] if model_type == 'all' else [model_type]
            
            for model_name in selected_models:
                if predictions_dict[model_name] is not None:
                    preds = predictions_dict[model_name]
                    
                    # Inverse transform predictions if needed
                    preds_original = preprocessor.inverse_transform_predictions(preds)
                    
                    results["models"][model_name] = {
                        "predictions": preds_original.tolist()[:10],  # First 10 for display
                        "all_predictions": preds_original.tolist(),
                        "training_status": train_results[model_name]
                    }
                    
                    # Add metrics if test labels available
                    if y_test is not None:
                        metrics = evaluator.evaluate(y_test, preds)
                        results["models"][model_name].update(metrics)
            
            # Get feature importance
            feature_names = preprocessor.feature_columns
            importance = models.get_feature_importance(feature_names)
            if importance:
                results["feature_importance"] = importance
            
            return results
        
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)
    
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Error during prediction: {str(e)}"
        )

@router.get("/predict/status")
async def prediction_status():
    """Check if prediction service is ready"""
    return {"status": "ready"}
