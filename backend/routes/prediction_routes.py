from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pathlib import Path
from models.comparison import run_all_models
import pandas as pd
import tempfile

router = APIRouter()

DATASETS_DIR = Path("datasets")

# CV Analysis required columns
CV_REQUIRED_COLUMNS = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO", "Current"]

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
                # CV analysis is required - return error for non-CV data
                raise HTTPException(
                    status_code=400,
                    detail="Dataset must contain CV analysis columns: Potential, OXIDATION, Zn/Co_Conc, SCAN_RATE, ZN, CO, Current"
                )
        
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
