import requests
from datetime import datetime
import os

WEIGHT = 55
HEIGHT = 164
AGE = 21
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")
format_headers = {
    "Authorization": os.environ.get("AUTHORIZATION")
}

nutritionapi_url = "https://trackapi.nutritionix.com/v2/natural/exercise"
spreadsheet_api = "https://api.sheety.co/15764f0bd71b7705c37645f8b95422bf/workoutTracking/workouts"
headers = {
    'Content-Type': 'application/json',
    'x-app-id': APP_ID,
    'x-app-key': APP_KEY
}
user_input = input("Tell me which exercises you did: ")
data = {
    'query': user_input,
    'weight_kg': WEIGHT,
    'height_cm': HEIGHT,
    'age': AGE
}

response = requests.post(nutritionapi_url, headers=headers, json=data)
data = response.json()["exercises"]
today_date = datetime.now().strftime("%x")
current_time = datetime.now().strftime("%X")

for exercise in data:
    body = {
        'workout': {
            'date': today_date,
            'time': current_time ,
            'exercise': exercise["name"].title(),
            'duration': exercise["duration_min"],
            'calories': exercise["nf_calories"]
        }
    }

    formatted_data = requests.post(spreadsheet_api, headers=format_headers, json=body)
    print(formatted_data.json())