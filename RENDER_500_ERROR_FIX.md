# Render 500 Error - Complete Debugging Guide

## Issue Summary
When clicking "Run Prediction" on https://ml-cv-prediction.onrender.com/#predict, the backend returns HTTP 500 error.

## Root Causes Identified & Fixed

### 1. **Path Resolution Issue (PRIMARY CAUSE)**
**Problem**: Using relative paths `Path("datasets")` doesn't work in Render's containerized environment
```python
# WRONG - doesn't work on Render
DATASETS_DIR = Path("datasets")
```

**Fix**: Use absolute paths based on module location
```python
# CORRECT - works everywhere
BACKEND_DIR = Path(__file__).parent
DATASETS_DIR = BACKEND_DIR / "datasets"
DATASETS_DIR.mkdir(parents=True, exist_ok=True)
```

**Impact**: Files can't be found → 500 error

### 2. **Encoding Issue on Windows/Linux**
**Problem**: Unicode characters (✓, ✗, etc.) in logging cause encoding errors
```python
print(f"[ANN] ✓ Training complete")  # FAILS on some systems
```

**Fix**: Use plain ASCII characters only
```python
print("[ANN] Training complete")  # Works everywhere
```

**Impact**: Logging crashes → 500 error in error handler

### 3. **Timeout Configuration**
**Problem**: Render's default timeout was too short for model training
```
web: cd backend && python main.py  # No timeout settings
```

**Fix**: Use Uvicorn with proper timeout configuration
```
web: cd backend && python -m uvicorn main:app --host 0.0.0.0 --port $PORT \
  --timeout-keep-alive 75 --timeout-graceful-shutdown 30
```

**Impact**: Long predictions (>30s) timeout → 500 error

## Files Modified

### backend/main.py
- Changed: `os.makedirs("datasets", exist_ok=True)` 
- To: `DATASETS_DIR = BACKEND_DIR / "datasets"; DATASETS_DIR.mkdir(...)`

### backend/routes/dataset_routes.py
- Added absolute path resolution
- Creates directory if missing

### backend/routes/prediction_routes.py
- Fixed all paths to use absolute
- Removed all Unicode from logging
- Added detailed error messages

### backend/models/ann.py
- Removed Unicode characters from logs

### backend/models/comparison.py  
- Removed Unicode characters from logs
- Better error handling with fallback values

### Procfile
- Updated to use Uvicorn with timeouts

### render.yaml
- Updated startCommand with proper configuration

### backend/requirements.txt
- Pinned all package versions

## Deployment Checklist

- [x] Fixed relative path issues → absolute paths
- [x] Removed all Unicode characters
- [x] Updated server configuration to use Uvicorn
- [x] Added proper timeout settings
- [x] Added comprehensive error logging
- [x] Pinned package versions
- [x] Local testing verified

## How to Deploy to Render

1. **Commit changes to git**:
   ```bash
   git add .
   git commit -m "Fix Render 500 error: path resolution, encoding, timeout config"
   git push origin main
   ```

2. **Render will automatically**:
   - Detect changes
   - Run `build.sh` for dependencies and frontend build
   - Start app with new `startCommand`

3. **Verify deployment**:
   - Go to https://ml-cv-prediction.onrender.com
   - Check Render dashboard for logs
   - New logs should show detailed [PREDICTION] messages

## Testing the Fix

### Local Test
```bash
python test_simple.py
```

Should complete in ~20 seconds with no encoding errors.

### Render Test
1. Select "sample_cv_train.csv" as training dataset
2. Upload "sample_cv_test.csv" as test file
3. Click "Run Prediction"
4. Should complete in 30-40 seconds with results

## Monitoring Logs

Check Render logs for these patterns:

**Success**:
```
[PREDICTION] Starting prediction for dataset: sample_cv_train.csv
[MODELS] Running ANN model...
[MODELS] ANN complete - R2=-5.3062
[PREDICTION] Models completed in 17.73s
```

**Error** (will now be detailed):
```
[PREDICTION] Error loading train data: ...
```

## Performance Metrics

| Metric | Target | Actual |
|--------|--------|--------|
| Training time | < 30s | ~18s |
| Response timeout | 75s | Configured |
| Graceful shutdown | 30s | Configured |
| Memory usage | < 512MB | Optimized |

## Fallback Mechanism

If models fail during training:
- Returns error-safe defaults instead of crashing
- API returns 500 with detailed error message
- Logs show exactly where failure occurred

## API Response Examples

### Success
```json
{
  "status": "success",
  "training_dataset": "sample_cv_train.csv",
  "test_samples": 50,
  "is_cv_analysis": true,
  "execution_time_seconds": 18.5,
  "performance": {...}
}
```

### Error (with detailed message now)
```json
{
  "detail": "Error during prediction: Missing column 'Current' in dataset"
}
```

## Next Steps if Still Getting 500

1. **Check Render logs** for specific error message
2. **Verify dataset structure**:
   - Must have columns: Potential, OXIDATION, Zn/Co_Conc, SCAN_RATE, ZN, CO, Current
   - File must be CSV or XLSX

3. **Try uploading custom dataset**:
   - Create test file with exact columns
   - Try predicting with it

4. **Contact Render support** with:
   - Specific error from logs
   - Steps to reproduce
   - Test dataset file

## Prevention for Future

- Always use absolute paths with `Path(__file__).parent`
- Never use Unicode in logging for compatibility
- Test on multiple systems before deployment
- Use explicit timeout configurations
- Add comprehensive error logging
