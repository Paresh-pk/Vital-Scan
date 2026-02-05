import os
import json
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
from app.models.schemas import DiseaseRisk, RiskLevel

# Load environment variables
load_dotenv()

class LLMService:
    """
    Layer 2: Explanation & Prevention Engine.
    Uses Hugging Face (GLM-4) via OpenAI Client for dynamic advice.
    """
    
    def __init__(self):
        # Load API Key from Environment
        self.api_key = os.getenv("HF_TOKEN")
        self.base_url = "https://router.huggingface.co/v1"
        self.model_name = "openai/gpt-oss-120b:groq"
        
        if self.api_key:
            self.client = OpenAI(
                base_url=self.base_url,
                api_key=self.api_key,
            )
        else:
            print("WARNING: No HF_TOKEN found. Using template fallback.")

    def generate_explanation(self, risks: List[DiseaseRisk], user_profile: dict = None) -> List[DiseaseRisk]:
        """
        Enriches risk objects with LLM-generated advice.
        """
        # Create/Append to debug log
        def log_debug(msg):
            with open("server_debug.log", "a", encoding="utf-8") as f:
                f.write(f"\n[{pd.Timestamp.now()}] {msg}\n")

        if not self.api_key:
            log_debug("ERROR: API Key missing.")
            return self._template_fallback(risks)

        try:
            # 1. Build Prompt
            prompt = self._build_prompt(risks, user_profile)
            log_debug(f"PROMPT SENT:\n{prompt[:200]}...[truncated]...")
            
            # 2. Call Hugging Face API
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "system", 
                        "content": "You are an expert Preventive Health Advisor. You output STRICT JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=4000  # Increased for 8 diseases × 5 suggestions each
            )
            
            # 3. Parse JSON Response
            content = completion.choices[0].message.content
            log_debug(f"RAW RESPONSE:\n{content}")
            
            # Clean markdown if model adds it despite instructions
            content = content.replace("```json", "").replace("```", "").strip()
            
            # Repair incomplete JSON (common with long responses)
            content = self._repair_json(content)
            
            advice_map = json.loads(content)
            
            # 4. Map back to objects
            for risk in risks:
                if risk.disease in advice_map:
                    data = advice_map[risk.disease]
                    if "prevention_steps" in data:
                        risk.prevention_steps = data["prevention_steps"]
            
            return risks

        except Exception as e:
            log_debug(f"EXCEPTION CAUGHT: {str(e)}")
            return self._template_fallback(risks)
    
    def _repair_json(self, text: str) -> str:
        """
        Repairs common JSON truncation issues from LLM responses.
        """
        # If already valid, return as-is
        try:
            json.loads(text)
            return text
        except:
            pass
        
        # Close unterminated strings
        if text.count('"') % 2 != 0:
            text += '"'
        
        # Close unterminated arrays
        open_brackets = text.count('[') - text.count(']')
        text += ']' * open_brackets
        
        # Close unterminated objects
        open_braces = text.count('{') - text.count('}')
        text += '}' * open_braces
        
        return text

    def _template_fallback(self, risks: List[DiseaseRisk]) -> List[DiseaseRisk]:
        """
        Robust fallback using pre-approved clinical text templates.
        Updated to match the 5-item, structured format regarding Action, Rationale, and Outcome.
        """
        for risk in risks:
            if not risk.contributing_factors:
                continue

            if risk.disease == "Type 2 Diabetes":
                risk.prevention_steps = [
                    "**Initiate 'Walking Prescriptions'**: Walk for 15 minutes immediately after lunch and dinner. *Why*: Muscle activity burns glucose without insulin. *Result*: Lower post-meal blood sugar.",
                    "**Optimize Carbohydrate Timing**: Eat carbs only *after* vegetables and protein in your meal. *Why*: Fiber blunts the sugar spike. *Result*: Stable energy levels.",
                    "**Strength Training Micro-Dosing**: Do 20 squats or push-ups before showering. *Why*: Increases insulin sensitivity in muscles. *Result*: Better long-term glucose control.",
                    "**Sleep Hygiene Audit**: Extend sleep to 7.5 hours minimum. *Why*: Sleep deprivation causes insulin resistance. *Result*: Lower morning fasting glucose.",
                    "**Swap Sugary Drinks**: Replace soda/juice with water or tea. *Why*: Liquid sugar spikes insulin rapidly. *Result*: Immediate caloric reduction and metabolic relief."
                ]
            elif risk.disease == "Hypertension":
                risk.prevention_steps = [
                    "**Sodium Pattern Interrupt**: Stop adding salt at the table entirely. *Why*: Excess sodium retains water, raising pressure. *Result*: potential 5-10 point systolic drop.",
                    "**Box Breathing Protocol**: Practice 4-4-4-4 breathing for 2 minutes when stressed. *Why*: Activates parasympathetic nervous system. *Result*: Immediate acute BP reduction.",
                    "**Increase Potassium Intake**: Eat one banana or avocado daily. *Why*: Potassium helps kidneys excrete sodium. *Result*: Balanced electrolyte levels.",
                    "**Aerobic Consistency**: Walk briskly for 30 minutes, 5 days/week. *Why*: Strengthens the heart muscle. *Result*: Lower resting heart rate and pressure.",
                    "**Limit Alcohol**: Cap intake to 1 drink/day maximum. *Why*: Alcohol is a direct vasoconstrictor. *Result*: Prevention of evening BP spikes."
                ]
            else:
                # Generic robust fallback for other diseases
                risk.prevention_steps = [
                    "**Consult a Specialist**: Schedule a targeted review for this specific condition. *Why*: Clinical evaluation is required for diagnosis. *Result*: Accurate treatment plan.",
                    "**Track Symptoms Daily**: Log occurrences of symptoms in a journal. *Why*: Identifying triggers helps management. *Result*: Better data for your doctor.",
                    "**Prioritize Sleep**: Aim for 7-8 hours of quality rest. *Why*: Recovery happens during sleep. *Result*: Improved systemic resilience.",
                    "**Hydration Strategy**: Drink 2.5L of water daily. *Why*: Dehydration exacerbates most chronic stress. *Result*: Better cellular function.",
                    "**Stress Reduction**: Practice 10 mins of mindfulness. *Why*: Cortisol management improves most conditions. *Result*: Mental clarity."
                ]
            
        return risks

    def _build_prompt(self, risks: List[DiseaseRisk], profile: dict) -> str:
        """
        Constructs a deeply personalized system prompt for Hugging Face/GLM-4.
        """
        risk_summary = []
        for r in risks:
            risk_summary.append({
                "disease": r.disease,
                "severity": r.risk_level,
                "drivers": r.contributing_factors
            })

        profile_str = json.dumps(profile, indent=2) if profile else "Unknown Profile"

        return f"""
        You are an elite Preventive Health Consultant. Your goal is to provide highly personalized, life-changing advice.

        ### 1. PATIENT PROFILE
        {profile_str}

        ### 2. IDENTIFIED RISKS
        {json.dumps(risk_summary, indent=2)}

        ### 3. YOUR TASK
        For EACH disease listed above, generate exactly **5 Concrete, Prevention/Mitigation Steps**.
        
        ### 4. CRITICAL RULES (Strict Adherence Required)
        1. **Deep Personalization**: Do NOT say "Exercise more". Look at their specific profile. 
           - If Age=25 and Sedentary: Suggest "HIIT or Competitive Sports".
           - If Age=60 and Sedentary: Suggest "Brisk Walking or Swimming".
           - If Sleep=5h: Suggest "Magnesium glycinate or Blackout curtains".
        2. **Structure**: Each suggestion must contain:
           - **Action**: What strictly to do.
           - **Rationale**: Why this helps THIS specific user (mention their metrics).
           - **Outcome**: What will improve.
        3. **Sort Order**: Most impactful first.
        4. **Safety**: Do not diagnosis. Add simple caveats (e.g. "if knees allow").

        ### 5. OUTPUT FORMAT
        Return STRICT JSON only. The "prevention_steps" array must contain strings formatted like:
        "**[Action Name]**: [Detailed Instruction]. *Why*: [Rationale]. *Result*: [Outcome]."

        Example JSON Structure:
        {{
            "Type 2 Diabetes": {{
                "prevention_steps": [
                    "**Start Post-Meal Walks**: Walk for 10 mins after dinner. *Why*: Your HbA1c is 5.8 and you sit 8h/day. *Result*: Blunted glucose spike.",
                    "**Swap Latex Focus**: ...",
                    ... (5 items)
                ]
            }},
            ...
        }}
        """
