"""
Script to generate sample datasets for testing the ML Web Application
Run this script to create example datasets in the datasets folder
"""

import pandas as pd
import numpy as np
import os

# Create datasets directory if it doesn't exist
os.makedirs('.', exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

def create_dataset(name, n_samples, features_count=4):
    """Create a synthetic dataset"""
    data = {}
    
    # Generate features
    for i in range(features_count):
        data[f'Feature{i+1}'] = np.random.uniform(1, 10, n_samples)
    
    # Generate target based on features (regression example)
    feature_values = [data[f'Feature{i+1}'] for i in range(features_count)]
    target = sum(feature_values[i] * (i+1) * 0.1 for i in range(features_count))
    target += np.random.normal(0, 1, n_samples)  # Add noise
    
    data['Target'] = target
    
    df = pd.DataFrame(data)
    
    # Save as CSV and Excel
    csv_path = f'{name}.csv'
    excel_path = f'{name}.xlsx'
    
    df.to_csv(csv_path, index=False)
    df.to_excel(excel_path, index=False)
    
    print(f'✓ Created {csv_path} and {excel_path} ({n_samples} samples)')
    return df

# Generate training datasets
print("📊 Generating sample datasets...\n")

create_dataset('BiFeO3_dataset', n_samples=150)
create_dataset('MnO2_dataset', n_samples=120)
create_dataset('Graphene_dataset', n_samples=100)

print("\n✅ All datasets created successfully!")
print("📁 Files saved to: datasets/")
print("\nUsage:")
print("1. Start the backend server")
print("2. Open the application")
print("3. Upload datasets using the UI")
print("4. Select from dropdown and run predictions")
