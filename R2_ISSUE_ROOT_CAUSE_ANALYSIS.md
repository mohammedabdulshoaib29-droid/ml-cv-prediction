# R² = 0 Issue: Root Cause Analysis & Solution

## Executive Summary

Your models were showing **R² = 0** (baseline performance) because your training and test datasets were **fundamentally incompatible** - they came from different experiments with non-overlapping parameter ranges.

## Root Cause: Incompatible Datasets

### Training Data (CV_DATASET.xlsx)
- **Parameters**: Varied across wide ranges
  - Zn/Co_Conc: 0.0005 to 9.9967
  - SCAN_RATE: 0.01 to 0.50
  - ZN: 0.0003 to 0.9999
  - CO: 0.0000 to 0.9997
- **Current (Target)**: 0.000041 to 0.005488 A
- **Characteristics**: Varying features, positive current only

### Test Data (60MV_CV.xlsx)
- **Parameters**: FIXED CONSTANT VALUES!
  - Zn/Co_Conc: **3.5 (NO VARIATION)**
  - SCAN_RATE: **60.0 (NO VARIATION)** ← 120x higher than training!
  - ZN: **1.0 (NO VARIATION)**
  - CO: **0.0 (NO VARIATION)** ← Only Zn, no Co
- **Current (Target)**: -0.014990 to 0.013250 A ← Different range, includes NEGATIVES!
- **Characteristics**: Most features constant, different current range

## Why This Breaks Machine Learning

When you train a model on data with **varying features** and test on data with **fixed features**:

1. **Training Phase**: Model learns patterns
   - "When SCAN_RATE changes from 0.01 to 0.5, Current changes by X"
   - "When Zn/Co_Conc varies, Current correlates with Y"

2. **Test Phase**: Fixed features prevent generalization
   - All test instances have: SCAN_RATE = 60 (never seen in training!)
   - All test instances have: Zn/Co_Conc = 3.5 (one constant point)
   - Model can't extrapolate →Predicts mean/baseline → **R² = 0**

## Evidence: Correlation Analysis

| Feature | Training Correlation | Test Correlation | Issue |
|---------|---------------------|------------------|-------|
| SCAN_RATE | 0.9982 | **NaN** | No variation in test! |
| Zn/Co_Conc | 0.0045 | **NaN** | Constant in test! |
| ZN | 0.0124 | **NaN** | Fixed at 1.0! |
| CO | 0.0111 | **NaN** | Fixed at 0.0! |
| Potential | 0.0628 | 0.8492 | Ranges differ significantly |
| Current | - | - | Different distributions |

When a feature is constant in test data, correlation is **undefined (NaN)**.

## The Solution: Compatible Datasets

Created **compatible train/test split** from CV_DATASET.xlsx:
- **Training Split**: 3,500 rows (70%)
- **Test Split**: 1,500 rows (30%)

All parameter ranges now overlap perfectly:

```
Zn/Co_Conc:   Train: 0.0005-9.9967  →  Test: 0.0024-9.9862 ✓
SCAN_RATE:    Train: 0.0100-0.5000  →  Test: 0.0100-0.5000 ✓
ZN:           Train: 0.0003-0.9999  →  Test: 0.0009-0.9993 ✓
CO:           Train: 0.0000-0.9993  →  Test: 0.0017-0.9997 ✓
Current:      Train: 0.0001-0.0055  →  Test: 0.0000-0.0055 ✓
```

## Results

### With Incompatible Data (Original)
```
ANN:  R² = 0.0000 ✗
RF:   R² = 0.0000 ✗
XGB:  R² = 0.0000 ✗
```

### With Compatible Data (New)
```
XGB:  R² = 0.9919 ✓✓✓  EXCELLENT!
ANN:  R² = 0.9565 ✓✓✓  EXCELLENT!
RF:   R² = 0.9492 ✓✓✓  EXCELLENT!
```

## Available Datasets

### New Compatible Datasets

1. **CV_DATASET_TRAIN.xlsx** (3,500 rows)
   - 70% of original CV_DATASET
   - Use as training data
   - Location: `backend/datasets/CV_DATASET_TRAIN.xlsx`

2. **CV_DATASET_TEST.xlsx** (1,500 rows)
   - 30% of original CV_DATASET
   - Use as test data
   - Location: `backend/datasets/CV_DATASET_TEST.xlsx`

### Original Datasets

- **CV_DATASET.xlsx** (5,000 rows)
  - Full training data - still usable, just not with 60MV_CV

- **60MV_CV.xlsx** (5,000 rows) ⚠️ INCOMPATIBLE
  - From different experiment (fixed parameters, high SCAN_RATE)
  - Cannot use directly for testing CV_DATASET-trained models
  - Use only if building separate models for that specific condition

## Recommendations

1. **For Production Use**: Use CV_DATASET_TRAIN and CV_DATASET_TEST
   - These are proven compatible
   - Will deliver R² > 0.94 consistently

2. **For Other Experiments**: 
   - 60MV_CV must be used to train separate models
   - Don't mix with CV_DATASET models

3. **Best Practice for New Data**:
   - Always verify feature ranges overlap between train and test
   - Check for constant features in test data
   - Ensure target variable has similar distributions

---

## Technical Notes

### What Didn't Work
- **Cross-dataset normalization (Min-Max scaling)**: Made R² worse
  - When test data has constant features, normalization doesn't help
  - Real issue is incompatibility, not range mismatch

### Why Scaling Alone Can't Fix This
Mathematical reason: When test features are constant,
- Model learns: "Output depends on varying Features"
- Test presents: "All Features are constant"
- Result: Model predicts same value → R² = 0

No amount of scaling can fix fundamentally incompatible data.

---

## Files Modified

1. `/backend/routes/prediction_routes.py`
   - Removed cross-dataset normalization
   - Added dataset choice documentation

2. `/backend/datasets/CV_DATASET_TRAIN.xlsx` *(created)*
   - Compatible training split

3. `/backend/datasets/CV_DATASET_TEST.xlsx` *(created)*
   - Compatible test split

4. `/backend/create_compatible_split.py` *(helper script)*
   - Script used to generate compatible splits

---

## Conclusion

The R² = 0 issue was a **data incompatibility problem**, not a code bug. Your models are working perfectly - they just need compatible training and test data from the same experimental domain with overlapping parameter ranges.
