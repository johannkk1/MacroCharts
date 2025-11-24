"""
Asset Insights Module
Provides comprehensive financial analysis for assets including:
- Current price and volume
- Technical indicators (RSI, MACD, Moving Averages)
- Trend analysis
- Support/Resistance levels
- Performance metrics
- News headlines
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_rsi(prices, period=14):
    """Calculate Relative Strength Index"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1] if not rsi.empty else 50

def calculate_macd(prices):
    """Calculate MACD (Moving Average Convergence Divergence)"""
    exp1 = prices.ewm(span=12, adjust=False).mean()
    exp2 = prices.ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return {
        'value': float(macd.iloc[-1]) if not macd.empty else 0,
        'signal': float(signal.iloc[-1]) if not signal.empty else 0
    }

def analyze_trend(df):
    """Analyze price trend based on moving averages and recent price action"""
    if df.empty or len(df) < 50:
        return "neutral"
    
    current_price = df['Close'].iloc[-1]
    sma_20 = df['Close'].rolling(window=20).mean().iloc[-1]
    sma_50 = df['Close'].rolling(window=50).mean().iloc[-1]
    
    # Price above both MAs = bullish
    if current_price > sma_20 and current_price > sma_50 and sma_20 > sma_50:
        return "bullish"
    # Price below both MAs = bearish
    elif current_price < sma_20 and current_price < sma_50 and sma_20 < sma_50:
        return "bearish"
    else:
        return "neutral"

def get_support_resistance(df):
    """Calculate support and resistance levels"""
    if df.empty or len(df) < 20:
        return {"support": [], "resistance": []}
    
    recent_high = df['High'].tail(20).max()
    recent_low = df['Low'].tail(20).min()
    current_price = df['Close'].iloc[-1]
    
    # Simple support/resistance based on recent highs/lows
    resistance = [recent_high]
    support = [recent_low]
    
    return {
        "support": [float(s) for s in support],
        "resistance": [float(r) for r in resistance]
    }

def get_asset_insights(ticker, period='1mo'):
    """
    Get comprehensive insights for an asset
    
    Args:
        ticker: Asset ticker symbol
        period: Time period for analysis (default: 1mo for faster loading)
    
    Returns:
        Dictionary with asset insights
    """
    try:
        # Fetch asset data
        asset = yf.Ticker(ticker)
        df = asset.history(period=period)
        
        if df.empty:
            raise ValueError(f"No data available for {ticker}")
        
        # Get current info
        info = asset.info
        current_price = df['Close'].iloc[-1]
        prev_close = df['Close'].iloc[-2] if len(df) > 1 else current_price
        change_24h = ((current_price - prev_close) / prev_close) * 100
        
        # Calculate technical indicators
        rsi = calculate_rsi(df['Close'])
        macd = calculate_macd(df['Close'])
        sma_50 = df['Close'].rolling(window=50).mean().iloc[-1] if len(df) >= 50 else current_price
        sma_200 = df['Close'].rolling(window=200).mean().iloc[-1] if len(df) >= 200 else current_price
        
        # Analyze trend
        trend = analyze_trend(df)
        
        # Support/Resistance
        levels = get_support_resistance(df)
        
        # Performance metrics
        performance = {}
        if len(df) >= 1:
            performance['1d'] = change_24h
        if len(df) >= 7:
            week_ago = df['Close'].iloc[-7]
            performance['1w'] = ((current_price - week_ago) / week_ago) * 100
        if len(df) >= 30:
            month_ago = df['Close'].iloc[-30]
            performance['1m'] = ((current_price - month_ago) / month_ago) * 100
        if len(df) >= 90:
            three_months_ago = df['Close'].iloc[-90]
            performance['3m'] = ((current_price - three_months_ago) / three_months_ago) * 100
        
        # Get news
        news = []
        try:
            # Try to get news from yfinance
            news_data = asset.news
            if news_data and isinstance(news_data, list):
                for item in news_data[:5]:  # Get top 5 news items
                    if isinstance(item, dict):
                        news.append({
                            'title': item.get('title', ''),
                            'publisher': item.get('publisher', ''),
                            'link': item.get('link', ''),
                            'published': item.get('providerPublishTime', 0)
                        })
            print(f"Fetched {len(news)} news items for {ticker}")
        except Exception as e:
            print(f"Could not fetch news for {ticker}: {e}")
            news = []
        
        # Build response
        insights = {
            'ticker': ticker,
            'name': info.get('longName', ticker),
            'current_price': float(current_price),
            'currency': info.get('currency', 'USD'),
            'change_24h': float(change_24h),
            'volume_24h': float(df['Volume'].iloc[-1]) if 'Volume' in df.columns else 0,
            'market_cap': info.get('marketCap', 0),
            'trend': trend,
            'technical_indicators': {
                'rsi': float(rsi),
                'macd': macd,
                'sma_50': float(sma_50),
                'sma_200': float(sma_200)
            },
            'support_resistance': levels,
            'performance': performance,
            'news': news,
            'last_updated': datetime.now().isoformat()
        }
        
        return insights
        
    except Exception as e:
        raise Exception(f"Error fetching insights for {ticker}: {str(e)}")
