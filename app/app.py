import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import time
import os
import sys
from pathlib import Path

# Add utils directory to path
utils_path = Path(__file__).parent.parent / "utils"
sys.path.append(str(utils_path))

from firecrawl_utils import (
    fetch_ticker_list, 
    fetch_alpha, 
    fetch_fmp, 
    fetch_marketaux_sentiment,
    calculate_resistance,
    compute_score
)

# Page configuration
st.set_page_config(
    page_title="FireCrawl Sentinel",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .alert-high {
        background-color: #ff4b4b;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .alert-neutral {
        background-color: #ffa500;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
    .alert-low {
        background-color: #00cc00;
        color: white;
        padding: 0.5rem;
        border-radius: 0.25rem;
        text-align: center;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

def check_api_keys():
    """Check if all required API keys are set"""
    required_keys = ["ALPHA_KEY", "FMP_KEY", "FRED_KEY", "SENTIMENT_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        st.error(f"Missing API keys: {', '.join(missing_keys)}")
        st.info("Please set the following environment variables:")
        st.code("$env:ALPHA_KEY='6IYZX9BYOB7W4KZP'")
        st.code("$env:FMP_KEY='RzEy4416tdF4w0rCMXYD2OFVsAJIgNLY'")
        st.code("$env:FRED_KEY='0c9d817350765cfa3510693cb18f73af'")
        st.code("$env:SENTIMENT_KEY='wchoX6Hu2MdqNZrLArnahshe5hZi3MPLCQbdqM0O'")
        return False
    return True

def play_alert():
    """Play alert sound"""
    try:
        assets_path = Path(__file__).parent.parent / "assets" / "alert.mp3"
        if assets_path.exists():
            # For Streamlit Cloud compatibility
            st.audio(str(assets_path), format="audio/mp3", autoplay=True)
    except Exception as e:
        st.warning(f"Could not play alert sound: {e}")

def fetch_stock_data(ticker):
    """Fetch comprehensive stock data"""
    try:
        # Get current price and volume
        current_price, current_vol = fetch_alpha(ticker)
        
        # Get historical data
        closes, volumes = fetch_fmp(ticker)
        
        # Get sentiment
        sentiment = fetch_marketaux_sentiment(ticker)
        
        if not closes or current_price == 0:
            return None
            
        # Calculate metrics
        resistance = calculate_resistance(closes)
        ma50 = sum(closes[-50:]) / min(50, len(closes)) if closes else current_price
        avg_vol = sum(volumes) / len(volumes) if volumes else current_vol
        
        return {
            'ticker': ticker,
            'current_price': current_price,
            'current_vol': current_vol,
            'resistance': resistance,
            'ma50': ma50,
            'avg_vol': avg_vol,
            'sentiment': sentiment,
            'closes': closes,
            'volumes': volumes
        }
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {e}")
        return None

def calculate_metrics(data):
    """Calculate trading metrics"""
    if not data:
        return None
        
    price_vs_res = data['current_price'] / data['resistance'] if data['resistance'] else 1
    price_vs_ma50 = data['current_price'] / data['ma50'] if data['ma50'] else 1
    rel_vol = data['current_vol'] / data['avg_vol'] if data['avg_vol'] else 1
    
    return {
        'PriceVsRes': price_vs_res,
        'PriceVsMA50': price_vs_ma50,
        'RelVol': rel_vol,
        'Sentiment': data['sentiment']
    }

def main():
    st.title("🔥 FireCrawl Sentinel")
    st.markdown("*Real-time Stock Monitoring Dashboard*")
    
    # Check API keys
    if not check_api_keys():
        st.stop()
    
    # Sidebar
    st.sidebar.header("📊 Configuration")
    
    # Auto-refresh settings
    auto_refresh = st.sidebar.checkbox("Auto Refresh", value=True)
    refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 30, 300, 60)
    
    # Ticker selection
    st.sidebar.subheader("Stock Selection")
    
    # Load ticker list
    with st.spinner("Loading ticker list..."):
        try:
            all_tickers = fetch_ticker_list()
            st.sidebar.success(f"Loaded {len(all_tickers)} tickers")
        except Exception as e:
            st.sidebar.error(f"Error loading tickers: {e}")
            all_tickers = ["AAPL", "GOOGL", "MSFT", "TSLA", "NVDA"]  # Fallback list
    
    # Ticker input methods
    input_method = st.sidebar.radio("Select Method:", ["Search & Select", "Manual Input"])
    
    if input_method == "Search & Select":
        search_term = st.sidebar.text_input("Search tickers:")
        if search_term:
            filtered_tickers = [t for t in all_tickers if search_term.upper() in t.upper()][:50]
        else:
            filtered_tickers = all_tickers[:50]  # Show first 50 by default
        
        selected_tickers = st.sidebar.multiselect(
            "Select Tickers:",
            filtered_tickers,
            default=["AAPL", "MSFT", "GOOGL"] if not search_term else []
        )
    else:
        ticker_input = st.sidebar.text_area(
            "Enter tickers (comma-separated):",
            value="AAPL,MSFT,GOOGL,TSLA,NVDA"
        )
        selected_tickers = [t.strip().upper() for t in ticker_input.split(",") if t.strip()]
    
    # Alert settings
    st.sidebar.subheader("🚨 Alert Settings")
    alert_threshold = st.sidebar.slider("Alert Score Threshold", 1.0, 2.0, 1.5, 0.1)
    sound_alerts = st.sidebar.checkbox("Sound Alerts", value=True)
    
    if not selected_tickers:
        st.warning("Please select at least one ticker to monitor.")
        st.stop()
    
    # Main dashboard
    st.header("📈 Live Dashboard")
    
    # Create placeholder for data
    data_placeholder = st.empty()
    
    # Initialize session state
    if 'last_alerts' not in st.session_state:
        st.session_state.last_alerts = set()
    
    # Main data fetching and display loop
    while True:
        with data_placeholder.container():
            # Fetch data for all tickers
            all_data = []
            progress_bar = st.progress(0)
            
            for i, ticker in enumerate(selected_tickers):
                progress_bar.progress((i + 1) / len(selected_tickers))
                
                with st.spinner(f"Fetching {ticker}..."):
                    stock_data = fetch_stock_data(ticker)
                    
                if stock_data:
                    metrics = calculate_metrics(stock_data)
                    if metrics:
                        row_data = {
                            'Ticker': ticker,
                            'Price': stock_data['current_price'],
                            'Resistance': stock_data['resistance'],
                            'MA50': stock_data['ma50'],
                            'Volume': stock_data['current_vol'],
                            'AvgVol': stock_data['avg_vol'],
                            **metrics
                        }
                        all_data.append(row_data)
            
            progress_bar.empty()
            
            if all_data:
                # Create DataFrame
                df = pd.DataFrame(all_data)
                df = compute_score(df)
                
                # Sort by score
                df = df.sort_values('Score', ascending=False)
                
                # Display summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Stocks", len(df))
                
                with col2:
                    high_alerts = len(df[df['Score'] > alert_threshold])
                    st.metric("High Alerts", high_alerts)
                
                with col3:
                    avg_score = df['Score'].mean()
                    st.metric("Avg Score", f"{avg_score:.2f}")
                
                with col4:
                    st.metric("Last Update", datetime.now().strftime("%H:%M:%S"))
                
                # Alert section
                high_alert_stocks = df[df['Score'] > alert_threshold]
                if not high_alert_stocks.empty:
                    st.markdown("### 🚨 HIGH ALERT STOCKS")
                    
                    # Check for new alerts
                    current_alerts = set(high_alert_stocks['Ticker'].tolist())
                    new_alerts = current_alerts - st.session_state.last_alerts
                    
                    if new_alerts and sound_alerts:
                        for ticker in new_alerts:
                            st.warning(f"🚨 NEW BREAKOUT ALERT: {ticker}")
                            play_alert()
                    
                    st.session_state.last_alerts = current_alerts
                    
                    for _, row in high_alert_stocks.iterrows():
                        st.markdown(f"""
                        <div class="alert-high">
                            🔥 {row['Ticker']} - Score: {row['Score']:.2f} - ${row['Price']:.2f} - {row['Alert']}
                        </div>
                        """, unsafe_allow_html=True)
                
                # Main data table
                st.markdown("### 📊 Stock Data")
                
                # Format DataFrame for display
                display_df = df.copy()
                display_df['Price'] = display_df['Price'].round(2)
                display_df['Score'] = display_df['Score'].round(2)
                display_df['PriceVsRes'] = display_df['PriceVsRes'].round(3)
                display_df['PriceVsMA50'] = display_df['PriceVsMA50'].round(3)
                display_df['RelVol'] = display_df['RelVol'].round(2)
                display_df['Sentiment'] = display_df['Sentiment'].round(3)
                
                # Color code the table
                def color_score(val):
                    if val > alert_threshold:
                        return 'background-color: #ff4b4b; color: white'
                    elif val > 1.0:
                        return 'background-color: #ffa500; color: white'
                    else:
                        return 'background-color: #00cc00; color: white'
                
                styled_df = display_df.style.applymap(color_score, subset=['Score'])
                st.dataframe(styled_df, use_container_width=True)
                
                # Charts section
                if len(df) > 1:
                    st.markdown("### 📈 Visualizations")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        # Score distribution
                        fig_hist = px.histogram(
                            df, 
                            x='Score', 
                            title='Score Distribution',
                            nbins=20
                        )
                        st.plotly_chart(fig_hist, use_container_width=True)
                    
                    with col2:
                        # Score vs Price scatter
                        fig_scatter = px.scatter(
                            df, 
                            x='Price', 
                            y='Score', 
                            text='Ticker',
                            title='Score vs Price'
                        )
                        fig_scatter.update_traces(textposition="top center")
                        st.plotly_chart(fig_scatter, use_container_width=True)
            
            else:
                st.error("No data available. Please check your API keys and ticker symbols.")
        
        # Auto-refresh logic
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()
        else:
            break

if __name__ == "__main__":
    main()
