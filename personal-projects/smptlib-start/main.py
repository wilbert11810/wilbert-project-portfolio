
import datetime as dt
import smtplib
import random
import os
from dotenv import load_dotenv
load_dotenv()

MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")

now = dt.datetime.now()
current_day = now.weekday()
if current_day == 3:
    with open("./quotes.txt", 'r') as quotes:
        list_of_quotes = quotes.readlines()
        quotes_of_the_day = random.choice(list_of_quotes)

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user= MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr= MY_EMAIL, to_addrs= MY_EMAIL, msg=f"Subject:Quotes of the day.\n\n {quotes_of_the_day}")