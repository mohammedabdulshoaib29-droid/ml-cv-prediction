"""
CV-specific prediction routes using specialized models
For electrochemical CV behavior prediction on supercapacitor materials
"""

from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pathlib import Path
from models.comparison import run_all_models
import pandas as pd
import tempfile

router = APIRouter()

DATASETS_DIR = Path("datasets")

# Required columns for CV analysis
REQUIRED_COLUMNS = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO", "Current"]

@router.post("/cv-predict")
async def cv_predict(
    dataset_name: str = Form(...),
    test_file: UploadFile = File(...)
):
    """
    Run CV (Cyclic Voltammetry) analysis using all three models
    
    Args:
        dataset_name: Name of training dataset
        test_file: Uploaded test dataset CSV/Excel
    
    Returns:
        Model comparison with best model, recommendations, and CV metrics
    """
    try:
        # Validate dataset exists
        train_path = DATASETS_DIR / dataset_name
        if not train_path.exists():
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_name} not found")
        
        # Load training data
        train_df = pd.read_csv(train_path) if str(train_path).endswith('.csv') else pd.read_excel(train_path)
        
        # Validate training data has required columns
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in train_df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Training dataset missing columns: {', '.join(missing_cols)}"
            )
        
        # Load test data from uploaded file
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(test_file.filename).suffix) as tmp:
            content = await test_file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            test_df = pd.read_csv(tmp_path) if tmp_path.endswith('.csv') else pd.read_excel(tmp_path)
            
            # Validate test data has required columns
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in test_df.columns]
            if missing_cols:
                raise HTTPException(
                    status_code=400,
                    detail=f"Test dataset missing columns: {', '.join(missing_cols)}"
                )
            
            # Run all models and get comparison
            results = run_all_models(train_df, test_df)
            
            return {
                "status": "success",
                "training_dataset": dataset_name,
                "test_samples": len(test_df),
                **results  # Includes performance, best_model, recommendations, table, graph
            }
        
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
            detail=f"Error during CV prediction: {str(e)}"
        )


@router.post("/cv-predict/single-model")
async def cv_predict_single_model(
    dataset_name: str = Form(...),
    test_file: UploadFile = File(...),
    model: str = Form(default="xgb", regex="^(ann|rf|xgb)$")
):
    """
    Run CV analysis using a single specific model
    
    Args:
        dataset_name: Name of training dataset
        test_file: Uploaded test dataset
        model: 'ann' (Artificial Neural Network), 'rf' (Random Forest), or 'xgb' (XGBoost)
    
    Returns:
        Single model results with CV metrics
    """
    try:
        # Import specific model functions
        from models.ann import run_ann
        from models.rf import run_rf
        from models.xgb import run_xgb
        
        model_functions = {
            'ann': run_ann,
            'rf': run_rf,
            'xgb': run_xgb
        }
        
        # Validate dataset exists
        train_path = DATASETS_DIR / dataset_name
        if not train_path.exists():
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_name} not found")
        
        # Load training data
        train_df = pd.read_csv(train_path) if str(train_path).endswith('.csv') else pd.read_excel(train_path)
        
        # Validate training data
        missing_cols = [col for col in REQUIRED_COLUMNS if col not in train_df.columns]
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Training dataset missing columns: {', '.join(missing_cols)}"
            )
        
        # Load test data
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(test_file.filename).suffix) as tmp:
            content = await test_file.read()
            tmp.write(content)
            tmp_path = tmp.name
        
        try:
            test_df = pd.read_csv(tmp_path) if tmp_path.endswith('.csv') else pd.read_excel(tmp_path)
            
            # Validate test data
            missing_cols = [col for col in REQUIRED_COLUMNS if col not in test_df.columns]
            if missing_cols:
                raise HTTPException(
                    status_code=400,
                    detail=f"Test dataset missing columns: {', '.join(missing_cols)}"
                )
            
            # Run requested model
            model_func = model_functions.get(model)
            if not model_func:
                raise HTTPException(status_code=400, detail=f"Invalid model: {model}")
            
            results = model_func(train_df, test_df)
            
            model_names = {'ann': 'Artificial Neural Network (ANN)', 'rf': 'Random Forest (RF)', 'xgb': 'XGBoost (XGB)'}
            
            return {
                "status": "success",
                "model": model_names[model],
                "training_dataset": dataset_name,
                "test_samples": len(test_df),
                **results  # Includes r2, rmse, best_concentration, capacitance, graph
            }
        
        finally:
            Path(tmp_path).unlink(missing_ok=True)
    
    except HTTPException as he:
        raise he
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail=f"Error during CV prediction: {str(e)}"
        )
