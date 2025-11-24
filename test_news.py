import news_data
import json

print("Testing News Fetching...")
try:
    result = news_data.get_news('US')
    print(f"News Items: {len(result['news'])}")
    print(f"Summary: {result['summary']['verdict']}")
    if len(result['news']) > 0:
        print(f"First Item: {result['news'][0]['title']}")
except Exception as e:
    print(f"Error: {e}")
