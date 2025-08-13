import re
from twilio.rest import Client
import requests
import os
from dotenv import load_dotenv
load_dotenv()

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_URL = os.getenv("STOCK_URL")
STOCK_API = os.getenv("STOCK_API")
STOCK_PARAM = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": STOCK_API,
}
NEWS_API = os.getenv("NEWS_API")
NEWS_URL = os.getenv("NEWS_URL")
DAY_OF_STOCK = []
PRICES_DATE = []
HEADLINES = {}
NEWS_PARAM = {
    "q": COMPANY_NAME,
    "from": "",
    "language": "en",
    "apiKey": NEWS_API
}
ACCOUNT_SID = os.getenv("ACCOUNT_SID")
AUTH_TOKEN = os.getenv("AUTH_TOKEN")
## STEP 1: Use https://www.alphavantage.co/
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
def check_stock():
    response = requests.get(STOCK_URL, params=STOCK_PARAM)
    response.raise_for_status()
    data = response.json()["Time Series (Daily)"]
    i = 0
    for value in data:
        if i == 2:
            break
        else:
            DAY_OF_STOCK.append(value)
            i += 1
    for date in DAY_OF_STOCK:
        PRICES_DATE.append(float(data[date]["4. close"]))

    changes = round(((PRICES_DATE[0] - PRICES_DATE[1])/ PRICES_DATE[1] * 100), 2)
    return changes



## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
def news_alert():
    NEWS_PARAM["from"] = DAY_OF_STOCK[1]
    response_news = requests.get(NEWS_URL, params=NEWS_PARAM)
    response_news.raise_for_status()
    data_news = response_news.json()["articles"]
    a = 0
    while a < 3:
        title = data_news[a]["title"]
        description = data_news[a]["description"]
        sentences = re.split(r"(?<=[.!?]) +", description)
        limited_description = "".join(sentences[:1])
        HEADLINES[title] = limited_description
        a += 1


## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def news_stock_alert():
    percentages = check_stock()
    up_down = None
    print(percentages)
    if abs(percentages):
        if percentages < 0:
            up_down = "🔻"
        else:
            up_down = " ↑ "
        news_alert()
        print(HEADLINES)
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        for index, value in HEADLINES.items():
            message = client.messages.create(
                body=f"{STOCK}: {up_down}{abs(percentages)}% \nHeadline: {index} \nBrief: {value}",
                from_='+17623164549',
                to='+61423000802'
            )
            print(message.status)

news_stock_alert()
#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

