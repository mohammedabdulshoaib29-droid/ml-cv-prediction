from fastapi import APIRouter, File, UploadFile, Form, HTTPException
from pathlib import Path
from models.comparison import run_all_models
from models.rf import run_rf
import pandas as pd
import tempfile
import sys
import traceback
import time
import asyncio
import psutil
import gc
from concurrent.futures import ThreadPoolExecutor

router = APIRouter()

# Adaptive worker count based on available memory
def get_optimal_workers():
    """Determine optimal worker count based on system memory"""
    try:
        available_memory = psutil.virtual_memory().available / (1024**3)  # GB
        if available_memory < 0.5:
            return 1
        elif available_memory < 1.0:
            return 2
        else:
            return 4
    except:
        return 2

# Thread pool for CPU-intensive model training (allows other requests to be handled)
optimal_workers = get_optimal_workers()
print("[PREDICTION] Using {} workers based on available memory".format(optimal_workers))
model_executor = ThreadPoolExecutor(max_workers=optimal_workers)

# Get datasets directory - works in both local and Render
BACKEND_DIR = Path(__file__).parent.parent
DATASETS_DIR = BACKEND_DIR / "datasets"

# Ensure datasets directory exists
DATASETS_DIR.mkdir(parents=True, exist_ok=True)

# CV Analysis dataset choices
CV_DATASET_CHOICES = {
    "CV_DATASET_TRAIN": "Training set (70% of CV_DATASET - 3500 rows)",
    "CV_DATASET_TEST": "Test set (30% of CV_DATASET - 1500 rows)",
    "CV_DATASET": "Full dataset (5000 rows - for custom splits)"
}

# CV Analysis required columns
CV_REQUIRED_COLUMNS = ["Potential", "OXIDATION", "Zn/Co_Conc", "SCAN_RATE", "ZN", "CO", "Current"]

def normalize_columns(df):
    """Normalize column names: strip whitespace, standardize format"""
    df.columns = [col.strip() for col in df.columns]
    return df

def get_column_mapping(available_cols, required_cols):
    """
    Try to match required columns with available columns.
    First tries exact match, then case-insensitive, then returns None.
    """
    available_set = set(available_cols)
    
    # First try exact match
    if all(col in available_set for col in required_cols):
        return {col: col for col in required_cols}
    
    # Try case-insensitive match
    available_lower = {col.lower(): col for col in available_cols}
    required_lower = {col.lower(): col for col in required_cols}
    
    if all(col_lower in available_lower for col_lower in required_lower):
        return {req: available_lower[req.lower()] for req in required_cols}
    
    return None

def sample_data_for_fast_training(train_df, test_df, max_train_samples=150):
    """
    Sample data to enable fast predictions while maintaining quality
    
    Strategy:
    - Limit training data to 150 rows (can handle in <1min)
    - Balance sampling if possible
    - Keep all test data for evaluation
    - Reduces training time from 3+ min to <1 minute
    """
    original_train_size = len(train_df)
    original_test_size = len(test_df)
    
    # If training data is small, use all of it
    if original_train_size <= max_train_samples:
        print("[PREDICTION] Training dataset size ({}) is already optimal".format(original_train_size))
        return train_df, test_df
    
    # Sample efficiently: use stratified sampling if possible, else random
    print("[PREDICTION] Sampling training data: {} rows → {} rows for fast training".format(
        original_train_size, max_train_samples))
    
    # Random sampling with seed for reproducibility
    sampled_train = train_df.sample(n=max_train_samples, random_state=42)
    print("[PREDICTION] Sampled {} training rows (was {}) - training time should be <1 minute".format(
        len(sampled_train), original_train_size))
    
    # Ensure minimum test set size (at least 20% of training or 10 samples, whichever is larger)
    min_test_size = max(20, int(len(sampled_train) * 0.2))
    if len(test_df) < min_test_size:
        print("[PREDICTION] WARNING: Test set ({}) smaller than recommended ({}). This may result in negative R².".format(
            len(test_df), min_test_size))
    
    return sampled_train, test_df
    
    # Random sampling with seed for reproducibility
    sampled_train = train_df.sample(n=max_train_samples, random_state=42)
    print("[PREDICTION] Sampled {} training rows (was {}) - training time should be <1 minute".format(
        len(sampled_train), original_train_size))
    
    # Ensure minimum test set size (at least 20% of training or 10 samples, whichever is larger)
    min_test_size = max(20, int(len(sampled_train) * 0.2))
    if len(test_df) < min_test_size:
        print("[PREDICTION] WARNING: Test set ({}) smaller than recommended ({}). This may result in negative R².".format(
            len(test_df), min_test_size))
    
    return sampled_train, test_df

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
        model_type: 'all', 'ann', 'rf', 'xgb', or 'rf-only' (fast mode)
    
    Returns:
        Predictions and accuracy metrics, including CV graphs if applicable
    """
    tmp_path = None
    try:
        print("\n" + "="*60)
        print("[PREDICTION] Starting prediction for dataset: {}".format(dataset_name))
        print("[PREDICTION] Model type: {}".format(model_type))
        start_time = time.time()
        
        # Validate dataset exists
        train_path = DATASETS_DIR / dataset_name
        if not train_path.exists():
            raise HTTPException(status_code=404, detail=f"Dataset {dataset_name} not found")
        
        print("[PREDICTION] Loading training dataset from: {}".format(train_path))
        # Load training data
        try:
            if str(train_path).endswith('.csv'):
                train_df = pd.read_csv(train_path)
            else:
                # For Excel files, try to read the first sheet
                try:
                    train_df = pd.read_excel(train_path, sheet_name=0)
                except Exception as e:
                    print("[PREDICTION] Error with sheet_name=0, listing available sheets: {}".format(e))
                    xl_file = pd.ExcelFile(train_path)
                    print("[PREDICTION] Available sheets: {}".format(xl_file.sheet_names))
                    train_df = pd.read_excel(train_path, sheet_name=xl_file.sheet_names[0])
            
            # Normalize column names
            train_df = normalize_columns(train_df)
            
            print("[PREDICTION] Loaded train data: {} rows, {} columns".format(len(train_df), len(train_df.columns)))
            print("[PREDICTION] Train columns: {}".format(list(train_df.columns)))
        except Exception as e:
            print("[PREDICTION] Error loading train data: {}".format(e))
            raise HTTPException(status_code=500, detail="Failed to load training dataset: {}".format(str(e)))
        
        # Load test data from uploaded file
        try:
            print("[PREDICTION] Reading uploaded test file: {}".format(test_file.filename))
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(test_file.filename).suffix) as tmp:
                content = await test_file.read()
                tmp.write(content)
                tmp_path = tmp.name
                print("[PREDICTION] Saved temp file to: {}".format(tmp_path))
            
            if tmp_path.endswith('.csv'):
                test_df = pd.read_csv(tmp_path)
            else:
                # For Excel files, try to read the first sheet
                try:
                    test_df = pd.read_excel(tmp_path, sheet_name=0)
                except Exception as e:
                    print("[PREDICTION] Error reading test Excel file: {}".format(e))
                    xl_file = pd.ExcelFile(tmp_path)
                    print("[PREDICTION] Available sheets: {}".format(xl_file.sheet_names))
                    test_df = pd.read_excel(tmp_path, sheet_name=xl_file.sheet_names[0])
            
            # Normalize column names
            test_df = normalize_columns(test_df)
            
            print("[PREDICTION] Loaded test data: {} rows".format(len(test_df)))
            print("[PREDICTION] Test columns after normalization: {}".format(list(test_df.columns)))
            
            # ============================================
            # SAMPLE DATA FOR FAST TRAINING (<1 minute)
            # ============================================
            train_df, test_df = sample_data_for_fast_training(train_df, test_df, max_train_samples=150)
            
            # Validate columns
            print("[PREDICTION] Validating columns...")
            train_cols = set(train_df.columns)
            test_cols = set(test_df.columns)
            required_cols = set(CV_REQUIRED_COLUMNS)
            
            print("[PREDICTION] Train columns: {}".format(train_cols))
            print("[PREDICTION] Test columns: {}".format(test_cols))
            print("[PREDICTION] Required columns: {}".format(required_cols))
            
            # Check for missing columns
            missing_train = required_cols - train_cols
            missing_test = required_cols - test_cols
            
            if missing_train or missing_test:
                # Try to find case-insensitive matches
                train_mapping = get_column_mapping(train_df.columns, CV_REQUIRED_COLUMNS)
                test_mapping = get_column_mapping(test_df.columns, CV_REQUIRED_COLUMNS)
                
                if train_mapping:
                    print("[PREDICTION] Found case-insensitive match for training data, remapping columns...")
                    train_df = train_df.rename(columns=train_mapping)
                    missing_train = required_cols - set(train_df.columns)
                
                if test_mapping:
                    print("[PREDICTION] Found case-insensitive match for test data, remapping columns...")
                    test_df = test_df.rename(columns=test_mapping)
                    missing_test = required_cols - set(test_df.columns)
            
            # Final validation after remapping attempt
            if missing_train or missing_test:
                error_msg = "Column validation failed after attempting remapping."
                if missing_train:
                    error_msg += " Training data missing: {}".format(missing_train)
                if missing_test:
                    error_msg += " Test data missing: {}".format(missing_test)
                error_msg += " Required columns: {}".format(required_cols)
                error_msg += " Available train: {}".format(train_cols)
                error_msg += " Available test: {}".format(test_cols)
                print("[PREDICTION] {}".format(error_msg))
                raise HTTPException(
                    status_code=400,
                    detail=error_msg
                )
            
            # Check if this is CV analysis data (has required columns)
            cv_columns_present = all(col in train_df.columns for col in CV_REQUIRED_COLUMNS)
            
            if cv_columns_present and all(col in test_df.columns for col in CV_REQUIRED_COLUMNS):
                print("[PREDICTION] CV columns validated, running models in background thread...")
                
                # Get event loop for async execution
                loop = asyncio.get_event_loop()
                
                # Handle quick mode - RF only (faster for Render free tier)
                if model_type.lower() == "rf-only":
                    print("[PREDICTION] Running in QUICK MODE - Random Forest only (non-blocking)...")
                    try:
                        # Run RF in thread pool so it doesn't block other requests
                        rf_result = await loop.run_in_executor(
                            model_executor,
                            run_rf,
                            train_df,
                            test_df
                        )
                        elapsed = time.time() - start_time
                        print("[PREDICTION] Models completed in {:.2f}s".format(elapsed))
                        return {
                            "status": "success",
                            "training_dataset": dataset_name,
                            "test_samples": len(test_df),
                            "is_cv_analysis": True,
                            "execution_time_seconds": elapsed,
                            "quick_mode": True,
                            "best_model": "Random Forest",
                            "performance": {
                                "random_forest": {
                                    "r2": rf_result.get('r2', 0),
                                    "rmse": rf_result.get('rmse', 0),
                                    "mae": rf_result.get('mae', 0)
                                }
                            },
                            **rf_result
                        }
                    except Exception as e:
                        print("[PREDICTION] RF-only mode error: {}".format(e))
                        raise HTTPException(status_code=500, detail="Quick mode failed: {}".format(str(e)))
                
                # Standard mode - run all models in background thread (non-blocking)
                print("[PREDICTION] Running all models in background thread (non-blocking)...")
                cv_results = await loop.run_in_executor(
                    model_executor,
                    run_all_models,
                    train_df,
                    test_df
                )
                elapsed = time.time() - start_time
                print("[PREDICTION] Models completed in {:.2f}s".format(elapsed))
                return {
                    "status": "success",
                    "training_dataset": dataset_name,
                    "test_samples": len(test_df),
                    "is_cv_analysis": True,
                    "execution_time_seconds": elapsed,
                    **cv_results  # Includes performance, best_model, graphs, table, recommendations, etc.
                }

        
        finally:
            # Clean up temp file
            if tmp_path and Path(tmp_path).exists():
                try:
                    Path(tmp_path).unlink(missing_ok=True)
                    print("[PREDICTION] Cleaned up temp file")
                except:
                    pass
    
    except HTTPException as he:
        print("[PREDICTION] HTTP Exception: {}".format(he.detail))
        raise he
    except Exception as e:
        print("[PREDICTION] Unexpected Error: {}".format(str(e)))
        print("[PREDICTION] Traceback:")
        traceback.print_exc()
        
        # Clean up temp file in error case
        if tmp_path and Path(tmp_path).exists():
            try:
                Path(tmp_path).unlink(missing_ok=True)
            except:
                pass
        
        raise HTTPException(
            status_code=500, 
            detail=f"Prediction error: {str(e)}"
        )

@router.get("/predict/status")
async def prediction_status():
    """Check if prediction service is ready"""
    return {"status": "ready"}

@router.get("/health")
async def health_check():
    """Health check endpoint with memory info"""
    try:
        memory_info = psutil.virtual_memory()
        return {
            "status": "healthy",
            "memory_percent": memory_info.percent,
            "memory_available_gb": round(memory_info.available / (1024**3), 2),
            "timestamp": time.time()
        }
    except Exception as e:
        return {
            "status": "warning",
            "message": "Health check error: {}".format(str(e)),
            "timestamp": time.time()
        }
