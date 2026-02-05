import pandas as pd
import numpy as np
from typing import Tuple

def generate_nhanes_data(n_samples: int = 5000) -> pd.DataFrame:
    """
    Generates a synthetic dataset mimicking NHANES (2017-2020) structure.
    Uses official variable codes.
    
    Variables:
    - RIDAGEYR (Age)
    - RIAGENDR (Gender: 1=Male, 2=Female)
    - BMXBMI (BMI)
    - BPXSY1 (Systolic BP)
    - LBXGH (HbA1c %)
    - LBXTC (Total Cholesterol)
    - PAQ650 (Vigorous Activity: 1=Yes, 2=No)
    - SLD010H (Sleep Hours)
    - SMQ020 (Smoked >100 cigs: 1=Yes, 2=No)
    """
    np.random.seed(42)
    
    # 1. Demographics
    age = np.random.randint(18, 80, n_samples)
    gender = np.random.choice([1, 2], n_samples) # 1=Male, 2=Female
    
    # 2. Body Measures (Correlated with Age)
    # Average BMI ~28, higher for older
    bmi_noise = np.random.normal(0, 5, n_samples)
    bmi = 24 + (age * 0.05) + bmi_noise
    bmi = np.clip(bmi, 15, 60)
    
    # 3. Lifestyle
    # Younger people more active (PAQ650: 1=Yes, 2=No)
    activity_prob = 1 - (age / 100)
    vigorous_activity = np.array([1 if p > np.random.rand() else 2 for p in activity_prob])
    
    sleep = np.random.normal(7, 1.5, n_samples)
    sleep = np.clip(sleep, 3, 12)
    
    smoker = np.random.choice([1, 2], n_samples, p=[0.4, 0.6])
    
    # 4. Biomarkers (Correlated with BMI, Age, Activity)
    
    # HbA1c (Diabetes indicator)
    # Base 5.0, +0.1 for every 5 BMI points over 25, +0.02 per year of age
    hba1c_noise = np.random.normal(0, 0.5, n_samples)
    hba1c = 5.0 + np.maximum(0, (bmi - 25) * 0.05) + (age * 0.01) + hba1c_noise
    
    # Systolic BP (Hypertension)
    # Base 110, +0.5 per BMI point over 25, +0.5 per year of age
    bp_noise = np.random.normal(0, 10, n_samples)
    bp_sys = 110 + np.maximum(0, (bmi - 25) * 0.6) + (age * 0.4) + bp_noise
    
    # Cholesterol
    chol_noise = np.random.normal(0, 30, n_samples)
    chol = 180 + (age * 0.2) + (bmi * 0.5) + chol_noise
    
    # 5. Create DataFrame
    df = pd.DataFrame({
        'RIDAGEYR': age,
        'RIAGENDR': gender,
        'BMXBMI': np.round(bmi, 1),
        'BPXSY1': np.round(bp_sys, 0),
        'LBXGH': np.round(hba1c, 1),
        'LBXTC': np.round(chol, 0),
        'PAQ650': vigorous_activity,
        'SLD010H': np.round(sleep, 1),
        'SMQ020': smoker
    })
    
    # 6. Define Targets (Ground Truth for Training)
    # Diabetes: HbA1c >= 6.5
    df['Target_Diabetes'] = (df['LBXGH'] >= 6.5).astype(int)
    
    # Hypertension: Systolic >= 130
    df['Target_Hypertension'] = (df['BPXSY1'] >= 130).astype(int)
    
    return df

if __name__ == "__main__":
    df = generate_nhanes_data(10000)
    df.to_csv('data/nhanes_mock.csv', index=False)
    print("NHANES Mock Data Generated: data/nhanes_mock.csv")
    print(df.head())
    print("\nPrevalence:")
    print(df[['Target_Diabetes', 'Target_Hypertension']].mean())
