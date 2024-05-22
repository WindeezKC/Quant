import alpaca_trade_api as tradeapi
import pandas as pd
import time
from config import ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL

api = tradeapi.REST(ALPACA_API_KEY, ALPACA_SECRET_KEY, ALPACA_BASE_URL, api_version='v2')

def get_historical_data(symbol, start_date, end_date):
    retries = 3
    for attempt in range(retries):
        try:
            bars = api.get_bars(symbol, tradeapi.rest.TimeFrame.Minute, start=start_date, end=end_date).df
            return bars
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Sleeping for 3 seconds before retrying...")
                time.sleep(3)
            else:
                print("All retries failed. Exiting.")
                raise

def get_today_data(symbol):
    retries = 3
    for attempt in range(retries):
        try:
            today = pd.Timestamp.now(tz='America/New_York').strftime('%Y-%m-%d')
            bars = api.get_bars(symbol, tradeapi.rest.TimeFrame.Minute, start=today).df
            return bars
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Sleeping for 3 seconds before retrying...")
                time.sleep(3)
            else:
                print("All retries failed. Exiting.")
                raise

def get_latest_bar(symbol):
    retries = 3
    for attempt in range(retries):
        try:
            bar = api.get_bars(symbol, tradeapi.rest.TimeFrame.Minute, limit=1).df
            return bar.iloc[0]
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                print(f"Sleeping for 3 seconds before retrying...")
                time.sleep(3)
            else:
                print("All retries failed. Exiting.")
                raise
