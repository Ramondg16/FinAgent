import yfinance as yf

def get_market_data(ticker: str) -> dict:
    """Fetches live market data for a given ticker."""
    print(f"Fetching market data for {ticker}...")
    
    stock = yf.Ticker(ticker)
    info = stock.info
    
    data = {
        "ticker": ticker,
        "company_name": info.get("longName", "N/A"),
        "current_price": info.get("currentPrice", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "52_week_high": info.get("fiftyTwoWeekHigh", "N/A"),
        "52_week_low": info.get("fiftyTwoWeekLow", "N/A"),
        "revenue": info.get("totalRevenue", "N/A"),
        "profit_margin": info.get("profitMargins", "N/A"),
        "debt_to_equity": info.get("debtToEquity", "N/A"),
        "analyst_rating": info.get("recommendationKey", "N/A"),
        "sector": info.get("sector", "N/A"),
        "industry": info.get("industry", "N/A"),
        "summary": info.get("longBusinessSummary", "N/A")[:500]
    }
    
    return data

def format_market_data(data: dict) -> str:
    """Formats market data into readable string for LLM."""
    
    def format_large_number(n):
        if n == "N/A":
            return "N/A"
        if n >= 1_000_000_000_000:
            return f"${n/1_000_000_000_000:.2f}T"
        if n >= 1_000_000_000:
            return f"${n/1_000_000_000:.2f}B"
        if n >= 1_000_000:
            return f"${n/1_000_000:.2f}M"
        return f"${n:,.2f}"
    
    return f"""
MARKET DATA FOR {data['ticker']} - {data['company_name']}
Current Price:    ${data['current_price']}
Market Cap:       {format_large_number(data['market_cap'])}
P/E Ratio:        {data['pe_ratio']}
52-Week High:     ${data['52_week_high']}
52-Week Low:      ${data['52_week_low']}
Revenue:          {format_large_number(data['revenue'])}
Profit Margin:    {round(data['profit_margin'] * 100, 2) if data['profit_margin'] != 'N/A' else 'N/A'}%
Debt/Equity:      {data['debt_to_equity']}
Analyst Rating:   {data['analyst_rating'].upper()}
Sector:           {data['sector']}
"""

if __name__ == "__main__":
    ticker = "AAPL"
    data = get_market_data(ticker)
    print(format_market_data(data))