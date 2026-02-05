from abc import ABC, abstractmethod
from typing import Dict, List
from app.models.schemas import QuestionnaireInput, RiskScore, RiskLevel, PainFrequency, SleepQuality

class RiskEvaluator(ABC):
    @abstractmethod
    def evaluate(self, input_data: QuestionnaireInput) -> Dict[str, RiskScore]:
        pass

class RuleBasedEvaluator(RiskEvaluator):
    def evaluate(self, input_data: QuestionnaireInput) -> Dict[str, RiskScore]:
        risks = {}
        
        # 1. Musculoskeletal Risk
        # Drivers: High screen time (>8h), Poor posture (pain often/always)
        musculo_score = 0.0
        musculo_reasons = []
        musculo_recommendations = []
        
        if input_data.daily_screen_time_hours > 8:
            musculo_score += 0.4
            musculo_reasons.append("Daily screen time exceeds 8 hours.")
            musculo_recommendations.append("Follow the 20-20-20 rule: Every 20 mins, look 20 ft away for 20 secs.")
        
        if input_data.neck_pain_frequency in [PainFrequency.OFTEN, PainFrequency.ALWAYS]:
            musculo_score += 0.4
            musculo_reasons.append("Frequent neck pain reported.")
            musculo_recommendations.append("Check monitor ergonomics: Eye level should be at the top 1/3 of the screen.")
            
        if input_data.physical_activity_days_per_week < 2:
            musculo_score += 0.2
            musculo_reasons.append("Low physical activity.")
            musculo_recommendations.append("Incorporate stretch breaks every hour.")

        risks["musculoskeletal"] = self._create_risk_score(
            "Musculoskeletal", musculo_score, musculo_reasons, musculo_recommendations
        )

        # 2. Sleep Risk
        # Drivers: Low sleep (<6h), Screen time, Poor quality
        sleep_score = 0.0
        sleep_reasons = []
        sleep_recommendations = []
        
        if input_data.sleep_hours < 6.0:
            sleep_score += 0.5
            sleep_reasons.append("Sleep duration is less than 6 hours.")
            sleep_recommendations.append("Aim for 7-9 hours of consistent sleep.")
            
        if input_data.daily_screen_time_hours > 10:
            sleep_score += 0.3
            sleep_reasons.append("Excessive screen time may impact circadian rhythm.")
            
        if input_data.sleep_quality == SleepQuality.POOR:
            sleep_score += 0.2
            sleep_reasons.append("Self-reported poor sleep quality.")
            sleep_recommendations.append("Enable device 'Night Mode' after sunset.")

        risks["sleep"] = self._create_risk_score(
            "Sleep Health", sleep_score, sleep_reasons, sleep_recommendations
        )
        
        # 3. Mental Health Indicator (Proxy)
        # Drivers: Social media > 3h, High Stress, Low Sleep
        mental_score = 0.0
        mental_reasons = []
        mental_recommendations = []
        
        if input_data.social_media_hours > 3.0:
            mental_score += 0.3
            mental_reasons.append("High daily social media usage (>3 hours).")
            mental_recommendations.append("Set app limits for social media reduction.")
            
        if input_data.stress_level >= 8:
            mental_score += 0.4
            mental_reasons.append("High self-reported stress level.")
            mental_recommendations.append("Practice mindfulness or deep breathing exercises.")
            
        if input_data.sleep_hours < 5.0:
             mental_score += 0.3 # Sleep deprivation exacerbates anxiety
             mental_reasons.append("Severe sleep deprivation detected.")

        risks["mental_health"] = self._create_risk_score(
            "Digital Well-being", mental_score, mental_reasons, mental_recommendations
        )

        return risks

    def _create_risk_score(self, category: str, score: float, reasons: List[str], recs: List[str]) -> RiskScore:
        # Cap score at 1.0
        final_score = min(score, 1.0)
        
        # Determine Level
        if final_score < 0.3:
            level = RiskLevel.LOW
        elif final_score < 0.7:
            level = RiskLevel.MODERATE
        else:
            level = RiskLevel.HIGH
            
        # Default text if low risk
        if not reasons:
            reasons = ["No significant risk factors identified."]
        if not recs:
            recs = ["Maintain current healthy habits."]

        return RiskScore(
            category=category,
            score=round(final_score, 2),
            level=level,
            explanation="; ".join(reasons),
            recommendations=recs
        )
