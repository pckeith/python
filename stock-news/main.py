#*****************************************************
# Stock Price News App:                              *
# Author:    Keith Caldwell                          *
# Date:      August 15,2026                          *
#*****************************************************
# Description:                                       *
# This task is Day 36 of 100 days of Python:         *
# The purpose of this script is to look for          *
# significaant variations in the stock price, for    *
# a selected list of ticker symbols. When a          *
# significant price change is found in a given       *
# stock ticker symbol, both the price change and     *
# the top 3 news articles related to the ticker      *
# symbol, sorted by relevance (i.e.: selecting up    *
# 3 of the most relevant articles for the past 3     *
# days) will be sent as an email message for each    *
# of the affected tickers. This will be combined     *
# into one email message, covering all affected      *
# ticker symbols for that day.                       *
#                                                    *
# The percentage price change needed (to be sensed   *
# as a significant variation) will be determined by  *
# a parameter setting in this program. The variable  *
# named PRICE_CHANGE_THRESHOLD_PCT defines the       *
# significant change threshold for this program.     *
# It is a float variable, which defines the          *
# percentage change threshold applicable to the      *
# stock price, which will considered a significant   *
# change. This program calculates the change to a    *
# stock price as the difference between the closing  *
# price of the current day, compared to the closing  *
# price of the previous day.                         *
#                                                    *
# There are two APIs which will be referenced, to    *
# pull in stock price and news content into this     *
# program. These two APIs are as follows:            *
#                                                    *
# 1) The Stock Endpoint:                             *
#    "https://www.alphavantage.co/query"             *
# 2) The News Endpoint:                              *
#    "https://newsapi.org/v2/everything"             *
#*****************************************************

# ---------------------------- LIBRARY IMPORTS ------------------------ #
from pathlib import *
import os
from dotenv import load_dotenv
import email.message
import smtplib
import requests
import html
import time
from datetime import date, datetime, timedelta, timezone


# ---------------------------- GLOBAL VARIABLES ----------------------- #

TICKER_LIST = ('AAPL','AMZN','BMY','MSFT')
PRICE_CHANGE_THRESHOLD_PCT = 5.0
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
SMTP_PORT = 465  # Switched to SSL port (Note: 587 works for plain SMTP connection)

news_begin_date = (date.today() - timedelta(days=4)).isoformat()
news_end_date = (date.today() - timedelta(days=1)).isoformat()

# ---------------------------- FUNCTION DEFINITIONS ------------------- #
def fetch_stock_data(ticker, stock_api_key, stock_endpoint):
    """Fetches stock data and returns it as a formatted string."""
    output = []

    # 1. Fetch Company Overview
    stock_name_parameters = {
        "function": "OVERVIEW",
        "symbol": ticker,
        "apikey": stock_api_key,
    }
    try:
        response = requests.get(url=stock_endpoint, params=stock_name_parameters)
        response.raise_for_status()
        data = response.json()
        company_name = data.get("Name", "Unknown Company")
    except Exception as e:
        company_name = f"Error fetching name ({e})"

    output.append(f"Company Name: {company_name}")
    time.sleep(1.1)  # Rate limiting delay

    # 2. Fetch Daily Time Series
    stock_price_parameters = {
        "function": "TIME_SERIES_DAILY",
        "symbol": ticker,
        "apikey": stock_api_key,
    }
    try:
        response = requests.get(url=stock_endpoint, params=stock_price_parameters)
        response.raise_for_status()
        data = response.json()

        time_series = data.get("Time Series (Daily)", {})
        all_dates_sorted = sorted(time_series.keys(), reverse=True)
        latest_two_dates = all_dates_sorted[:2]

        prices = []
        for index, date in enumerate(latest_two_dates, start=1):
            day_label = "Latest Day" if index == 1 else "Previous Day"
            day_data = time_series[date]
            close_price = day_data.get("4. close", "N/A")
            output.append(f"  - {day_label} ({date}): Close: {close_price}")
            
            # Save prices for percentage calculation
            if close_price != "N/A":
                prices.append(float(close_price))

        # Calculate percentage change if we have exactly two days of data
        significant_change = False
        percentage_change = 0.0

        if len(prices) == 2:
            latest_close, prev_close = prices[0], prices[1]
            percentage_change = abs((latest_close - prev_close) / prev_close) * 100
            # Track if the change meets or exceeds 5%
            if percentage_change >= PRICE_CHANGE_THRESHOLD_PCT:
                significant_change = True
                output.append(f"  - Price Change: {percentage_change:.2f}% (Significant)")
            else:
                output.append(f"  - Price Change: {percentage_change:.2f}%")

    except Exception as e:
        output.append(f"  - Error fetching price series: {e}")
        significant_change = False
        percentage_change = 0.0

    time.sleep(1.1)
    return "\n".join(output), significant_change, percentage_change



def fetch_news_data(
    ticker, news_api_id, news_endpoint, news_begin_date, news_end_date
):
    """Fetches up to 3 news articles and returns them as a formatted string."""
    output = ["\nRecent News:"]
    news_parameters = {
        "q": ticker,
        "from": news_begin_date,
        "to": news_end_date,
        "sortBy": "relevancy",
        "apiKey": news_api_id,
    }

    try:
        response = requests.get(url=news_endpoint, params=news_parameters)
        response.raise_for_status()
        data = response.json()

        target_keys = ["title", "description", "url", "author", "publishedAt"]
        extracted_articles = [
            {key: article.get(key) for key in target_keys}
            for article in data.get("articles", [])
        ]

        if not extracted_articles:
            output.append("  No articles found.")

        for i, article in enumerate(extracted_articles[:3], start=1):
            desc = article.get("description") or "No description available"
            url = article.get("url") or "No URL provided"
            raw_date = article.get("publishedAt")

            if raw_date:
                dt = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))
                date = dt.strftime("%Y-%m-%d %H:%M")
            else:
                date = "Unknown date"

            output.append(f"  [{i}] Date: {date}\n      URL: {url}\n      Info: {desc}")
    except Exception as e:
        output.append(f"  Error fetching news: {e}")

    time.sleep(1.1)
    return "\n".join(output)


# ---------------------------- MAIN PROGRAM FLOW ---------------------- #

#*********************************************************
# Note: Use Environment variables to keep confidential   *
#       information out of the Python program code. This *
#       way it's only loaded at runtime, when needed.    *
#*********************************************************
load_dotenv() # Get email & API account information
stock_api_key = os.getenv("STOCK_API_KEY")
news_api_id = os.getenv("NEWS_API_ID")
SMTP_SERVER = os.getenv("SMTP_SERVER")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

# 1. Initialize the master string for the email body
email_body_content = f"Stock and News Report - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
email_body_content += "=" * 60 + "\n"

# Keep track of how many tickers had a >= 5% change
significant_ticker_count = 0

# 2. Iterate through tickers and compile the reports
for ticker in TICKER_LIST:
    print(f"Gathering data for {ticker}...")  # Terminal status indicator

    # Unpack text output, the true/false flag, and the raw percentage change calculated
    stock_info, significant_change, actual_change = fetch_stock_data(
        ticker=ticker,
        stock_api_key=stock_api_key,
        stock_endpoint=STOCK_ENDPOINT,
    )

    #*****************************************************
    # ONLY proceed with news and email addition if       *
    # price change is >= Significant Change threshold    *
    #*****************************************************
    if significant_change:
        significant_ticker_count += 1
        email_body_content += f"\n\n=== {ticker} ===\n"
        email_body_content += stock_info

        # Fetch and append news data
        news_info = fetch_news_data(
            ticker=ticker,
            news_api_id=news_api_id,
            news_endpoint=NEWS_ENDPOINT,
            news_begin_date=news_begin_date,
            news_end_date=news_end_date,
        )
        email_body_content += news_info
    else:
        # Verbose console reporting showing the actual vs required threshold
        print(f" -> Skipped {ticker}: Actual change was {actual_change:.2f}%, which is under the {PRICE_CHANGE_THRESHOLD_PCT}% threshold.")

email_body_content += "\n\n" + "=" * 60 + "\nEnd of Report."


# 3. Create and send the email
if significant_ticker_count > 0:
    print(f"\n{significant_ticker_count} volatile ticker(s) found. Sending email...")

    try:
        # Set up email headers
        msg = email.message.EmailMessage()
        msg["Subject"] = f"Daily Stock & News Summary ({datetime.now().strftime('%Y-%m-%d')})"
        msg["From"] = SENDER_EMAIL
        msg["To"] = RECIPIENT_EMAIL
        msg.set_content(email_body_content)
          
        #*************************************************************************
        # Establish secure connection and transmit:                              *
        # Note: We're using SMTP_SSL, but can use SMTP for port 587 as follows:  *
        # with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as connection:               *
        #*************************************************************************
        # Use SMTP_SSL for port 465
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as connection:
            connection.login(SENDER_EMAIL, SENDER_PASSWORD)
            connection.send_message(msg)
            print("Email sent successfully!")

    except Exception as e:
        print(f"Failed to send email. Error: {e}")
else:
    print(f"\nNo tickers experienced a price change of {PRICE_CHANGE_THRESHOLD_PCT}% or more. Email skipped.")
