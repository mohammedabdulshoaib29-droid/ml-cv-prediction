# Sample Datasets

This directory contains example datasets for testing the ML Web Application.

## Generating Sample Datasets

Run the following Python script to generate sample datasets:

```python
import pandas as pd
import numpy as np

# Set random seed for reproducibility
np.random.seed(42)

# Generate BiFeO3 training dataset
n_train = 150
train_data = {
    'Feature1': np.random.uniform(1, 5, n_train),
    'Feature2': np.random.uniform(2, 6, n_train),
    'Feature3': np.random.uniform(3, 7, n_train),
    'Feature4': np.random.uniform(4, 8, n_train),
}
train_data['Target'] = (
    train_data['Feature1'] * 2 + 
    train_data['Feature2'] * 1.5 - 
    train_data['Feature3'] * 0.5 + 
    np.random.normal(0, 0.5, n_train)
)

df_train = pd.DataFrame(train_data)
df_train.to_csv('BiFeO3_dataset.csv', index=False)
df_train.to_excel('BiFeO3_dataset.xlsx', index=False)

# Generate BiFeO3 test dataset
n_test = 50
test_data = {
    'Feature1': np.random.uniform(1, 5, n_test),
    'Feature2': np.random.uniform(2, 6, n_test),
    'Feature3': np.random.uniform(3, 7, n_test),
    'Feature4': np.random.uniform(4, 8, n_test),
}
test_data['Target'] = (
    test_data['Feature1'] * 2 + 
    test_data['Feature2'] * 1.5 - 
    test_data['Feature3'] * 0.5 + 
    np.random.normal(0, 0.5, n_test)
)

df_test = pd.DataFrame(test_data)
df_test.to_csv('BiFeO3_test.csv', index=False)
df_test.to_excel('BiFeO3_test.xlsx', index=False)

print("Dataset created successfully!")
```

## Sample Datasets Structure

All datasets follow this structure:

| Feature1 | Feature2 | Feature3 | Feature4 | Target |
|----------|----------|----------|----------|--------|
| 1.23     | 3.45     | 5.67     | 7.89     | 10.45  |
| 2.11     | 3.92     | 5.23     | 7.14     | 11.23  |
| 3.54     | 4.21     | 6.11     | 8.32     | 12.10  |

## Uploading Datasets

1. Open the application in browser
2. Navigate to "Upload New Training Dataset" section
3. Select a CSV or Excel file (example datasets above)
4. Click "Upload Dataset"
5. The dataset will appear in the "Select Training Dataset" dropdown

## File Formats Supported

- `.csv` - Comma-separated values
- `.xlsx` - Microsoft Excel 2007+
- `.xls` - Microsoft Excel 97-2003

## Dataset Requirements

- Minimum rows: 20 (recommended: 50+)
- All columns should be numerical except target (can be categorical or numerical)
- No completely empty columns
- Column headers required in first row
- Target variable should be clearly distinct

## Example Python Script to Create Custom Dataset

```python
import pandas as pd
import numpy as np

# Create synthetic data
data = {
    'Temperature': np.random.uniform(20, 100, 100),
    'Pressure': np.random.uniform(1, 10, 100),
    'pH': np.random.uniform(1, 14, 100),
    'Concentration': np.random.uniform(0.1, 1, 100),
}

# Create target based on features
data['Yield'] = (
    data['Temperature'] * 0.5 + 
    data['Pressure'] * 0.3 - 
    data['pH'] * 0.1 + 
    np.random.normal(0, 2, 100)
)

df = pd.DataFrame(data)
df.to_csv('MyDataset.csv', index=False)
print("Custom dataset created!")
```
