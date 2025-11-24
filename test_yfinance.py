import yfinance as yf
import sys

print("Testing yfinance news fetching...")

ticker = yf.Ticker('AAPL')
print(f"Ticker object created: {ticker}")

try:
    news = ticker.news
    print(f"News fetched: {len(news)} items")
    
    if news:
        item = news[0]
        print(f"\nFirst item structure:")
        print(f"Keys: {item.keys()}")
        
        content = item.get('content', {})
        print(f"\nContent keys: {content.keys() if content else 'No content'}")
        
        if content:
            print(f"Title: {content.get('title', 'NO TITLE')}")
            print(f"Summary: {content.get('summary', 'NO SUMMARY')}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
