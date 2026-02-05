import requests
import json

url = "http://127.0.0.1:8000/api/v1/assess"
data = {
    "age": 45, "gender": 1, "bmi": 28.5, "systolic_bp": 130, 
    "hba1c": 5.7, "cholesterol": 200, "vigorous_activity": False, 
    "sleep_hours": 6.5, "smoker_history": True,
    "q1_bp_history": True, "q2_diabetes_history": False, "q3_family_heart": True,
    "q4_dry_eyes": True, "q5_headaches": True, "q6_neck_pain": True,
    "q7_back_pain": True, "q8_sedentary": True, "q11_insomnia": True,
    "q12_overwhelmed": True, "q13_drained": True, "q14_anxious": True,
    "q15_anhedonia": True, "q16_phone_bedtime": True, "q17_internet_anxiety": True,
    "q18_breathlessness": True, "q19_fatigue": True, "q20_diet": True,
    "daily_digital_hours": 8.0
}

try:
    print(f"Sending request to {url}...")
    res = requests.post(url, json=data)
    print(f"Status Code: {res.status_code}")
    if res.status_code == 200:
        print("Success! Check server_debug.log")
    else:
        print(f"Error: {res.text}")
except Exception as e:
    print(f"Failed to connect: {e}")
