import os
from dotenv import load_dotenv
from sec_edgar_downloader import Downloader

load_dotenv()

def download_10k(ticker: str) -> str:
    print(f"Starting download for {ticker}...")
    dl = Downloader("FinAgent", "ramondario1216@gmail.com", "data")
    print("Downloader initialized...")
    dl.get("10-K", ticker, limit=1)
    print("Download complete. Checking files...")
    
    filing_dir = f"data/sec-edgar-filings/{ticker}/10-K"
    print(f"Looking in: {filing_dir}")
    
    if not os.path.exists(filing_dir):
        return f"No 10-K found for {ticker}"
    
    folders = os.listdir(filing_dir)
    print(f"Folders found: {folders}")
    
    if not folders:
        return f"No folders found for {ticker}"
    
    filing_path = os.path.join(filing_dir, folders[0])
    files = os.listdir(filing_path)
    print(f"Files found: {files}")
    
    for file in files:
        if file.endswith(".txt") or file.endswith(".htm"):
            return os.path.join(filing_path, file)
    
    return f"Could not locate filing document for {ticker}"

if __name__ == "__main__":
    ticker = "AAPL"
    result = download_10k(ticker)
    print(f"Result: {result}")