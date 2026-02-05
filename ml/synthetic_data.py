import pandas as pd
import numpy as np
import random
from typing import List, Dict

def generate_synthetic_data(n_samples: int = 1000) -> pd.DataFrame:
    """
    Generates synthetic data for Health Risk Assessment.
    Simulates clusters: 'Office Worker', 'Gamer/Student', 'Active Individual'.
    """
    data = []
    
    for _ in range(n_samples):
        profile_type = random.choice(['office', 'gamer', 'active', 'balanced'])
        
        # Base Features
        if profile_type == 'office':
            screen_time = np.random.normal(9, 1.5)
            posture_pain = np.random.choice([0, 1], p=[0.4, 0.6]) # High pain prob
            sleep = np.random.normal(6.5, 1.0)
            social_media = np.random.normal(1.5, 0.5)
            physical_activity = np.random.randint(0, 3)
            stress = np.random.randint(5, 9)
            occupation = "Office"
            
        elif profile_type == 'gamer':
            screen_time = np.random.normal(12, 2.0)
            posture_pain = np.random.choice([0, 1], p=[0.5, 0.5])
            sleep = np.random.normal(5.5, 1.5)
            social_media = np.random.normal(2.0, 1.0) # + gaming time implicit in screen
            physical_activity = np.random.randint(0, 2)
            stress = np.random.randint(3, 8)
            occupation = "Student"
            
        elif profile_type == 'active':
            screen_time = np.random.normal(4, 1.5)
            posture_pain = np.random.choice([0, 1], p=[0.8, 0.2]) # Low pain prob
            sleep = np.random.normal(7.5, 0.8)
            social_media = np.random.normal(1.0, 0.5)
            physical_activity = np.random.randint(4, 7)
            stress = np.random.randint(2, 6)
            occupation = "Athlete"
            
        else: # Balanced
            screen_time = np.random.normal(6, 1.5)
            posture_pain = np.random.choice([0, 1], p=[0.7, 0.3])
            sleep = np.random.normal(7.0, 1.0)
            social_media = np.random.normal(2.0, 0.5)
            physical_activity = np.random.randint(2, 5)
            stress = np.random.randint(3, 7)
            occupation = "General"

        # Clip values to realistic bounds
        screen_time = max(0, min(24, screen_time))
        sleep = max(0, min(24, sleep))
        
        # Define Targets (Rule-based generation for Ground Truth)
        # 0 = Low, 1 = High Risk
        risk_musculo = 1 if (screen_time > 8 or posture_pain == 1) else 0
        risk_sleep = 1 if (sleep < 6 or screen_time > 11) else 0
        risk_mental = 1 if (stress > 7 or (social_media > 3 and sleep < 6)) else 0
        
        data.append({
            "daily_screen_time_hours": round(screen_time, 1),
            "sleep_hours": round(sleep, 1),
            "social_media_hours": round(social_media, 1),
            "physical_activity_days": physical_activity,
            "stress_level": stress,
            "neck_pain_frequency": "often" if posture_pain else "never", # Simplified for model
            "occupation": occupation,
            # Targets
            "target_musculoskeletal_risk": risk_musculo,
            "target_sleep_risk": risk_sleep,
            "target_mental_risk": risk_mental
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    df = generate_synthetic_data(2000)
    output_path = "data/synthetic_health_risk_v1.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {len(df)} samples to {output_path}")
