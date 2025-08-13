import requests
from datetime import datetime
import smtplib
import time
import os
from dotenv import load_dotenv
load_dotenv()

MY_LAT = os.getenv("MY_LAT")
MY_LONG = os.getenv("MY_LONG")
MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv('PASSWORD')
def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT - 5 <= iss_latitude <= MY_LAT+5 and MY_LONG-5 <= iss_longitude <= MY_LONG+5:
        return True

#Your position is within +5 or -5 degrees of the ISS position.



def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True

while True:
    if is_night() and is_iss_overhead():
        connection = smtplib.SMTP("smtp.gmail.com", 587)
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg="Subject: ISS\n\n Look up ISS is passing through.")
    time.sleep(60)


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.



