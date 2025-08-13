from bs4 import BeautifulSoup
import requests
import smtplib
from dotenv import load_dotenv
import os
import re

load_dotenv()

MY_EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("EMAIL_PW")
URL = "https://www.amazon.com/Aussie-Miracle-Conditioner-Treatment-Australian/dp/B0857LTYZ2/ref=sr_1_1?crid=JLEW9D14PCC3&dib=eyJ2IjoiMSJ9.mqGWcQjlrnkzQ9tKCg59rUkbKreWaAD87pU-mbCFhGAw-ySV8n3uhbsgdI6V-1bJx2UJ0Jt4j3bLeuNQlxTZOvd96ejtijKblwzfoHbiAc3fO5sSfrDgT80uf5_Pr1QTo9R1nJhEH4w5TZPdMkwx8Wwk5WL-nhhErSoSWJZ55bmyvXASgw6R3UcHEe_g6grcPBf4o-b41FyzRflOrBEIf99yHE4Bh6OT6Tnga00fW7kt7Ba1nmLeYnV_fdSwyX1NnAZI76qIT_t0iFjJTzpIdSAvdH6mdyx5Pxyp5hVfO0E.vg_u-AqGH0J0VedRvpIlO8GiwWA-oobQmyIDJyaIrU4&dib_tag=se&keywords=aussie&qid=1754483202&sprefix=aus%2Caps%2C323&sr=8-1&th=1"
HEADER = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9,en-AU;q=0.8,id;q=0.7",
    "Priority": "u=0, i",
    "Sec-Ch-Ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": "\"Windows\"",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "cross-site",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"}
response = requests.get(URL, headers=HEADER)
soup = BeautifulSoup(response.text, "html.parser")
price = soup.find_all("span", class_="aok-offscreen")
title = soup.find("span", id="productTitle").get_text()
clean_title = re.sub(r'\s+', ' ', title).strip()
price_value = float(price[1].getText().split("$")[1])
subject = "Price Alert!"
body = f"{clean_title} has dropped to {price_value}. Quickly grab your product before you miss out. {URL}"
message = f"Subject: {subject}\n\n{body}"
if price_value < 200:
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=message.encode("utf-8"))

