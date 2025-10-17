# 🔥 FireCrawl Sentinel

**Real-time Stock Monitoring Dashboard** - A comprehensive Streamlit application for tracking stock performance with intelligent scoring and alerts.

## 🚀 Features

- **Real-time Stock Monitoring**: Live price updates with configurable refresh intervals
- **Dynamic Ticker Selection**: Search and select from full US stock list (3000+ stocks)
- **Intelligent Scoring System**: Multi-factor analysis including:
  - Price vs Resistance levels
  - Volume analysis vs historical averages  
  - Moving Average (MA50) comparisons
  - News sentiment analysis
- **Visual & Audio Alerts**: Color-coded alerts with sound notifications
- **Interactive Charts**: Score distribution and correlation visualizations
- **Streamlit Cloud Compatible**: Optimized for cloud deployment

## ⚡ Quick Start

1. **Clone the repository**
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Set environment variables** (see DEPLOYMENT.md for details)
4. **Run locally**: `streamlit run app/app.py`
5. **Deploy to Streamlit Cloud** using the provided configuration

## 📊 Data Sources

- **Alpha Vantage**: Real-time stock prices and volume
- **Financial Modeling Prep**: Historical data and comprehensive ticker lists
- **MarketAux**: News sentiment analysis
- **FRED**: Economic indicators

## 🎯 Scoring Algorithm

The application uses a weighted scoring system:
- **Price vs Resistance (40%)**: Breakout potential analysis
- **Relative Volume (30%)**: Volume surge detection
- **Price vs MA50 (20%)**: Trend analysis
- **Sentiment (10%)**: News sentiment impact

## 📈 Live Application

Your FireCrawl Sentinel is currently running at: `http://localhost:8501`

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)
