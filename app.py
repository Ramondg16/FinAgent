import streamlit as st
import os
from dotenv import load_dotenv
from pathlib import Path
from agents.market_agent import get_market_data, format_market_data
from agents.sentiment_agent import analyze_sentiment
from utils.parser import extract_risk_factors
from agents.research_agent import generate_investment_brief
from sec_edgar_downloader import Downloader

if "OPENAI_API_KEY" in st.secrets:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]

load_dotenv(Path(__file__).parent / ".env")

st.set_page_config(
    page_title="Financial Research Assistant",
    page_icon="📊",
    layout="wide"
)

st.title("Financial Research Assistant")
st.subheader("Automated insights from SEC filings and market data")
st.markdown("---")

ticker = st.text_input(
    "Enter a stock ticker",
    placeholder="e.g. AAPL, MSFT, JPM",
    max_chars=10
).upper().strip()

analyze_button = st.button("Generate Investment Brief", type="primary")

if analyze_button and ticker:
    
    # Download 10-K
    with st.spinner(f"Downloading {ticker} 10-K from SEC EDGAR..."):
        try:
            # Check if already downloaded
            filing_dir = f"data/sec-edgar-filings/{ticker}/10-K"
            
            if not os.path.exists(filing_dir) or not os.listdir(filing_dir):
                dl = Downloader("FinAgent", "ramondario1216@gmail.com", "data")
                dl.get("10-K", ticker, limit=1)
            
            folders = os.listdir(filing_dir)
            if not folders:
                st.error(f"No 10-K found for {ticker}")
                st.stop()
                
            filing_path = os.path.join(filing_dir, folders[0], "full-submission.txt")
            
            if not os.path.exists(filing_path):
                st.error(f"Filing file not found for {ticker}")
                st.stop()
                
            st.success(f"10-K filing retrieved for {ticker}")
        except Exception as e:
            st.error(f"Could not retrieve 10-K for {ticker}. SEC EDGAR may be rate limiting — wait 30 seconds and try again. Error: {e}")
            st.stop()
    
    # Market Data
    with st.spinner("Fetching live market data..."):
        market_data = get_market_data(ticker)
        st.success("Live market data fetched")
    
    # Display market metrics
    st.markdown("### Market Overview")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Current Price", f"${market_data['current_price']}")
    col2.metric("Market Cap", f"${market_data['market_cap']/1_000_000_000_000:.2f}T" 
                if market_data['market_cap'] != 'N/A' else "N/A")
    col3.metric("P/E Ratio", round(market_data['pe_ratio'], 2) 
                if market_data['pe_ratio'] != 'N/A' else "N/A")
    col4.metric("Analyst Rating", market_data['analyst_rating'].upper() 
                if market_data['analyst_rating'] != 'N/A' else "N/A")
    
    col5, col6, col7, col8 = st.columns(4)
    col5.metric("52W High", f"${market_data['52_week_high']}")
    col6.metric("52W Low", f"${market_data['52_week_low']}")
    col7.metric("Revenue", f"${market_data['revenue']/1_000_000_000:.1f}B" 
                if market_data['revenue'] != 'N/A' else "N/A")
    col8.metric("Profit Margin", f"{round(market_data['profit_margin']*100, 2)}%" 
                if market_data['profit_margin'] != 'N/A' else "N/A")
    
    st.markdown("---")
    
    # Sentiment Analysis
    with st.spinner("Running FinBERT sentiment analysis on Risk Factors..."):
        risk_text = extract_risk_factors(filing_path)
        sentiment = analyze_sentiment(risk_text)
        st.success("FinBERT sentiment analysis complete")
    
    st.markdown("### Risk Factors Sentiment Analysis")
    col1, col2, col3, col4 = st.columns(4)
    
    sentiment_color = "🟢" if sentiment['overall'] == 'positive' else "🔴" if sentiment['overall'] == 'negative' else "🟡"
    col1.metric("Overall Sentiment", f"{sentiment_color} {sentiment['overall'].upper()}")
    col2.metric("Positive Score", sentiment['scores']['positive'])
    col3.metric("Negative Score", sentiment['scores']['negative'])
    col4.metric("Neutral Score", sentiment['scores']['neutral'])
    
    st.markdown("---")
    
    # Generate Brief
    with st.spinner("Generating investment brief..."):
        brief = generate_investment_brief(ticker, filing_path)
        st.success("Investment brief generated")
    
    st.markdown("### Investment Brief")
    st.markdown(brief)
    
    st.markdown("---")
    st.caption("FinAgent — Powered by SEC EDGAR, FinBERT, and GPT-4o-mini")

elif analyze_button and not ticker:
    st.warning("Please enter a ticker symbol.")