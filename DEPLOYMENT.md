# 🚀 FireCrawl Sentinel - Deployment Guide

## 📋 Pre-Deployment Checklist

### ✅ Completed Tasks:
- [x] Removed hardcoded API keys (security fix)
- [x] Created main Streamlit application (`app/app.py`)
- [x] Updated dependencies in `requirements.txt`
- [x] Created test script to verify setup
- [x] Added `.env.example` for API key configuration

### 🔑 Required API Keys:
You need to obtain and configure these API keys:

1. **Alpha Vantage** (Stock Prices): https://www.alphavantage.co/support/#api-key
2. **Financial Modeling Prep** (Historical Data): https://financialmodelingprep.com/developer/docs  
3. **FRED** (Economic Data): https://fred.stlouisfed.org/docs/api/api_key.html
4. **MarketAux** (Sentiment): https://www.marketaux.com/

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended)

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit - FireCrawl Sentinel"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/firecrawl-sentinel.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your GitHub account
   - Select your repository
   - Set main file path: `app/app.py`
   - Add environment variables in the "Advanced settings":
     - `ALPHA_KEY`
     - `FMP_KEY`
     - `FRED_KEY`
     - `SENTIMENT_KEY`

### Option 2: Local Development

1. **Set Environment Variables (Windows PowerShell):**
   ```powershell
   $env:ALPHA_KEY='6IYZX9BYOB7W4KZP'
   $env:FMP_KEY='RzEy4416tdF4w0rCMXYD2OFVsAJIgNLY'
   $env:FRED_KEY='0c9d817350765cfa3510693cb18f73af'
   $env:SENTIMENT_KEY='wchoX6Hu2MdqNZrLArnahshe5hZi3MPLCQbdqM0O'
   ```

2. **Run the Application:**
   ```bash
   streamlit run app/app.py
   ```

### Option 3: Heroku

1. **Create `Procfile`:**
   ```
   web: streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Deploy:**
   ```bash
   heroku create firecrawl-sentinel
   heroku config:set ALPHA_KEY=6IYZX9BYOB7W4KZP
   heroku config:set FMP_KEY=RzEy4416tdF4w0rCMXYD2OFVsAJIgNLY
   heroku config:set FRED_KEY=0c9d817350765cfa3510693cb18f73af
   heroku config:set SENTIMENT_KEY=wchoX6Hu2MdqNZrLArnahshe5hZi3MPLCQbdqM0O
   git push heroku main
   ```

## 🧪 Testing Before Deployment

Run the test script to verify everything is working:
```bash
python test_setup.py
```

Expected output: "🎉 All tests passed! Ready for deployment!"

## 📱 Application Features

- **Real-time Stock Monitoring**: Live price updates with configurable refresh intervals
- **Dynamic Ticker Selection**: Search and select from full US stock list
- **Scoring System**: Comprehensive scoring based on resistance, volume, MA50, and sentiment
- **Visual Alerts**: Color-coded alerts with audio notifications
- **Interactive Charts**: Score distribution and price correlation visualizations
- **Streamlit Cloud Compatible**: Optimized for cloud deployment

## 🔧 Configuration Options

### Alert Settings:
- Adjustable score threshold for alerts
- Sound alerts with `.mp3` file support
- Color-coded status indicators

### Data Sources:
- Alpha Vantage: Real-time stock prices
- Financial Modeling Prep: Historical data and ticker lists
- MarketAux: News sentiment analysis
- Cached ticker list for performance

## 📊 Usage Instructions

1. **Select Tickers**: Use search or manual input to select stocks to monitor
2. **Configure Alerts**: Set your preferred alert threshold and options
3. **Monitor Dashboard**: Watch real-time scores and alerts
4. **Auto-refresh**: Enable automatic updates for continuous monitoring

## 🚨 Important Security Notes

- **Never commit API keys to version control**
- **Use environment variables for all sensitive data**
- **Regularly rotate your API keys**
- **Monitor API usage to avoid rate limits**

## 📞 Support

If you encounter issues:
1. Run `python test_setup.py` to diagnose problems
2. Check that all API keys are properly set
3. Verify internet connection for API calls
4. Review Streamlit Cloud logs for deployment issues

---

**Ready for deployment!** 🎉

Your FireCrawl Sentinel application is now fully configured and ready to be deployed to Streamlit Cloud or any other hosting platform.