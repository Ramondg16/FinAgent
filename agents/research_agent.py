from openai import OpenAI
from dotenv import load_dotenv
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from agents.market_agent import get_market_data, format_market_data
from agents.sentiment_agent import analyze_sentiment
from utils.parser import extract_risk_factors

from pathlib import Path
load_dotenv(Path(__file__).parent.parent / ".env")

client = OpenAI()

def generate_investment_brief(ticker: str, filing_path: str) -> str:
    """Generates a full investment brief for a Financial Advisor."""
    
    print(f"\nGenerating investment brief for {ticker}...")
    
    # Step 1: Get market data
    print("Step 1/3: Fetching market data...")
    market_data = get_market_data(ticker)
    market_summary = format_market_data(market_data)
    
    # Step 2: Extract and analyze risk factors
    print("Step 2/3: Analyzing risk factors...")
    risk_text = extract_risk_factors(filing_path)
    sentiment = analyze_sentiment(risk_text)
    
    # Step 3: Synthesize with LLM
    print("Step 3/3: Generating investment brief...")
    
    prompt = f"""
You are a senior financial analyst at a top wealth management firm preparing a briefing for a Financial Advisor and their client.

Using the following data, generate a concise, professional investment brief that includes:
1. Company Snapshot
2. Key Risk Assessment (based on the 10-K Risk Factors sentiment analysis)
3. Market Position
4. Investment Considerations for a wealth management client
5. Overall Recommendation

MARKET DATA:
{market_summary}

RISK FACTORS SENTIMENT ANALYSIS (FinBERT):
Overall Sentiment: {sentiment['overall'].upper()}
Positive Score: {sentiment['scores']['positive']}
Negative Score: {sentiment['scores']['negative']}
Neutral Score:  {sentiment['scores']['neutral']}
Chunks Analyzed: {sentiment['chunks_analyzed']}

Write in a professional but accessible tone suitable for a Financial Advisor presenting to a client.
Keep the brief under 500 words.
"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a senior financial analyst at a wealth management firm."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    ticker = "AAPL"
    filing_path = "data/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt"
    brief = generate_investment_brief(ticker, filing_path)
    print("\n" + "="*60)
    print("FINAGENT INVESTMENT BRIEF")
    print("="*60)
    print(brief)