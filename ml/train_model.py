import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report
import pickle
import os

def train_model():
    data_path = "data/synthetic_health_risk_v1.csv"
    if not os.path.exists(data_path):
        print("Data file not found. Run synthetic_data.py first.")
        return

    df = pd.read_csv(data_path)
    
    # Features & Targets
    X = df.drop(columns=['target_musculoskeletal_risk', 'target_sleep_risk', 'target_mental_risk'])
    y = df[['target_musculoskeletal_risk', 'target_sleep_risk', 'target_mental_risk']]
    
    # Preprocessing
    numeric_features = ['daily_screen_time_hours', 'sleep_hours', 'social_media_hours', 'physical_activity_days', 'stress_level']
    categorical_features = ['neck_pain_frequency', 'occupation']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Model Pipeline (Multi-Output Random Forest)
    clf = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42)))
    ])
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("Training Model...")
    clf.fit(X_train, y_train)
    
    # Evaluate
    print("Evaluating...")
    y_pred = clf.predict(X_test)
    print(classification_report(y_test, y_pred, target_names=['Musculoskeletal', 'Sleep', 'Mental']))
    
    # Save
    model_path = "ml/risk_model_v1.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(clf, f)
    print(f"Model saved to {model_path}")

if __name__ == "__main__":
    train_model()
