import pandas as pd
import numpy as np
from pathlib import Path

# Load the datasets
train_path = Path('datasets/CV_DATASET.xlsx')
test_path = Path('datasets/60MV_CV.xlsx')

df_train = pd.read_excel(train_path)
df_test = pd.read_excel(test_path)

print('=== TRAINING DATASET ===')
print(f'Shape: {df_train.shape}')
print(f'Columns: {df_train.columns.tolist()}')
print(f'\nFirst few rows:')
print(df_train.head())
print(f'\nData types:')
print(df_train.dtypes)
print(f'\nCurrent (target) stats:')
print(f'  Min: {df_train["Current"].min()}')
print(f'  Max: {df_train["Current"].max()}')
print(f'  Mean: {df_train["Current"].mean():.10f}')
print(f'  Std: {df_train["Current"].std():.10f}')
print(f'  Variance: {df_train["Current"].var():.10f}')
print(f'  Null values: {df_train["Current"].isnull().sum()}')

print('\n=== TEST DATASET ===')
print(f'Shape: {df_test.shape}')
print(f'Columns: {df_test.columns.tolist()}')
print(f'\nFirst few rows:')
print(df_test.head())
print(f'\nCurrent (target) stats:')
print(f'  Min: {df_test["Current"].min()}')
print(f'  Max: {df_test["Current"].max()}')
print(f'  Mean: {df_test["Current"].mean():.10f}')
print(f'  Std: {df_test["Current"].std():.10f}')
print(f'  Null values: {df_test["Current"].isnull().sum()}')

print('\n=== CHECKING FOR CONSTANT VALUES ===')
print(f'Training - All Current values same? {df_train["Current"].nunique() == 1}')
print(f'Testing - All Current values same? {df_test["Current"].nunique() == 1}')
print(f'Training - Unique Current values: {df_train["Current"].nunique()}')
print(f'Testing - Unique Current values: {df_test["Current"].nunique()}')
