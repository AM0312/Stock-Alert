import requests
from twilio.rest import Client

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_API_KEY = ""
NEWS_API_KEY = ""

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_SID = ""
TWILIO_AUTH_KEY = ""


stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=stock_params)
response.raise_for_status()
data = response.json()["Time Series (Daily)"]
data_list = [value for (key, value) in data.items()]
yesterday = data_list[0]
day_before = data_list[1]

yesterday_closing = yesterday["4. close"]
day_before_closing = day_before["4. close"]

# print(yesterday_closing)
# print(day_before_closing)
up_down = None
difference = float(yesterday_closing)-float(day_before_closing)
if difference > 0:
    up_down = "↑"
else:
    up_down = "↓"

diff_percent = round((abs(difference)/float(yesterday_closing))*100)
# print(diff_percent)

if diff_percent >= 1:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    news_response.raise_for_status()
    articles = news_response.json()["articles"][:3]
    formatted_articles = [
        f"{STOCK}: {up_down}{diff_percent}%\nHeadline: {article['title']}.\nBrief: {article['description']}" for article in articles]

    # print(articles)
    # print(formatted_articles)
    client = Client(TWILIO_SID, TWILIO_AUTH_KEY)
    for article in formatted_articles:
        message = client.messages.create(
            body=article,
            to="+",
            from_="+"
        )
