from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pathlib import Path
from utils.preprocessing import DataPreprocessor
from utils.evaluation import ModelEvaluator
from models.ml_models import MLModels
from models.comparison import run_all_models
import numpy as np
import pandas as pd
import tempfile
import json

router = APIRouter()

DATASETS_DIR = Path("datasets")

# CV Analysis required columns
CV_REQUIRED_COLUMNS = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO", "Current"]

def convert_numpy_to_python(obj):
    """Convert numpy types to Python native types for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_numpy_to_python(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_to_python(item) for item in obj]
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, (np.floating, np.integer)):
        return float(obj) if isinstance(obj, np.floating) else int(obj)
    elif isinstance(obj, np.bool_):
        return bool(obj)
    elif isinstance(obj, (float, int, str, bool, type(None))):
        return obj
    else:
        return str(obj)

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
        Predictions and accuracy metrics, including CV graphs if applicable
    """
    try:
        # Validate dataset exists
        train_path = DATASETS_DIR / dataset_name
        if not train_path.exists():
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_name} not found")
        
        # Load training and test data
        train_df = pd.read_csv(train_path) if str(train_path).endswith('.csv') else pd.read_excel(train_path)
        
        # Load test data from uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(test_file.filename).suffix) as tmp:
            content = await test_file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            test_df = pd.read_csv(tmp_path) if tmp_path.endswith('.csv') else pd.read_excel(tmp_path)
            
            # Check if this is CV analysis data (has required columns)
            cv_columns_present = all(col in train_df.columns for col in CV_REQUIRED_COLUMNS)
            
            if cv_columns_present and all(col in test_df.columns for col in CV_REQUIRED_COLUMNS):
                # Use CV analysis with comparison models
                cv_results = run_all_models(train_df, test_df)
                return {
                    "status": "success",
                    "training_dataset": dataset_name,
                    "test_samples": len(test_df),
                    "is_cv_analysis": True,
                    **cv_results  # Includes performance, best_model, graphs, table, recommendations, etc.
                }
            else:
                # Use general ML models
                preprocessor = DataPreprocessor()
                X_train, y_train = preprocessor.preprocess(
                    train_df,
                    fit=True
                )
                
                X_test, y_test = preprocessor.preprocess(test_df, fit=False)
                
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
                    "is_cv_analysis": False,
                    "models": {}
                }
                
                evaluator = ModelEvaluator()
                selected_models = ['ann', 'rf', 'xgb'] if model_type == 'all' else [model_type]
                
                # Process each selected model
                for model_name in selected_models:
                    if predictions_dict.get(model_name) is not None:
                        preds = predictions_dict[model_name]
                        
                        # Inverse transform predictions if needed
                        preds_original = preprocessor.inverse_transform_predictions(preds)
                        
                        results["models"][model_name] = {
                            "predictions": preds_original.tolist()[:10],  # First 10 for display
                            "all_predictions": preds_original.tolist(),
                            "training_status": train_results.get(model_name, 'unknown')
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
                
                # Convert numpy types to Python native types for JSON serialization
                results = convert_numpy_to_python(results)
                return results
        
        finally:
            # Clean up temp file
            Path(tmp_path).unlink(missing_ok=True)
    
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500, 
            detail=f"Error during prediction: {str(e)}"
        )

@router.get("/predict/status")
async def prediction_status():
    """Check if prediction service is ready"""
    return {"status": "ready"}
