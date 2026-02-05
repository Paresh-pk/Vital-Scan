import pandas as pd
import numpy as np
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
import pickle
import os

def train_disease_models():
    # Load Data
    if not os.path.exists("data/nhanes_mock.csv"):
        print("Data not found. Run nhanes_data.py first.")
        return

    df = pd.read_csv("data/nhanes_mock.csv")
    
    # Features (Clinical Inputs)
    feature_cols = ['RIDAGEYR', 'RIAGENDR', 'BMXBMI', 'BPXSY1', 'LBXGH', 'LBXTC', 'PAQ650', 'SLD010H', 'SMQ020']
    
    X = df[feature_cols]
    
    # Preprocessing (Scaling is good practice even for Trees)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Save Scaler
    with open("ml/models/scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)
        
    # --- Model 1: Type 2 Diabetes ---
    print("\n--- Training Type 2 Diabetes Model ---")
    y_diab = df['Target_Diabetes']
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_diab, test_size=0.2, random_state=42)
    
    model_diab = XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=100)
    model_diab.fit(X_train, y_train)
    
    preds_diab = model_diab.predict(X_test)
    probs_diab = model_diab.predict_proba(X_test)[:, 1]
    
    print(classification_report(y_test, preds_diab))
    print(f"AUC: {roc_auc_score(y_test, probs_diab):.4f}")
    
    with open("ml/models/diabetes_model.pkl", "wb") as f:
        pickle.dump(model_diab, f)

    # --- Model 2: Hypertension ---
    print("\n--- Training Hypertension Model ---")
    y_hyper = df['Target_Hypertension']
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_hyper, test_size=0.2, random_state=42)
    
    model_hyper = XGBClassifier(use_label_encoder=False, eval_metric='logloss', n_estimators=100)
    model_hyper.fit(X_train, y_train)
    
    preds_hyper = model_hyper.predict(X_test)
    probs_hyper = model_hyper.predict_proba(X_test)[:, 1]
    
    print(classification_report(y_test, preds_hyper))
    print(f"AUC: {roc_auc_score(y_test, probs_hyper):.4f}")
    
    with open("ml/models/hypertension_model.pkl", "wb") as f:
        pickle.dump(model_hyper, f)
        
    print("\nTraining Complete. Models saved to ml/models/")

if __name__ == "__main__":
    train_disease_models()
