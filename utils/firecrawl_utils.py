import requests
import pandas as pd
import time
import os

ALPHA_KEY = os.getenv("ALPHA_KEY")
FMP_KEY = os.getenv("FMP_KEY")
FRED_KEY = os.getenv("FRED_KEY")
SENTIMENT_KEY = os.getenv("SENTIMENT_KEY")
TICKERS_CACHE = "tickers.csv"

def fetch_ticker_list(force_refresh=False):
    if os.path.exists(TICKERS_CACHE) and not force_refresh:
        df = pd.read_csv(TICKERS_CACHE)
        return df['symbol'].tolist()
    url = f"https://financialmodelingprep.com/api/v3/stock/list?apikey={FMP_KEY}"
    r = requests.get(url).json()
    tickers = [item['symbol'] for item in r]
    pd.DataFrame({'symbol': tickers}).to_csv(TICKERS_CACHE, index=False)
    return tickers

def fetch_alpha(ticker):
    try:
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={ticker}&interval=5min&apikey={ALPHA_KEY}"
        r = requests.get(url).json()
        last_key = list(r['Time Series (5min)'].keys())[0]
        last_price = float(r['Time Series (5min)'][last_key]['4. close'])
        last_vol = float(r['Time Series (5min)'][last_key]['5. volume'])
        return last_price, last_vol
    except:
        return 0,0

def fetch_fmp(ticker):
    try:
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={FMP_KEY}&serietype=line"
        r = requests.get(url).json()
        historical = r.get("historical", [])[:50]
        closes = [x['close'] for x in historical]
        vols = [x.get('volume',1) for x in historical[:30]]
        return closes, vols
    except:
        return [], []

def fetch_marketaux_sentiment(ticker):
    try:
        url = f"https://api.marketaux.com/v1/news/all?symbols={ticker}&filter_entities=true&language=en&api_token={SENTIMENT_KEY}"
        r = requests.get(url).json()
        sentiments = [article.get('sentiment',0) for article in r.get('data',[])]
        return sum(sentiments)/len(sentiments) if sentiments else 0
    except:
        return 0

def calculate_resistance(closes, ma_period=50):
    if not closes or len(closes) < 2:
        return 1
    recent_high = max(closes[-50:])
    ma50 = sum(closes[-ma_period:])/ma_period
    return 0.7*recent_high + 0.3*ma50

def compute_score(df):
    df['Score'] = df['PriceVsRes']*0.4 + df['RelVol']*0.3 + df['PriceVsMA50']*0.2 + df['Sentiment']*0.1
    df['Class'] = pd.cut(df['Score'], bins=[-float('inf'),0.8,1.5,float('inf')], labels=['Low','Neutral','High'])
    df['Alert'] = df.apply(lambda x: 'BREAKOUT' if x['Score']>1.5 else '', axis=1)
    return df
