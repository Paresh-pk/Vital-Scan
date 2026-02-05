import requests
import json

data = {
    "age": 45,
    "gender": 1,
    "bmi": 28.5,
    "systolic_bp": 120,
    "hba1c": 5.4,
    "cholesterol": 190,
    "vigorous_activity": True,
    "sleep_hours": 7.5,
    "smoker_history": False,
    "q1_bp_history": False,
    "q2_diabetes_history": False,
    "q3_family_heart": False,
    "q4_dry_eyes": True,
    "q5_headaches": True,
    "q6_neck_pain": False,
    "q7_back_pain": False,
    "q8_sedentary": False,
    "q11_insomnia": False,
    "q12_overwhelmed": False,
    "q13_drained": False,
    "q14_anxious": False,
    "q15_anhedonia": False,
    "q16_phone_bedtime": False,
    "q17_internet_anxiety": False,
    "q18_breathlessness": False,
    "q19_fatigue": False,
    "q20_diet": False,
    "daily_digital_hours": 8.0
}

try:
    print("Testing API...")
    r = requests.post("http://127.0.0.1:8000/api/v1/assess", json=data, timeout=10)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        print("Success!")
        print(json.dumps(r.json(), indent=2)[:500]) # Print first 500 chars
    else:
        print("Error Response:")
        print(r.text)
except Exception as e:
    print(f"Failed to connect: {e}")
