#!/usr/bin/env python3
"""Diagnose why CV_DATASET is producing bad R² scores"""

import sys
import os

if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'
    sys.stdout.reconfigure(encoding='utf-8')
    
import pandas as pd
import numpy as np
from pathlib import Path

def analyze_dataset(filepath, name):
    """Analyze dataset characteristics"""
    print("\n" + "="*60)
    print("ANALYZING: {}".format(name))
    print("="*60)
    
    df = pd.read_excel(filepath)
    
    print("\nBasic Stats:")
    print("  Shape: {}".format(df.shape))
    print("  Columns: {}".format(df.columns.tolist()))
    
    print("\nData Types:")
    print(df.dtypes)
    
    print("\nDescriptive Statistics:")
    print(df.describe())
    
    print("\nValue Ranges:")
    for col in df.columns:
        print("  {}: [{:.6f}, {:.6f}]".format(col, df[col].min(), df[col].max()))
    
    print("\nMissing Values:")
    print(df.isnull().sum())
    
    print("\nTarget Variable (Current) Distribution:")
    current = df["Current"]
    print("  Mean: {:.6f}".format(current.mean()))
    print("  Std: {:.6f}".format(current.std()))
    print("  Skewness: {:.6f}".format(current.skew()))
    print("  Kurtosis: {:.6f}".format(current.kurtosis()))
    
    # Calculate IQR for outlier detection
    Q1 = current.quantile(0.25)
    Q3 = current.quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    outliers = current[(current < lower) | (current > upper)]
    print("  IQR bounds: [{:.6f}, {:.6f}]".format(lower, upper))
    print("  Outliers: {} ({:.1f}%)".format(len(outliers), 100*len(outliers)/len(current)))

def main():
    # Find CV datasets
    datasets_dir = Path("backend/datasets")
    
    cv_files = sorted(datasets_dir.glob("CV_DATASET*.xlsx"))
    original_files = sorted(datasets_dir.glob("60MV_CV*.xlsx"))
    
    print("\nFoundCV_DATASET files: {}".format(len(cv_files)))
    for f in cv_files:
        analyze_dataset(f, f.name)
    
    print("\n\nFound 60MV_CV files: {}".format(len(original_files)))
    for f in original_files:
        analyze_dataset(f, f.name)
    
    print("\n\n" + "="*60)
    print("COMPARISON SUMMARY")
    print("="*60)
    
    if cv_files and original_files:
        cv = pd.read_excel(cv_files[0])
        original = pd.read_excel(original_files[0])
        
        print("\nCurrent (target) variable ranges:")
        print("  CV_DATASET: [{:.6f}, {:.6f}]".format(cv["Current"].min(), cv["Current"].max()))
        print("  60MV_CV: [{:.6f}, {:.6f}]".format(original["Current"].min(), original["Current"].max()))
        
        print("\nCurrent (target) variable distributions:")
        print("  CV_DATASET mean: {:.6f}, std: {:.6f}".format(cv["Current"].mean(), cv["Current"].std()))
        print("  60MV_CV mean: {:.6f}, std: {:.6f}".format(original["Current"].mean(), original["Current"].std()))

if __name__ == "__main__":
    main()
