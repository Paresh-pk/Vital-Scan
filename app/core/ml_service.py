import pickle
import numpy as np
import pandas as pd
import os
from typing import List
from app.models.schemas import ClinicalInput, DiseaseRisk, RiskLevel
from app.core.llm_service import LLMService

class MLRiskEngine:
    def __init__(self, model_dir: str = "ml/models"):
        self.model_dir = model_dir
        self.scaler = self._load_model("scaler.pkl")
        self.diabetes_model = self._load_model("diabetes_model.pkl")
        self.hyper_model = self._load_model("hypertension_model.pkl")
        self.llm_service = LLMService() # Initialize with defaults (Template Mode)
        
    def _load_model(self, filename: str):
        path = os.path.join(self.model_dir, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Model {filename} not found. Train models first.")
        with open(path, "rb") as f:
            return pickle.load(f)

    def assess(self, input_data: ClinicalInput) -> List[DiseaseRisk]:
        # 1. Prepare Feature Vector (Order matters! Must match training)
        # Features: ['RIDAGEYR', 'RIAGENDR', 'BMXBMI', 'BPXSY1', 'LBXGH', 'LBXTC', 'PAQ650', 'SLD010H', 'SMQ020']
        
        # Mapping input to NHANES codes
        features = np.array([[
            input_data.age,
            input_data.gender.value,
            input_data.bmi,
            input_data.systolic_bp,
            input_data.hba1c,
            input_data.cholesterol,
            1 if input_data.vigorous_activity else 2, # Yes=1, No=2
            input_data.sleep_hours,
            1 if input_data.smoker_history else 2
        ]])
        
        # 2. Scale
        features_scaled = self.scaler.transform(features)
        
        results = []
        
        # 3. Predict Diabetes
        diab_prob = self.diabetes_model.predict_proba(features_scaled)[0][1]
        results.append(self._build_risk("Type 2 Diabetes", diab_prob, input_data, "hba1c", 6.0))

        # 4. Predict Hypertension
        hyper_prob = self.hyper_model.predict_proba(features_scaled)[0][1]
        results.append(self._build_risk("Hypertension", hyper_prob, input_data, "systolic_bp", 130))
        
        # 5. Calculate 20-Question Screening Score
        screening_risks = self._calculate_screening_score(input_data)
        results.extend(screening_risks)

        # 6. Layer 2: Narrative Enrichment (LLM/Template)
        results = self.llm_service.generate_explanation(results, user_profile=input_data.dict())
        
        # 7. Sort by Probability (Descending) - High Risk First
        results.sort(key=lambda x: x.probability, reverse=True)
        
        return results

    def _calculate_screening_score(self, data: ClinicalInput) -> List[DiseaseRisk]:
        """
        Splits the 20-Question Input into specific Risk Domains.
        Returns a list of DiseaseRisk objects for every domain with elevated risk.
        """
        all_new_risks = []
        
        # --- 1. Digital Eye Strain ---
        # Q4 (Dry Eyes), Q5 (Headaches)
        eye_score = sum([data.q4_dry_eyes, data.q5_headaches])
        if eye_score > 0:
            all_new_risks.append(DiseaseRisk(
                disease="Digital Eye Strain",
                risk_level=RiskLevel.MODERATE if eye_score == 1 else RiskLevel.HIGH,
                probability=0.65 if eye_score == 1 else 0.85,
                contributing_factors=["Frequent Headaches", "Dry/Tired Eyes"],
                prevention_steps=["Follow 20-20-20 Rule.", "Blink more often."]
            ))
        else:
             all_new_risks.append(DiseaseRisk(
                disease="Digital Eye Strain",
                risk_level=RiskLevel.LOW,
                probability=0.10,
                contributing_factors=["No major symptoms reported"],
                prevention_steps=["Maintain good screen habits."]
            ))

        # --- 2. Musculoskeletal (Back/Neck) ---
        # Q6 (Neck), Q7 (Back)
        msd_score = sum([data.q6_neck_pain, data.q7_back_pain])
        if msd_score > 0:
            all_new_risks.append(DiseaseRisk(
                disease="Musculoskeletal Disorder Risk",
                risk_level=RiskLevel.HIGH if msd_score == 2 else RiskLevel.MODERATE,
                probability=0.75,
                contributing_factors=["Neck Stiffness", "Lower Back Pain"],
                prevention_steps=["Ergonomic Audit", "Daily Stretching"]
            ))
        else:
            all_new_risks.append(DiseaseRisk(
                disease="Musculoskeletal Disorder Risk",
                risk_level=RiskLevel.LOW,
                probability=0.10,
                contributing_factors=["Good posture indicators"],
                prevention_steps=["Keep active to prevent future issues."]
            ))

        # --- 3. Sleep Disorders ---
        # Q10 (<7h), Q11 (Insomnia), Q16 (Phone Bedtime)
        sleep_score = 0
        factors = []
        if data.sleep_hours < 7: sleep_score += 1; factors.append("Low Sleep Duration")
        if data.q11_insomnia: sleep_score += 2; factors.append("Insomnia Symptoms")
        if data.q16_phone_bedtime: sleep_score += 1; factors.append("Blue Light Exposure")
        
        if sleep_score >= 2:
            all_new_risks.append(DiseaseRisk(
                disease="Sleep Deprivation/Disorder",
                risk_level=RiskLevel.HIGH if sleep_score >= 3 else RiskLevel.MODERATE,
                probability=0.80,
                contributing_factors=factors,
                prevention_steps=["Digital Sunset (No phones 1h before bed)", "Consistent Wake Time"]
            ))
        else:
             all_new_risks.append(DiseaseRisk(
                disease="Sleep Deprivation/Disorder",
                risk_level=RiskLevel.LOW,
                probability=0.15,
                contributing_factors=["Good sleep hygiene"],
                prevention_steps=["Maintain 7-8h sleep schedule."]
            ))

        # --- 4. Mental Wellbeing (Stress/Burnout/Anxiety) ---
        # Q12 (Overwhelmed), Q13 (Drained), Q14 (Anxious), Q15 (Anhedonia), Q17 (Net Anxiety)
        stress_score = sum([data.q12_overwhelmed, data.q13_drained])
        anxiety_score = sum([data.q14_anxious, data.q15_anhedonia, data.q17_internet_anxiety])
        
        if stress_score >= 1:
             all_new_risks.append(DiseaseRisk(
                disease="High Chronic Stress / Burnout",
                risk_level=RiskLevel.HIGH if stress_score == 2 else RiskLevel.MODERATE,
                probability=0.70,
                contributing_factors=["Feeling Overwhelmed", "Emotional Exhaustion"],
                prevention_steps=["Mindfulness Breaks", "Work-Life Boundaries"]
            ))
        else:
             all_new_risks.append(DiseaseRisk(
                disease="High Chronic Stress / Burnout",
                risk_level=RiskLevel.LOW,
                probability=0.10,
                contributing_factors=["Balanced emotional state"],
                prevention_steps=["Continue stress management practices."]
            ))
            
        if anxiety_score >= 2:
             all_new_risks.append(DiseaseRisk(
                disease="Anxiety & Mood Risk",
                risk_level=RiskLevel.MODERATE,
                probability=0.60,
                contributing_factors=["Nervousness", "Digital Dependency"],
                prevention_steps=["Digital Detox", "Professional Counseling"]
            ))
        else:
             all_new_risks.append(DiseaseRisk(
                disease="Anxiety & Mood Risk",
                risk_level=RiskLevel.LOW,
                probability=0.10,
                contributing_factors=["Stable mood indicators"],
                prevention_steps=["Practice gratitude/journaling."]
            ))

        # --- 5. Sedentary Lifestyle ---
        # Q8 (>6h Sit), Q9 (Inactive)
        sed_score = 0
        if data.q8_sedentary: sed_score += 1
        if not data.vigorous_activity: sed_score += 1
        
        if sed_score >= 1:
            all_new_risks.append(DiseaseRisk(
                disease="Sedentary Lifestyle Risk",
                risk_level=RiskLevel.HIGH if sed_score == 2 else RiskLevel.MODERATE,
                probability=0.65,
                contributing_factors=["Prolonged Sitting", "Low Activity"],
                prevention_steps=["Standing Desk", "Hourly Movement Snacks"]
            ))
        else:
             all_new_risks.append(DiseaseRisk(
                disease="Sedentary Lifestyle Risk",
                risk_level=RiskLevel.LOW,
                probability=0.20,
                contributing_factors=["Active lifestyle"],
                prevention_steps=["Aim for 150min moderate activity/week."]
            ))

        return all_new_risks

    def _build_risk(self, name: str, prob: float, data: ClinicalInput, key_driver: str, threshold: float) -> DiseaseRisk:
        if prob > 0.7:
            level = RiskLevel.HIGH
        elif prob > 0.4:
            level = RiskLevel.MODERATE
        else:
            level = RiskLevel.LOW
            
        # Simple rule-based explanation for MVP (Layer 2 LLM would expand this)
        reasons = []
        driver_val = getattr(data, key_driver)
        if driver_val > threshold:
            reasons.append(f"Elevated {key_driver.replace('_', ' ').title()}")
        if data.bmi > 30:
            reasons.append("High BMI")
            
        steps = ["Consult your doctor for a checkup."]
        if level == RiskLevel.HIGH:
            steps.append("Prioritize lifestyle changes immediately.")
            
        return DiseaseRisk(
            disease=name,
            risk_level=level,
            probability=round(prob, 2),
            contributing_factors=reasons if reasons else ["General Risk Profile"],
            prevention_steps=steps
        )
