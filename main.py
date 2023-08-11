import requests
import os
from twilio.rest import Client
# from twilio.http.http_client import TwilioHttpClient

# proxy_client = TwilioHttpClient()
# proxy_client.session.proxies = {'https': os.environ['https_proxy']}

STOCK = "ABNB"
COMPANY_NAME = "Airbnb"
API_KEY = "DL09AE42ZIOJ4WBT"
NEWS_API_KEY = "686f96994a3943cc8c4ed1b5622a8dca"
URL = "https://www.alphavantage.co/query"
account_sid = "AC5cb620f3b5c2013b7979a2095828513a"
auth_token = "98e8f86a21fbb57b710d0168e3d8d145"
client = Client(account_sid, auth_token)

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "datatype": "json",
    "apikey": API_KEY

}

response = requests.get(url=URL, params=stock_params)

stock_data = response.json()
stock_slice = list(stock_data["Time Series (Daily)"])

today = stock_slice[0]
yesterday = stock_slice[1]

today_results = float(stock_data["Time Series (Daily)"][today]["4. close"])
yesterday_results = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])

percent_change = ((today_results - yesterday_results) / yesterday_results) * 100
rounded_percent_change = round(percent_change)

stock_change = 0

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

news_params = {
    "apiKey": NEWS_API_KEY,
    "q": COMPANY_NAME,
    "searchIn": "title",
    "language": "en",
    "sortBy": "publishedAt"
}

news_response = requests.get(url="https://newsapi.org/v2/everything", params=news_params)
news = news_response.json()
news_list = news["articles"][0:3]

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number.

if rounded_percent_change <= 0:
    stock_change = 1
elif rounded_percent_change >= 0:
    stock_change = 2


if stock_change == 1:
    message = client.messages \
                .create(
                    body=f"{COMPANY_NAME}: 🔻{abs(rounded_percent_change)}%\nHeadline: {news_list[0]['title']}\nBrief:"
                         f" {news_list[0]['description']}\n\n\nHeadline: {news_list[1]['title']}\nBrief:"
                         f" {news_list[1]['description']}\n\n\nHeadline: {news_list[2]['title']}\nBrief:"
                         f" {news_list[2]['description']}\n",
                    from_='+18777011027',
                    to="+19293952326"
                )
    print(message.sid)
elif stock_change == 2:
    message = client.messages \
                .create(
                    body=f"{COMPANY_NAME}: 🔺{rounded_percent_change}%\nHeadline: {news_list[0]['title']}Brief:"
                    f" {news_list[0]['description']}\nHeadline: {news_list[1]['title']}Brief:"
                    f" {news_list[1]['description']}\nHeadline: {news_list[2]['title']}Brief:"
                    f" {news_list[2]['description']}\n",
                    from_='+18777011027',
                    to="+19293952326"
                 )
    print(message.sid)


