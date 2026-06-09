from transformers import BertTokenizer, BertForSequenceClassification
import torch
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.parser import extract_risk_factors

def chunk_text(text: str, chunk_size: int = 512) -> list:
    """Splits text into chunks of roughly chunk_size characters."""
    words = text.split()
    chunks = []
    current_chunk = []
    current_length = 0
    
    for word in words:
        current_length += len(word) + 1
        current_chunk.append(word)
        if current_length >= chunk_size:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_length = 0
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks

def analyze_sentiment(text: str) -> dict:
    """Runs FinBERT sentiment analysis on text."""
    print("Loading FinBERT model...")
    tokenizer = BertTokenizer.from_pretrained("ProsusAI/finbert")
    model = BertForSequenceClassification.from_pretrained("ProsusAI/finbert")
    model.eval()
    
    chunks = chunk_text(text)
    print(f"Analyzing {len(chunks)} chunks...")
    
    scores = {"positive": 0, "negative": 0, "neutral": 0}
    
    for i, chunk in enumerate(chunks[:20]):  # Limit to 20 chunks for speed
        inputs = tokenizer(
            chunk,
            return_tensors="pt",
            truncation=True,
            max_length=512,
            padding=True
        )
        
        with torch.no_grad():
            outputs = model(**inputs)
        
        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        labels = ["positive", "negative", "neutral"]
        
        for j, label in enumerate(labels):
            scores[label] += probs[0][j].item()
    
    # Average the scores
    total_chunks = min(len(chunks), 20)
    for key in scores:
        scores[key] = round(scores[key] / total_chunks, 4)
    
    # Determine overall sentiment
    overall = max(scores, key=scores.get)
    
    return {
        "scores": scores,
        "overall": overall,
        "chunks_analyzed": total_chunks
    }

if __name__ == "__main__":
    filepath = "data/sec-edgar-filings/AAPL/10-K/0000320193-25-000079/full-submission.txt"
    print("Extracting risk factors...")
    text = extract_risk_factors(filepath)
    print(f"Running FinBERT on {len(text)} characters...")
    result = analyze_sentiment(text)
    print("\n--- SENTIMENT RESULTS ---")
    print(f"Overall: {result['overall'].upper()}")
    print(f"Positive: {result['scores']['positive']}")
    print(f"Negative: {result['scores']['negative']}")
    print(f"Neutral:  {result['scores']['neutral']}")
    print(f"Chunks analyzed: {result['chunks_analyzed']}")