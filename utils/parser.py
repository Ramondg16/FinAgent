import re

def extract_risk_factors(filepath: str) -> str:
    print("Reading filing...")
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    print(f"File size: {len(content)} characters")
    content = re.sub(r'<[^>]+>', ' ', content)
    content = re.sub(r'\s+', ' ', content).strip()
    
    print("Searching for Risk Factors section...")
    
    # Find all matches and take the third one - actual content
    matches = [m for m in re.finditer(r'risk factor', content, re.IGNORECASE)]
    
    if len(matches) < 3:
        return "Risk Factors section not found"
    
    # Match 3 is the real content (index 2)
    start = matches[2].start()
    
    # End at match 4
    end = matches[3].start()
    
    risk_text = content[start:end]
    
    print(f"Risk Factors extracted: {len(risk_text)} characters")
    return risk_text

if __name__ == "__main__":
    filepath = "data/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt"
    text = extract_risk_factors(filepath)
    print("\n--- FIRST 500 CHARACTERS ---")
    print(text[:500])
    print("\n--- LAST 500 CHARACTERS ---")
    print(text[-500:])
