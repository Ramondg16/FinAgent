# FinAgent — Autonomous Wealth Research Assistant

An agentic financial research tool that autonomously pulls SEC EDGAR 10-K filings, runs FinBERT sentiment analysis on risk factors, fetches live market data, and synthesizes a professional investment brief for Financial Advisors.

Built to demonstrate applied NLP, agentic systems, and generative AI in a wealth management context.

---

## What It Does

Enter any stock ticker and FinAgent autonomously:

1. **Pulls the latest 10-K filing** directly from SEC EDGAR
2. **Extracts the Risk Factors section** from the raw filing document
3. **Runs FinBERT sentiment analysis** — a financial domain NLP model — across the risk factors text
4. **Fetches live market data** via Yahoo Finance (price, market cap, P/E, analyst rating, revenue, margins)
5. **Generates a structured investment brief** using GPT-4o-mini, synthesizing all of the above into a document a Financial Advisor could present to a client

---

## Tech Stack

| Component | Technology |
| Agentic Orchestration | LangChain |
| Financial NLP | FinBERT (ProsusAI) |
| SEC Filings | SEC EDGAR Downloader |
| Market Data | Yahoo Finance (yfinance) |
| LLM | GPT-4o-mini (OpenAI) |
| Frontend | Streamlit |
| Language | Python |

---

## Architecture
User Input (Ticker)
│
▼
SEC EDGAR Agent ──► 10-K Filing
│
▼
Parser ──► Risk Factors Section
│
▼
FinBERT Sentiment Agent ──► Sentiment Scores
│
▼
Yahoo Finance Agent ──► Live Market Data
│
▼
Research Agent (GPT-4o-mini) ──► Investment Brief
│
▼
Streamlit UI

---

## Sample Output

**Ticker: AAPL**
- Overall Risk Sentiment: NEGATIVE (57.8%)
- Current Price: $301.54 | Market Cap: $4.43T
- Analyst Rating: BUY
- Generated a 500-word investment brief covering company snapshot, risk assessment, market position, and recommendation

---

## Setup

```bash
git clone https://github.com/Ramondg16/FinAgent.git
cd FinAgent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Add your OpenAI API key to a `.env` file:
OPENAI_API_KEY=your_key_here
Run locally:

```bash
streamlit run app.py
```

---

## Why I Built This

Financial Advisors at wealth management firms deal with enormous volumes of SEC filings, research reports, and market data. FinAgent automates the research pipeline — pulling, analyzing, and synthesizing that information into actionable briefs. This directly mirrors the kind of AI-driven decision support that enterprise wealth management teams are building today.
