import yfinance as yf
from collections import Counter
import feedparser
import requests
from datetime import datetime, timedelta
import time
import random
import re

# Data Extraction Utilities
def extract_numbers_from_text(text):
    """Extract percentages and basis points from text"""
    import re
    numbers = {
        'percentages': [],
        'basis_points': [],
        'rates': []
    }
    
    # Extract percentages (e.g., "3.2%", "fell to 2.1%")
    pct_pattern = r'(\d+\.?\d*)\s*%'
    percentages = re.findall(pct_pattern, text)
    numbers['percentages'] = [float(p) for p in percentages]
    
    # Extract basis points (e.g., "25bps", "50 basis points")
    bp_pattern = r'(\d+)\s*(?:bps|basis\s+points?)'
    bps = re.findall(bp_pattern, text, re.IGNORECASE)
    numbers['basis_points'] = [int(b) for b in bps]
    
    # Extract interest rates (e.g., "5.25%", "raised to 4.5%")
    rate_pattern = r'(?:rate|yield)(?:\s+of|\s+to|\s+at)?\s+(\d+\.?\d*)\s*%'
    rates = re.findall(rate_pattern, text, re.IGNORECASE)
    numbers['rates'] = [float(r) for r in rates]
    
    return numbers

def extract_policy_actions(news_items):
    """Extract specific central bank actions from news"""
    actions = []
    for item in news_items:
        text = (item['title'] + ' ' + item.get('summary', '')).lower()
        
        # Enhanced rate change detection
        if any(phrase in text for phrase in ['rate cut', 'cut rates', 'cuts rates', 'lowers rates', 'reduces rates']):
            nums = extract_numbers_from_text(text)
            if nums['basis_points']:
                bps = nums['basis_points'][0]
                actions.append(f"Rate cut ({bps}bps)")
            elif nums['percentages']:
                pct = nums['percentages'][0]
                actions.append(f"Rate cut ({pct}%)")
            else:
                # Try to find explicit mentions
                import re
                half_match = re.search(r'half.point|0\.5', text)
                quarter_match = re.search(r'quarter.point|0\.25', text)
                if half_match:
                    actions.append("Rate cut (50bps)")
                elif quarter_match:
                    actions.append("Rate cut (25bps)")
                else:
                    actions.append("Rate cut announced")
                    
        elif any(phrase in text for phrase in ['rate hike', 'raised rates', 'raises rates', 'increase rates', 'increases rates', 'lifts rates']):
            nums = extract_numbers_from_text(text)
            if nums['basis_points']:
                bps = nums['basis_points'][0]
                actions.append(f"Rate hike ({bps}bps)")
            elif nums['percentages']:
                pct = nums['percentages'][0]
                actions.append(f"Rate hike ({pct}%)")
            else:
                # Try to find explicit mentions
                import re
                half_match = re.search(r'half.point|0\.5', text)
                quarter_match = re.search(r'quarter.point|0\.25', text)
                if half_match:
                    actions.append("Rate hike (50bps)")
                elif quarter_match:
                    actions.append("Rate hike (25bps)")
                else:
                    actions.append("Rate hike announced")
        
        # QE/QT
        if 'quantitative easing' in text or ' qe ' in text or 'bond buying' in text:
            actions.append("Quantitative Easing program")
        if 'quantitative tightening' in text or ' qt ' in text or 'balance sheet reduction' in text:
            actions.append("Quantitative Tightening active")
            
    return actions

def generate_contextual_insight(metric_name, score, news_items, country_code):
    """Generate intelligent, context-aware market implications - INVESTOR ACTIONABLE"""
    all_text = ' '.join([item['title'] + ' ' + item.get('summary', '') for item in news_items[:10]]).lower()
    numbers = extract_numbers_from_text(all_text)
    
    # Base context on actual data
    if metric_name == 'Monetary Policy':
        if score > 65:
            if 'cut' in all_text or 'dovish' in all_text:
                return f"**Dovish pivot** in {country_code} supports **risk assets**. Implications: ✅ Growth equities, real estate, EM debt benefit from easier financial conditions. Watch: Duration risk if inflation reaccelerates."
            return f"**Accommodative stance** in {country_code} maintains liquidity. Implications: ✅ Credit spreads tight, equity multiples supported. Risk: Policy error if growth slows."
        elif score < 40:
            return f"**Hawkish policy** in {country_code} tightening financial conditions. Implications: ⚠️ Defensive positioning warranted. Favor: Value over growth, quality credit, short duration. Pressure on: High-multiple tech, leveraged names."
        return f"**Neutral policy** in {country_code} - data-dependent approach. Implications: 🔄 Tactical rotations based on incoming data. Monitor: CPI prints, labor market, Fed communications."
    
    elif metric_name == 'Inflation & Growth':
        if score > 65:
            return f"**Goldilocks scenario** in {country_code} - robust growth with controlled inflation. Implications: ✅ Cyclicals, banks, industrials outperform. Stable inflation supports: Corporate margins, consumer spending power."
        elif score < 40:
            if 'recession' in all_text or 'contraction' in all_text:
                return f"**Recession risk** elevated in {country_code}. Implications: 🛡️ Flight to quality underway. Favor: Utilities, staples, healthcare, long-duration Treasuries. Avoid: Cyclicals, discretionary, small caps."
            return f"**Stagflation concerns** in {country_code} - weak growth + sticky inflation. Implications: ⚠️ Challenging for equities. Consider: Commodities, TIPS, value stocks. Avoid: Long-duration growth."
        return f"**Mixed economic signals** in {country_code}. Implications: 🎯 Sector-specific approach. Monitor: Leading indicators (PMI, yield curve) for directional clarity."
    
    elif metric_name == 'Political Risk':
        if score < 40:
            if 'tariff' in all_text or 'trade war' in all_text:
                return f"**Trade policy uncertainty** in {country_code} elevates risk premiums. Implications: ⚠️ Supply chain disruptions possible. Favor: Domestic-oriented names, hedged multinationals. Monitor: Negotiation developments."
            return f"**Political instability** in {country_code} increases volatility. Implications: 💰 Risk premium in sovereign spreads. Favor: Quality over beta, gold, defensive sectors."
        return f"**Stable political environment** in {country_code} supports investment. Implications: ✅ Regulatory clarity enables long-term capex. Infrastructure, regulated utilities benefit."
    
    elif metric_name == 'Currency Strength':
        if score > 60:
            return f"**Strong {country_code} currency** reduces import costs but hurts exporters. Implications: ✅ Importers, retailers, travel/hospitality benefit. ⚠️ Multinationals with high foreign revenue exposure face headwinds."
        elif score < 40:
            return f"**Weak {country_code} currency** boosts export competitiveness. Implications: ✅ Exporters, manufacturers, tourism operators gain. ⚠️ Import-dependent sectors (energy, autos) face margin pressure."
        return f"**Stable {country_code} FX** provides predictability. Implications: 🔄 Focus on fundamentals vs currency swings. Natural hedges valuable."
    
    elif metric_name == 'Investor Sentiment':
        if score > 65:
            return f"**Risk-on environment** in {country_code} markets. Implications: 📈 Strong momentum in growth/cyclicals. Caution: Elevated sentiment can signal crowding - watch for mean reversion signals (VIX spike, breadth divergence)."
        elif score < 40:
            return f"**Risk-off positioning** in {country_code}. Implications: 💎 Contrarian opportunities in oversold quality names. Defensive sectors (utilities, staples) outperforming. Entry points emerging."
        return f"**Neutral sentiment** in {country_code}. Implications: 📊 Balanced positioning. Use fundamental analysis vs momentum. Stock-picking environment."
    
    elif metric_name == 'Fiscal Health':
        if score < 40:
            return f"**Fiscal concerns** in {country_code} pressuring sovereign outlook. Implications: ⚠️ Sovereign CDS widening risk. Austerity measures may drag growth. Consider: Foreign diversification, inflation hedges."
        return f"**Solid fiscal position** in {country_code} provides policy flexibility. Implications: ✅ Countercyclical capacity available if downturn materializes. Infrastructure investment sustainable."
    
    elif metric_name == 'External Vulnerability':
        if score < 40:
            return f"**High external vulnerability** in {country_code} amplifies global shock transmission. Implications: ⚠️ Sanctions/tariff exposure elevated. Diversify: Less correlated regions, maintain tail-risk hedges (options, gold)."
        return f"**Low external vulnerability** in {country_code} provides insulation. Implications: ✅ Domestic assets less correlated with global volatility events. Resilient to external shocks."
    
    # Fallback
    return f"Score based on {len(news_items)} news sources. {country_code} {metric_name.lower()} at {score:.0f}/100."

# Mapping countries to representative tickers to fetch news from
COUNTRY_TICKERS = {
    'US': ['^GSPC', '^DJI', '^IXIC', 'AAPL', 'MSFT', 'GOOGL', 'NVDA', 'TSLA', 'JPM'],
    'DE': ['^GDAXI', 'SIE.DE', 'VOW3.DE', 'ALV.DE', 'BMW.DE', 'DTE.DE', 'SAP.DE'],
    'UK': ['^FTSE', 'HSBC', 'BP', 'SHEL', 'ULVR.L', 'AZN.L', 'GSK.L'],
    'CN': ['000001.SS', '^HSI', 'BABA', 'TCEHY', 'JD', 'BIDU', 'PDD'],
    'JP': ['^N225', '7203.T', '6758.T', '9984.T', '7974.T', '8035.T'],
    'Global': ['GC=F', 'CL=F', 'EURUSD=X', 'BTC-USD', '^GSPC', '^STOXX50E']
}

KEYWORDS = {
    'Economy': ['inflation', 'gdp', 'rate', 'fed', 'central bank', 'jobs', 'unemployment', 'cpi', 'ppi', 'economy', 'recession', 'growth', 'debt', 'deficit', 'spending', 'tax', 'policy', 'trade', 'tariff', 'export', 'import'],
    'Finance': ['stock', 'market', 'bond', 'yield', 'currency', 'forex', 'dollar', 'euro', 'yen', 'yuan', 'gold', 'oil', 'crypto', 'bitcoin', 'earnings', 'revenue', 'profit', 'ipo', 'merger', 'acquisition', 'dividend', 'buyback'],
    'Politics': ['election', 'vote', 'president', 'minister', 'parliament', 'congress', 'senate', 'law', 'bill', 'regulation', 'sanction', 'geopolitics', 'war', 'conflict', 'treaty', 'agreement', 'diplomacy', 'campaign', 'scandal', 'protest'],
    'Technology': ['tech', 'ai', 'artificial intelligence', 'chip', 'semiconductor', 'software', 'cloud', 'cyber', 'internet', 'mobile', 'app', 'startup', 'venture', 'innovation', 'robotics', 'automation', 'data', 'privacy'],
    'Energy': ['energy', 'oil', 'gas', 'renewable', 'solar', 'wind', 'nuclear', 'power', 'grid', 'utility', 'climate', 'carbon', 'emission', 'green', 'battery', 'ev', 'electric vehicle'],
    'Bullish': ['surge', 'jump', 'rally', 'soar', 'gain', 'record', 'high', 'beat', 'exceed', 'strong', 'growth', 'positive', 'optimism', 'bull', 'buy', 'upgrade', 'profit'],
    'Bearish': ['plunge', 'drop', 'fall', 'sink', 'loss', 'low', 'miss', 'weak', 'decline', 'negative', 'pessimism', 'bear', 'sell', 'downgrade', 'crash', 'crisis', 'recession', 'inflation', 'fear', 'panic']
}

# RSS Feeds for additional sources
RSS_FEEDS = {
    'US': [
        'http://feeds.marketwatch.com/marketwatch/topstories/',
        'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=10000664', # CNBC Finance
        'https://feeds.bbci.co.uk/news/business/rss.xml',
        'http://feeds.reuters.com/reuters/businessNews'
    ],
    'DE': [
        'https://www.tagesschau.de/wirtschaft/index~rss2.xml',
        'https://www.spiegel.de/wirtschaft/index.rss'
    ],
    'UK': [
        'http://feeds.bbci.co.uk/news/business/rss.xml',
        'https://www.theguardian.com/uk/business/rss'
    ],
    'CN': [
        'http://www.chinadaily.com.cn/rss/bizchina_rss.xml'
    ],
    'JP': [
        'https://www3.nhk.or.jp/rss/news/cat6.xml' # NHK Business (Japanese, might need translation or specific handling, sticking to English sources for now if possible)
    ],
    'Global': [
        'https://feeds.bloomberg.com/markets/news.rss',
        'https://www.economist.com/finance-and-economics/rss.xml'
    ]
}

# RSS Feeds - Using Google News for broad, search-based coverage
# We will generate these dynamically in fetch_rss_news based on the country
import requests

# RSS Feeds - Using Google News for broad, search-based coverage
# We will generate these dynamically in fetch_rss_news based on the country
BASE_RSS_URL = "https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en"

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def analyze_news_item(title):
    """
    Analyze a news title to determine category, sentiment, and score.
    """
    if not title:
        return "General", "Neutral", 0, 0
        
    title_lower = title.lower()
    
    # Determine Category
    scores = {cat: 0 for cat in ['Economy', 'Finance', 'Politics', 'Technology', 'Energy']}
    
    # Keywords must be defined globally or passed in. Assuming KEYWORDS is global.
    # We need to make sure KEYWORDS is defined. It is defined in the file.
    
    for cat, keywords in KEYWORDS.items():
        if cat in ['Bullish', 'Bearish']: continue
        for k in keywords:
            if k in title_lower:
                scores[cat] += 1
                
    # Default to Finance if related ticker is present (handled in caller), but here we guess
    best_category = max(scores, key=scores.get)
    if scores[best_category] == 0:
        best_category = "General"
        
    # Determine Sentiment
    sentiment = "Neutral"
    bull_score = sum(1 for k in KEYWORDS['Bullish'] if k in title_lower)
    bear_score = sum(1 for k in KEYWORDS['Bearish'] if k in title_lower)
    
    sentiment_score = 0 # -1 to 1 scale roughly
    
    if bull_score > bear_score:
        sentiment = "Positive"
        sentiment_score = 1
    elif bear_score > bull_score:
        sentiment = "Negative"
        sentiment_score = -1
        
    # Calculate Impact Score (0-10)
    total_keywords = sum(scores.values()) + bull_score + bear_score
    impact_score = min(10, total_keywords * 2 + random.randint(1, 4))
    if impact_score < 3: impact_score = 3 # Minimum relevance
    
    return best_category, sentiment, impact_score, sentiment_score

def generate_chain_reaction(category, sentiment, title):
    """
    Generates a logical chain reaction of market events based on category and sentiment.
    """
    chain = []
    
    if category == 'Economy':
        if sentiment == 'Positive': # e.g. Strong GDP/Jobs
            chain = [
                {"step": "Economic Data Beats", "detail": "Stronger than expected growth"},
                {"step": "Yields Rise", "detail": "Bond market prices in higher rates"},
                {"step": "Currency Strengthens", "detail": "Capital inflows chase yield"},
                {"step": "Cyclicals Rally", "detail": "Banks & Industrials outperform"}
            ]
        else: # Weak Data
            chain = [
                {"step": "Economic Data Misses", "detail": "Signs of slowdown emerge"},
                {"step": "Yields Fall", "detail": "Safe haven buying in bonds"},
                {"step": "Growth Stocks Bid", "detail": "Lower rates favor tech valuations"},
                {"step": "Defensives Outperform", "detail": "Rotation into Utilities & Staples"}
            ]
    elif category == 'Politics':
        chain = [
            {"step": "Political Event", "detail": "Policy change or uncertainty"},
            {"step": "Volatility Spikes", "detail": "VIX index moves higher"},
            {"step": "Sector Rotation", "detail": "Policy-favored sectors gain"},
            {"step": "Market Repricing", "detail": "Long-term risk premiums adjust"}
        ]
    elif category == 'Energy':
        if sentiment == 'Positive': # Oil Up
            chain = [
                {"step": "Supply Constraint", "detail": "Production cuts or geopolitical tension"},
                {"step": "Crude Spikes", "detail": "Oil prices break resistance"},
                {"step": "Energy Stocks Rally", "detail": "XLE and majors gain"},
                {"step": "Inflation Fears", "detail": "Input costs rise for broader market"}
            ]
        else: # Oil Down
            chain = [
                {"step": "Oversupply / Weak Demand", "detail": "Inventories build up"},
                {"step": "Crude Slides", "detail": "Oil tests support levels"},
                {"step": "Transport Stocks Gain", "detail": "Airlines & Logistics benefit"},
                {"step": "Disinflationary Impulse", "detail": "Reduced pressure on CPI"}
            ]
    elif category == 'Technology':
        chain = [
            {"step": "Tech Catalyst", "detail": "Earnings beat or AI breakthrough"},
            {"step": "Nasdaq Rally", "detail": "Momentum traders pile in"},
            {"step": "Semi Leadership", "detail": "Chip stocks lead the advance"},
            {"step": "Broad Market Lift", "detail": "Mega-caps pull indices higher"}
        ]
    else: # General/Finance
        chain = [
            {"step": "News Break", "detail": "Market digesting information"},
            {"step": "Volume Spike", "detail": "Increased trading activity"},
            {"step": "Price Discovery", "detail": "Buyers and sellers find equilibrium"},
            {"step": "Trend Continuation", "detail": "Market incorporates new baseline"}
        ]
        
    return chain

def generate_historical_lookback(category, sentiment):
    """
    Generates simulated historical price reaction data (T-0 to T+5).
    """
    # Base pattern
    data = [0] # T-0
    
    trend = 1 if sentiment == 'Positive' else -1
    volatility = random.uniform(0.5, 1.5)
    
    current = 0
    for i in range(5):
        move = random.gauss(0.2 * trend, 0.3) * volatility
        current += move
        data.append(round(current, 2))
        
    return {
        'labels': ['Day 0', 'Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5'],
        'data': data,
        'asset': 'S&P 500' if category != 'Technology' else 'Nasdaq 100'
    }

def identify_affected_assets(title, category):
    """
    Identifies relevant tickers based on keywords.
    """
    assets = []
    title_lower = title.lower()
    
    # Simple keyword mapping
    mapping = {
        'oil': 'CL=F', 'crude': 'CL=F', 'energy': 'XLE',
        'gold': 'GC=F', 'silver': 'SI=F',
        'bitcoin': 'BTC-USD', 'crypto': 'ETH-USD',
        'apple': 'AAPL', 'iphone': 'AAPL',
        'microsoft': 'MSFT', 'windows': 'MSFT', 'azure': 'MSFT',
        'google': 'GOOGL', 'alphabet': 'GOOGL',
        'amazon': 'AMZN',
        'tesla': 'TSLA', 'ev': 'TSLA',
        'nvidia': 'NVDA', 'chip': 'NVDA', 'ai': 'NVDA',
        'bank': 'XLF', 'jpmorgan': 'JPM',
        'fed': '^TNX', 'rate': '^TNX', 'yield': '^TNX',
        'inflation': '^TNX', 'cpi': '^TNX'
    }
    
    for key, ticker in mapping.items():
        if key in title_lower:
            assets.append(ticker)
            
    # Defaults if none found
    if not assets:
        if category == 'Technology': assets = ['^IXIC', 'XLK']
        elif category == 'Energy': assets = ['CL=F', 'XLE']
        elif category == 'Finance': assets = ['^GSPC', 'XLF']
        else: assets = ['^GSPC', '^DJI']
        
    return list(set(assets))[:3] # Return top 3 unique

def generate_social_sentiment(sentiment_score):
    """
    Generates a social sentiment distribution based on the score.
    """
    # sentiment_score is roughly -1 to 1
    
    # Base distribution
    bullish = 33
    bearish = 33
    neutral = 34
    
    # Shift based on score
    shift = sentiment_score * 30 # Max shift +/- 30%
    
    bullish += shift
    bearish -= shift
    
    # Add some noise
    bullish += random.randint(-5, 5)
    bearish += random.randint(-5, 5)
    neutral = 100 - bullish - bearish
    
    # Clamp
    bullish = max(5, min(90, bullish))
    bearish = max(5, min(90, bearish))
    neutral = 100 - bullish - bearish
    
    return {
        'bullish': int(bullish),
        'bearish': int(bearish),
        'neutral': int(neutral)
    }

def generate_analysis(title, summary, category, sentiment, impact_score):
    """
    Generates a detailed market impact and investor sentiment analysis.
    """
    # Market Impact Analysis
    impact_text = ""
    if impact_score >= 8:
        impact_text = f"This development represents a significant shift in the {category.lower()} landscape. "
        impact_text += "Analysts expect immediate volatility in related sectors. "
        if category == 'Economy':
            impact_text += "Central bank policy expectations may be repriced accordingly."
        elif category == 'Technology':
            impact_text += "This could trigger a broader sector rotation or re-rating of growth stocks."
        elif category == 'Energy':
            impact_text += "Commodity prices are likely to react sharply, influencing global input costs."
    elif impact_score >= 5:
        impact_text = f"This is a noteworthy development for {category.lower()} watchers. "
        impact_text += "While immediate market disruption may be limited, it contributes to the broader narrative. "
        impact_text += "Investors should monitor follow-up reports for confirmation of the trend."
    else:
        impact_text = "The immediate market impact is expected to be muted. "
        impact_text += "However, this adds to the cumulative data points for the current quarter. "
        impact_text += "Specific assets directly linked to this news may see minor intraday moves."

    # Investor Sentiment Analysis
    sentiment_text = ""
    if sentiment == "Positive":
        sentiment_text = "Investor sentiment is likely to be buoyed by this news. "
        sentiment_text += "Risk appetite may increase, favoring equities and growth-oriented assets. "
        sentiment_text += "Institutional flows could shift towards capitalizing on this momentum."
    elif sentiment == "Negative":
        sentiment_text = "This news is likely to weigh on investor sentiment. "
        sentiment_text += "We may see a flight to safety or defensive positioning in the short term. "
        sentiment_text += "Traders should exercise caution and watch for key support levels breaking."
    else:
        sentiment_text = "The market reaction appears mixed or neutral at this stage. "
        sentiment_text += "Investors are likely digesting the details before committing to a directional bias. "
        sentiment_text += "Volatility may compress as the market awaits further clarity."

    # Advanced Features
    chain_reaction = generate_chain_reaction(category, sentiment, title)
    historical_lookback = generate_historical_lookback(category, sentiment)
    affected_assets = identify_affected_assets(title, category)
    social_sentiment = generate_social_sentiment(1 if sentiment == 'Positive' else -1 if sentiment == 'Negative' else 0)

    return {
        'market_impact': impact_text,
        'investor_sentiment': sentiment_text,
        'chain_reaction': chain_reaction,
        'historical_lookback': historical_lookback,
        'affected_assets': affected_assets,
        'social_sentiment': social_sentiment
    }

def fetch_feed_content(url):
    """
    Fetches RSS feed content using requests with a browser-like User-Agent.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.content
    except Exception as e:
        print(f"Error fetching URL {url}: {e}")
        return None

def get_google_news_feeds(country_name):
    """
    Generates search-based RSS feeds for a country to ensure diverse coverage.
    """
    queries = [
        f"{country_name} economy",
        f"{country_name} politics neutral",
        f"{country_name} financial market",
        f"{country_name} energy sector",
        f"{country_name} technology news"
    ]
    return [BASE_RSS_URL.format(query=q.replace(" ", "+")) for q in queries]

def fetch_rss_news(country_code):
    news_items = []
    
    # Map code to name for better search queries
    country_names = {
        'US': 'United States',
        'DE': 'Germany',
        'UK': 'United Kingdom',
        'CN': 'China',
        'JP': 'Japan',
        'Global': 'Global Economy'
    }
    country_name = country_names.get(country_code, 'Global Economy')
    
    # Get dynamic feeds + any static ones (optional, but dynamic is better for "whole web")
    feeds = get_google_news_feeds(country_name)
    
    # Add some specific high-quality sources if needed, but Google News aggregates them anyway.
    # We'll keep the static list as a backup or for specific reputable outlets.
    static_feeds = RSS_FEEDS.get(country_code, [])
    feeds.extend(static_feeds)
    
    # Limit to unique feeds
    feeds = list(set(feeds))
    
    for feed_url in feeds:
        try:
            print(f"Fetching RSS: {feed_url}")
            
            # Use requests to fetch content first (bypasses 403)
            xml_content = fetch_feed_content(feed_url)
            if not xml_content:
                print(f"Failed to fetch content for {feed_url}")
                continue
                
            feed = feedparser.parse(xml_content)
            print(f"RSS Status: {getattr(feed, 'status', 'OK')}, Entries: {len(feed.entries)}")
            
            # Limit to top 5 per feed to avoid overwhelming but get diversity
            for entry in feed.entries[:5]: 
                title = entry.title
                link = entry.link
                
                # Summary extraction
                summary = ""
                if hasattr(entry, 'summary'):
                    summary = clean_html(entry.summary)
                elif hasattr(entry, 'description'):
                    summary = clean_html(entry.description)
                
                # Time handling
                timestamp = time.time()
                if hasattr(entry, 'published_parsed'):
                    timestamp = time.mktime(entry.published_parsed)
                elif hasattr(entry, 'updated_parsed'):
                    timestamp = time.mktime(entry.updated_parsed)
                    
                time_str = datetime.datetime.fromtimestamp(timestamp).strftime("%H:%M")
                
                publisher = feed.feed.get('title', 'News Source')
                # Google News often puts source in title "Headline - Source"
                if " - " in title:
                    parts = title.rsplit(" - ", 1)
                    title = parts[0]
                    publisher = parts[1]
                
                category, sentiment, impact, sent_score = analyze_news_item(title)
                analysis = generate_analysis(title, summary, category, sentiment, impact)
                
                news_items.append({
                    'title': title,
                    'link': link,
                    'publisher': publisher,
                    'time': time_str,
                    'timestamp': timestamp,
                    'category': category,
                    'sentiment': sentiment,
                    'impact': impact,
                    'sentiment_score': sent_score,
                    'source_type': 'RSS',
                    'summary': summary,
                    'analysis': analysis
                })
        except Exception as e:
            print(f"Error fetching RSS {feed_url}: {e}")
            continue
            
    print(f"Total RSS items fetched: {len(news_items)}")
    return news_items

def get_news(country_code='US'):
    """
    Fetch news for a specific country/region from Yahoo and RSS.
    """
    all_news = []
    seen_titles = set()
    
    # 1. Fetch Yahoo News
    tickers = COUNTRY_TICKERS.get(country_code, COUNTRY_TICKERS['Global'])
    for ticker in tickers:
        try:
            news_items = yf.Ticker(ticker).news
            
            for item in news_items:
                # New yfinance structure: item['content'] contains the data
                content = item.get('content', {})
                if not content:
                    content = item  # Fallback to item itself if no 'content' key
                
                title = content.get('title', '')
                if not title or title in seen_titles:
                    continue
                    
                seen_titles.add(title)
                
                category, sentiment, impact, sent_score = analyze_news_item(title)
                
                # Summary extraction
                summary = content.get('summary', '')
                if not summary:
                    summary = title # Fallback
                
                analysis = generate_analysis(title, summary, category, sentiment, impact)
                
                # Date/time handling
                pub_date = content.get('pubDate', '')
                timestamp = 0
                time_str = ""
                
                if pub_date:
                    try:
                        from datetime import datetime as dt
                        parsed_dt = dt.strptime(pub_date, "%Y-%m-%dT%H:%M:%SZ")
                        timestamp = parsed_dt.timestamp()
                        time_str = parsed_dt.strftime("%H:%M")
                    except (ValueError, AttributeError) as e:
                        # Fallback to current time
                        from datetime import datetime as dt
                        timestamp = dt.now().timestamp()
                        time_str = dt.now().strftime("%H:%M")
                            
                link = content.get('clickThroughUrl', {}).get('url', '')
                if not link:
                    link = content.get('canonicalUrl', {}).get('url', '')
                if not link:
                    link = f"https://finance.yahoo.com/quote/{ticker}"
                
                publisher = content.get('provider', {}).get('displayName', 'Yahoo Finance')
                
                all_news.append({
                    'title': title,
                    'link': link,
                    'publisher': publisher,
                    'time': time_str,
                    'timestamp': timestamp,
                    'category': category,
                    'sentiment': sentiment,
                    'impact': impact,
                    'sentiment_score': sent_score,
                    'source_type': 'Yahoo',
                    'summary': summary,
                    'analysis': analysis
                })
        except Exception as e:
            print(f"[ERROR] Fetching Yahoo news for {ticker}: {e}")
            continue

    print(f"[DEBUG] Yahoo news fetched: {len(all_news)} items for {country_code}")

    # 2. Fetch RSS News
    rss_news = fetch_rss_news(country_code)
    print(f"[DEBUG] RSS news fetched: {len(rss_news)} items for {country_code}")
    
    for item in rss_news:
        if item['title'] not in seen_titles:
            seen_titles.add(item['title'])
            all_news.append(item)
    
    print(f"[DEBUG] Total news items: {len(all_news)} for {country_code}")
    
    # Sort by timestamp descending
    all_news.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # Generate Summary
    summary = generate_country_summary(all_news, country_code)
    
    # Generate Hexagon Metrics
    hexagon_data = generate_hexagon_metrics(all_news, country_code)
    
    return {
        'news': all_news,
        'summary': summary,
        'hexagon': hexagon_data
    }

def generate_country_summary(news_items, country_code='Global'):
    if not news_items:
        return {
            'eco_score': 0,
            'pol_score': 0,
            'market_sentiment': 'Neutral',
            'top_topics': [],
            'verdict': 'No data available.'
        }
        
    total_sent_score = 0
    eco_sent = 0
    pol_sent = 0
    eco_count = 0
    pol_count = 0
    
    all_words = []
    stop_words = set(['the', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'of', 'and', 'or', 'with', 'is', 'are', 'was', 'were', 'be', 'has', 'have', 'had', 'it', 'that', 'this', 'from', 'by', 'as', 'but', 'not', 'will', 'would', 'can', 'could', 'should', 'may', 'might', 'must', 'new', 'us', 'says', 'stock', 'market', 'stocks', 'markets', 'year', 'after', 'before', 'up', 'down', 'high', 'low', 'report', 'news', 'video', 'watch'])
    
    for item in news_items:
        s_score = item.get('sentiment_score', 0)
        total_sent_score += s_score
        
        if item['category'] == 'Economy':
            eco_sent += s_score
            eco_count += 1
        elif item['category'] == 'Politics':
            pol_sent += s_score
            pol_count += 1
            
        # Topic extraction
        words = re.findall(r'\w+', item['title'].lower())
        all_words.extend([w for w in words if w not in stop_words and len(w) > 3])
        
    # Normalize scores (-10 to 10) with VOLUME WEIGHTING
    # If we have fewer than 5 articles, we dampen the score significantly.
    # Damping factor = min(count, 5) / 5
    
    item_count = len(news_items)
    
    # Global Sentiment
    raw_avg_sent = (total_sent_score / item_count) * 10 if item_count > 0 else 0
    damp_factor = min(item_count, 10) / 10 # Require 10 articles for full confidence
    avg_sentiment = raw_avg_sent * damp_factor
    
    # Economy Score
    raw_eco = (eco_sent / eco_count) * 10 if eco_count > 0 else 0
    eco_damp = min(eco_count, 5) / 5 # Require 5 articles
    eco_score = raw_eco * eco_damp
    
    # Politics Score
    raw_pol = (pol_sent / pol_count) * 10 if pol_count > 0 else 0
    pol_damp = min(pol_count, 5) / 5 # Require 5 articles
    pol_score = raw_pol * pol_damp
    
    # Market Sentiment Label
    if avg_sentiment > 2: market_sentiment = "Bullish"
    elif avg_sentiment < -2: market_sentiment = "Bearish"
    else: market_sentiment = "Neutral"
    
    # Top Topics
    topic_counts = Counter(all_words)
    top_topics = [t[0] for t in topic_counts.most_common(5)]
    
    # Verdict Generation
    verdict = f"Based on {item_count} analyzed reports, the market sentiment is {market_sentiment.lower()}."
    
    if abs(eco_score) > 2:
        verdict += f" Economic indicators are trending {'positively' if eco_score > 0 else 'negatively'} ({eco_count} reports)."
    elif eco_count > 0:
        verdict += " Economic signals are currently mixed or neutral."
        
    if abs(pol_score) > 2:
        verdict += f" Political stability is {'improving' if pol_score > 0 else 'a concern'} ({pol_count} reports)."
    elif pol_count > 0:
        verdict += " The political landscape appears relatively stable."
        
    if top_topics:
        verdict += f" Key themes include {', '.join(top_topics[:3])}."
        
    # Get Macro Data
    macro_data = _get_country_macro_data(country_code, news_items)
        
    return {
        'eco_score': round(eco_score, 1),
        'pol_score': round(pol_score, 1),
        'market_sentiment': market_sentiment,
        'sentiment_score': round(avg_sentiment, 1),
        'top_topics': top_topics,
        'verdict': verdict,
        'article_count': item_count,
        'macro_data': macro_data,
        'top_news': news_items[:3] # Top 3 news for the feed
    }

def _get_monetary_data_points(news_items, score):
    """Extract real monetary policy data from news with specific details - INVESTOR GRADE"""
    import re
    from datetime import datetime
    
    all_text = ' '.join([item['title'] + ' ' + item.get('summary', '') for item in news_items])
    numbers = extract_numbers_from_text(all_text)
    actions = extract_policy_actions(news_items)
    
    points = []
    
    # Extract central bank names
    cb_pattern = r'\b(Fed|Federal Reserve|ECB|European Central Bank|BOJ|Bank of Japan|BOE|Bank of England|PBOC|SNB|RBA|BoC)\b'
    central_banks = list(set(re.findall(cb_pattern, all_text, re.IGNORECASE)))
    
    # Extract specific dates with month/day
    date_pattern = r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{1,2}(?:,?\s+\d{4})?\b'
    dates = re.findall(date_pattern, all_text, re.IGNORECASE)
    
    # Extract vote counts (e.g., "unanimous", "8-1", "11-1")
    vote_pattern = r'(unanimous|(\d+)-(\d+)\s*vote|split\s*vote)'
    vote_matches = re.findall(vote_pattern, all_text, re.IGNORECASE)
    
    # Extract forward guidance keywords
    forward_guidance = []
    if 'data.dependent' in all_text.lower() or 'data dependent' in all_text.lower():
        forward_guidance.append("Data-dependent approach")
    if 'patient' in all_text.lower() and ('policy' in all_text.lower() or 'approach' in all_text.lower()):
        forward_guidance.append("Patient stance indicated")
    if 'restrictive' in all_text.lower():
        forward_guidance.append("Maintaining restrictive conditions")
    if 'premature' in all_text.lower() and 'cut' in all_text.lower():
        forward_guidance.append("Premature to cut rates")
    
    # Policy actions with full context
    if actions:
        action_summary = actions[0] if len(actions) == 1 else f"{len(actions)} policy moves"
        points.append(f"📅 **Latest Action**: {action_summary}")
        if dates:
            points.append(f"🗓️ **Meeting Date**: {dates[0]}")
        if vote_matches:
            if 'unanimous' in vote_matches[0][0].lower():
                points.append(f"✅ **Vote**: Unanimous consensus")
            elif vote_matches[0][1]:  # Has vote count
                points.append(f"🗳️ **Vote**: {vote_matches[0][1]}-{vote_matches[0][2]} split decision")
    else:
        points.append(f"📊 **Policy Stance**: {'Dovish (supportive)' if score > 60 else 'Hawkish (restrictive)' if score < 40 else 'Neutral (balanced)'}")
    
    # Interest rates with richer context
    if numbers['rates']:
        latest_rate = numbers['rates'][-1]
        if len(numbers['rates']) > 1:
            prev_rate = numbers['rates'][-2]
            change = latest_rate - prev_rate
            arrow = "↗" if change > 0 else "↘" if change < 0 else "→"
            direction = "hawkish tightening" if change > 0 else "dovish easing" if change < 0 else "no change"
            points.append(f"💰 **Policy Rate**: {latest_rate}% ({arrow} {abs(change):.2f}pp {direction})")
            
            # Add historical context
            if latest_rate > 5.0:
                points.append(f"📈 **Context**: Rate at multi-year high ({latest_rate}% level)")
            elif latest_rate < 1.0:
                points.append(f"📉 **Context**: Near zero-rate environment ({latest_rate}%)")
        else:
            points.append(f"💰 **Current Rate**: {latest_rate}%")
    
    # Basis points with aggregate and context
    if numbers['basis_points']:
        total_bps = sum(numbers['basis_points'])
        avg_bps = total_bps / len(numbers['basis_points'])
        cycle_direction = "tightening" if total_bps > 0 else "easing"
        points.append(f"📈 **Cumulative Moves**: {total_bps}bps {cycle_direction} (avg {avg_bps:.0f}bps per move)")
    
    # Forward guidance
    if forward_guidance:
        points.append(f"🎯 **Forward Guidance**: {' | '.join(forward_guidance)}")
    
    # Central bank attribution
    if central_banks:
        cb_list = ", ".join(central_banks[:3])
        points.append(f"🏛️ **Institutions**: {cb_list}{' +' + str(len(central_banks)-3) + ' more' if len(central_banks) > 3 else ''}")
    
    # News coverage with sentiment breakdown
    monetary_mentions = sum(1 for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['rate', 'fed', 'ecb', 'boj', 'monetary', 'policy']))
    if monetary_mentions > 0:
        coverage_pct = (monetary_mentions / len(news_items) * 100) if news_items else 0
        hawkish_mentions = sum(1 for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['hike', 'hawkish', 'tighten', 'restrictive']))
        dovish_mentions = sum(1 for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['cut', 'dovish', 'ease', 'accommodative']))
        
        sentiment_label = "Hawkish" if hawkish_mentions > dovish_mentions else "Dovish" if dovish_mentions > hawkish_mentions else "Balanced"
        points.append(f"📰 **Media Coverage**: {monetary_mentions} articles ({coverage_pct:.0f}% of total) - {sentiment_label} tone")
    
    return points if points else ['Insufficient monetary policy data from recent news']

def _get_country_macro_data(country_code, news_items=[]):
    """
    Fetch real-time macro indicators for the country outlook.
    Returns a list of dicts with label, value, change, trend_data.
    """
    import yfinance as yf
    import random
    
    # Define tickers based on country
    tickers = {
        'US': {'equity': '^GSPC', 'yield': '^TNX', 'fx': 'DX-Y.NYB'},
        'DE': {'equity': '^GDAXI', 'yield': None, 'fx': 'EURUSD=X'},
        'UK': {'equity': '^FTSE', 'yield': None, 'fx': 'GBPUSD=X'},
        'CN': {'equity': '000001.SS', 'yield': None, 'fx': 'CNY=X'},
        'JP': {'equity': '^N225', 'yield': None, 'fx': 'JPY=X'},
        'Global': {'equity': '^MS_WORLD', 'yield': '^TNX', 'fx': 'DX-Y.NYB'} # MS World proxy
    }
    
    country_tickers = tickers.get(country_code, tickers['Global'])
    
    macro_data = []
    
    # Helper for deep analysis
    def _get_macro_analysis(indicator, country):
        """Returns detailed structural analysis for macro indicators"""
        analysis = {
            'Equity Market': {
                'structural_analysis': 'The equity market is currently navigating a transition from high-inflation headwinds to a potential soft-landing scenario. Valuations remain elevated in tech, driven by AI optimism, while broader indices show caution regarding rate cut timing.',
                'larger_trend': 'Long-term trend remains bullish, supported by technological innovation and corporate earnings resilience. However, the era of "free money" is over, demanding higher quality from balance sheets.',
                'relevance': 'Equities represent the primary growth engine for capital. They are a leading indicator of economic sentiment and corporate health, often pricing in economic shifts 6-12 months in advance.',
                'drivers': ['Corporate Earnings', 'Fed Policy', 'AI Innovation', 'Consumer Spending']
            },
            '10Y Yield': {
                'structural_analysis': 'The 10-Year Treasury yield is hovering in a restrictive territory, reflecting a "higher for longer" rate regime. Recent volatility suggests market uncertainty about the neutral rate (r*) and long-term inflation expectations.',
                'larger_trend': 'We are in a secular bear market for bonds (rising yields) after a 40-year bull run ended in 2020. This structural shift implies higher borrowing costs for the foreseeable future.',
                'relevance': 'The "risk-free" rate against which all other assets are valued. Rising yields compress stock valuations (P/E ratios) and increase mortgage rates, directly impacting housing and tech.',
                'drivers': ['Inflation Expectations', 'Fed Funds Rate', 'Term Premium', 'Global Demand']
            },
            'GDP Growth': {
                'structural_analysis': 'GDP growth has defied recession calls, powered by robust consumer spending and fiscal stimulus. However, divergences are emerging, with manufacturing softening while services remain resilient.',
                'larger_trend': 'Trend growth is slowing in developed markets due to demographics (aging population) and productivity challenges, though AI adoption may offer a productivity boost in the coming decade.',
                'relevance': 'The ultimate scorecard for economic health. Two consecutive quarters of negative growth defines a technical recession. Strong growth supports corporate earnings but can reignite inflation.',
                'drivers': ['Consumer Spending', 'Business Investment', 'Government Expenditure', 'Net Exports']
            },
            'Inflation (CPI)': {
                'structural_analysis': 'Disinflation is progressing, but the "last mile" to the 2% target is proving difficult due to sticky services inflation and shelter costs. Goods deflation has largely played out.',
                'larger_trend': 'We have moved from a regime of chronic disinflation (2008-2020) to a volatile inflation regime, driven by deglobalization, decarbonization, and demographics (the "3 Ds").',
                'relevance': 'Inflation erodes purchasing power. It is the primary driver of Central Bank policy. High inflation forces rate hikes; stable inflation allows for accommodation and economic stability.',
                'drivers': ['Energy Prices', 'Housing/Shelter', 'Wage Growth', 'Supply Chains']
            },
            'Unemployment': {
                'structural_analysis': 'The labor market remains historically tight, though cracks are forming in hiring rates and quit rates. This resilience supports consumption but keeps upward pressure on wages.',
                'larger_trend': 'Structural labor shortages are likely to persist due to retirement waves (Boomers) and lower immigration in some regions, shifting power from capital to labor.',
                'relevance': 'The pulse of the consumer. Low unemployment supports spending and confidence. Rising unemployment is the most reliable signal of an oncoming recession and typically triggers Fed rate cuts.',
                'drivers': ['Labor Participation', 'Job Openings', 'Wage Growth', 'Demographics']
            },
            'Currency': {
                'structural_analysis': 'Currency strength is currently driven by relative interest rate differentials and economic growth divergence. The "higher for longer" Fed stance has supported the USD, weighing on peers.',
                'larger_trend': 'Currencies are moving from a period of synchronized global easing to divergent tightening cycles. The USD retains its dominance as the global reserve currency and safe haven during geopolitical stress.',
                'relevance': 'Currency strength affects export competitiveness and inflation. A strong currency lowers import costs (disinflationary) but hurts exporters. A weak currency boosts exports but imports inflation.',
                'drivers': ['Interest Rate Differentials', 'Economic Growth Gap', 'Safe Haven Flows', 'Trade Balance']
            }
        }
        return analysis.get(indicator, {
            'structural_analysis': 'Detailed analysis unavailable.',
            'larger_trend': 'Trend data unavailable.',
            'relevance': 'Relevance data unavailable.',
            'drivers': []
        })

    # 1. Equity Market (Real)
    try:
        equity = yf.Ticker(country_tickers['equity'])
        hist = equity.history(period="max") # Fetch MAX for charts
        if not hist.empty:
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            
            # Structured trend data
            trend_values = hist['Close'].tolist()
            trend_dates = hist.index.strftime('%Y-%m-%d').tolist()
            
            analysis = _get_macro_analysis('Equity Market', country_code)
            
            macro_data.append({
                'label': 'Equity Market',
                'value': f"{current:,.0f}",
                'change': change,
                'change_label': f"{change:+.2f}%",
                'trend': {'dates': trend_dates, 'values': trend_values},
                'frequency': 'daily',
                'format': 'number',
                'details': {
                    'structural_analysis': analysis['structural_analysis'],
                    'larger_trend': analysis['larger_trend'],
                    'relevance': analysis['relevance'],
                    'key_drivers': analysis['drivers'],
                    'related_news': [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['stocks', 'market', 'equity', 'sp500'])][:3]
                }
            })
    except:
        pass
        
    # 2. 10Y Yield (Real)
    try:
        if country_tickers['yield']:
            bond = yf.Ticker(country_tickers['yield'])
            hist = bond.history(period="max")
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = current - prev
                
                trend_values = hist['Close'].tolist()
                trend_dates = hist.index.strftime('%Y-%m-%d').tolist()
                
                analysis = _get_macro_analysis('10Y Yield', country_code)
                
                macro_data.append({
                    'label': '10Y Yield',
                    'value': f"{current:.2f}%",
                    'change': change,
                    'change_label': f"{change:+.2f}bp",
                    'trend': {'dates': trend_dates, 'values': trend_values},
                    'frequency': 'daily',
                    'format': 'percent',
                    'inverse': True,
                    'details': {
                        'structural_analysis': analysis['structural_analysis'],
                        'larger_trend': analysis['larger_trend'],
                        'relevance': analysis['relevance'],
                        'key_drivers': analysis['drivers'],
                        'related_news': [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['yield', 'bond', 'treasury', 'rates'])][:3]
                    }
                })
    except:
        pass
        
    # 3. GDP Growth (Real/Estimated)
    from economic_data import get_economic_data, fetch_fred_historical
    eco_data = get_economic_data()
    
    gdp_val = 2.9 
    if country_code == 'US': gdp_val = 3.1
    elif country_code == 'CN': gdp_val = 5.2
    elif country_code == 'DE': gdp_val = -0.3
    
    # Try to fetch real GDP history for US
    gdp_trend_data = None
    gdp_freq = 'quarterly'
    if country_code == 'US' or country_code == 'Global':
        # GDP is quarterly
        # Let's use 'A191RL1Q225SBEA' (Real GDP Growth)
        df_growth = fetch_fred_historical('A191RL1Q225SBEA', period='max')
        if df_growth is not None and not df_growth.empty:
            gdp_trend_data = {
                'dates': df_growth.index.strftime('%Y-%m-%d').tolist(),
                'values': df_growth['Close'].tolist()
            }
    
    if not gdp_trend_data:
        # Simulate with dates
        import datetime
        end_date = datetime.datetime.now()
        dates = [(end_date - datetime.timedelta(days=x*90)).strftime('%Y-%m-%d') for x in range(20)][::-1] # 5 years quarterly
        values = [gdp_val + random.uniform(-0.5, 0.5) for _ in range(20)]
        gdp_trend_data = {'dates': dates, 'values': values}
    
    analysis = _get_macro_analysis('GDP Growth', country_code)
    
    macro_data.append({
        'label': 'GDP Growth',
        'value': f"{gdp_val:.1f}%",
        'change': 0.0,
        'change_label': "Stable",
        'trend': gdp_trend_data,
        'frequency': gdp_freq,
        'format': 'percent',
        'details': {
            'structural_analysis': analysis['structural_analysis'],
            'larger_trend': analysis['larger_trend'],
            'relevance': analysis['relevance'],
            'key_drivers': analysis['drivers'],
            'related_news': [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['gdp', 'growth', 'economy', 'recession'])][:3]
        }
    })
    
    # 4. Inflation (CPI)
    cpi_data = eco_data.get('cpi', {})
    cpi_val = cpi_data.get('value', 3.2)
    if country_code == 'CN': cpi_val = 0.7
    if country_code == 'UK': cpi_val = 3.4
    if country_code == 'DE': cpi_val = 2.5
    
    # Fetch Real CPI History
    cpi_trend_data = None
    cpi_freq = 'monthly'
    if country_code == 'US' or country_code == 'Global':
        # CPIAUCSL is monthly.
        df_cpi = fetch_fred_historical('CPIAUCSL', period='max')
        if df_cpi is not None and not df_cpi.empty:
            # We are using the static fallback which returns 'Close' as the value we want (YoY or Level)
            # The static fallback returns YoY directly for CPIAUCSL
            cpi_trend_data = {
                'dates': df_cpi.index.strftime('%Y-%m-%d').tolist(),
                'values': df_cpi['Close'].tolist()
            }

    if not cpi_trend_data:
        import datetime
        end_date = datetime.datetime.now()
        dates = [(end_date - datetime.timedelta(days=x*30)).strftime('%Y-%m-%d') for x in range(60)][::-1]
        values = [cpi_val + random.uniform(-0.5, 0.5) for _ in range(60)]
        cpi_trend_data = {'dates': dates, 'values': values}
    
    analysis = _get_macro_analysis('Inflation (CPI)', country_code)
    
    macro_data.append({
        'label': 'Inflation (CPI)',
        'value': f"{cpi_val:.1f}%",
        'change': cpi_data.get('change', -0.1),
        'change_label': "Cooling" if cpi_data.get('change', 0) < 0 else "Rising",
        'trend': cpi_trend_data,
        'frequency': cpi_freq,
        'format': 'percent',
        'inverse': True, 
        'details': {
            'structural_analysis': analysis['structural_analysis'],
            'larger_trend': analysis['larger_trend'],
            'relevance': analysis['relevance'],
            'key_drivers': analysis['drivers'],
            'related_news': [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['inflation', 'cpi', 'prices', 'cost of living'])][:3]
        }
    })
    
    # 5. Unemployment
    unemp_data = eco_data.get('unemployment', {})
    unemp_val = unemp_data.get('value', 3.9)
    if country_code == 'DE': unemp_val = 5.9
    if country_code == 'UK': unemp_val = 4.2
    
    unemp_trend_data = None
    unemp_freq = 'monthly'
    if country_code == 'US' or country_code == 'Global':
        df_unemp = fetch_fred_historical('UNRATE', period='max')
        if df_unemp is not None and not df_unemp.empty:
            unemp_trend_data = {
                'dates': df_unemp.index.strftime('%Y-%m-%d').tolist(),
                'values': df_unemp['Close'].tolist()
            }
            
    if not unemp_trend_data:
        import datetime
        end_date = datetime.datetime.now()
        dates = [(end_date - datetime.timedelta(days=x*30)).strftime('%Y-%m-%d') for x in range(60)][::-1]
        values = [unemp_val + random.uniform(-0.2, 0.2) for _ in range(60)]
        unemp_trend_data = {'dates': dates, 'values': values}
    
    analysis = _get_macro_analysis('Unemployment', country_code)
    
    macro_data.append({
        'label': 'Unemployment',
        'value': f"{unemp_val:.1f}%",
        'change': unemp_data.get('change', 0.0),
        'change_label': "Steady",
        'trend': unemp_trend_data,
        'frequency': unemp_freq,
        'format': 'percent',
        'inverse': True,
        'details': {
            'structural_analysis': analysis['structural_analysis'],
            'larger_trend': analysis['larger_trend'],
            'relevance': analysis['relevance'],
            'key_drivers': analysis['drivers'],
            'related_news': [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['jobs', 'unemployment', 'labor', 'hiring'])][:3]
        }
    })
    
    # 6. Currency (Real)
    try:
        if country_tickers['fx']:
            fx = yf.Ticker(country_tickers['fx'])
            hist = fx.history(period="max") # Fetch MAX for charts
            if not hist.empty:
                current = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2]
                change = ((current - prev) / prev) * 100
                
                # Structured trend data
                trend_values = hist['Close'].tolist()
                trend_dates = hist.index.strftime('%Y-%m-%d').tolist()
                
                label = "USD Index" if country_code == 'US' else f"{country_code}/USD"
                
                analysis = _get_macro_analysis('Currency', country_code)
                
                macro_data.append({
                    'label': label,
                    'value': f"{current:.2f}",
                    'change': change,
                    'change_label': f"{change:+.2f}%",
                    'trend': {'dates': trend_dates, 'values': trend_values},
                    'frequency': 'daily',
                    'format': 'number',
                    'details': {
                        'structural_analysis': analysis['structural_analysis'],
                        'larger_trend': analysis['larger_trend'],
                        'relevance': analysis['relevance'],
                        'key_drivers': analysis['drivers'],
                        'related_news': [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['currency', 'dollar', 'euro', 'yen', 'fx'])][:3]
                    }
                })
    except:
        pass

    return macro_data

def _get_inflation_data_points(news_items, score):
    """Extract real inflation and growth data with specifics - INVESTOR GRADE"""
    import re
    
    all_text = ' '.join([item['title'] + ' ' + item.get('summary', '') for item in news_items])
    numbers = extract_numbers_from_text(all_text)
    
    points = []
    
    # Distinguish core vs headline CPI
    core_pattern = r'core\s+(?:cpi|inflation|pce)[:\s]+([0-9.]+)%'
    headline_pattern = r'(?:cpi|inflation|headline)[:\s]+([0-9.]+)%'
    core_matches = re.findall(core_pattern, all_text, re.IGNORECASE)
    headline_matches = re.findall(headline_pattern, all_text, re.IGNORECASE)
    
    # YoY vs MoM distinction
    yoy_pattern = r'([0-9.]+)%\s*(?:year.over.year|yoy|y/y|annually)'
    mom_pattern = r'([0-9.]+)%\s*(?:month.over.month|mom|m/m|monthly)'
    yoy_values = [float(x) for x in re.findall(yoy_pattern, all_text, re.IGNORECASE)]
    mom_values = [float(x) for x in re.findall(mom_pattern, all_text, re.IGNORECASE)]
    
    # Inflation readings with granular breakdown
    if numbers['percentages']:
        inflation_vals = [p for p in numbers['percentages'] if 0 < p < 20]
        if inflation_vals:
            latest = inflation_vals[-1]
            
            # Core vs Headline if available
            if core_matches and headline_matches:
                core_val = float(core_matches[-1])
                headline_val = float(headline_matches[-1])
                spread = core_val - headline_val
                points.append(f"📊 **Headline CPI**: {headline_val}% | **Core**: {core_val}% (spread: {spread:+.1f}pp)")
            elif headline_matches:
                points.append(f"📊 **Headline CPI**: {float(headline_matches[-1])}%")
            
            # YoY vs MoM if available
            if yoy_values and mom_values:
                points.append(f"📈 **YoY**: {yoy_values[-1]}% | **MoM**: {mom_values[-1]}% annualized rate")
            elif yoy_values:
                points.append(f"📈 **Year-over-Year**: {yoy_values[-1]}%")
            
            if len(inflation_vals) > 1:
                prev = inflation_vals[-2]
                change = latest - prev
                arrow = "↗" if change > 0 else "↘" if change < 0 else "→"
                verb = "accelerated" if change > 0 else "decelerated" if change < 0 else "held steady"
                points.append(f"📉 **Recent Move**: {arrow} {verb} {abs(change):.1f}pp vs prior period")
            
            avg = sum(inflation_vals) / len(inflation_vals)
            vs_avg = latest - avg
            points.append(f"📊 **Average**: {avg:.1f}% ({'+' if vs_avg > 0 else ''}{vs_avg:.1f}pp vs current, n={len(inflation_vals)})")
            
            # Trend determination with context
            if len(inflation_vals) >= 3:
                recent_trend = inflation_vals[-1] - inflation_vals[-3]
                if recent_trend > 0.5:
                    trend_assessment = "⚠️ **Trend**: Accelerating ({recent_trend:+.1f}pp) - potential overheat risk"
                elif recent_trend < -0.5:
                    trend_assessment = "✅ **Trend**: Decelerating ({recent_trend:.1f}pp) - disinflationary"
                else:
                    trend_assessment = f"→ **Trend**: Stable ({recent_trend:+.1f}pp) - range-bound"
                points.append(trend_assessment)
            
            # Distance from target (assume 2% for most central banks)
            target = 2.0
            deviation = latest - target
            if abs(deviation) > 1.0:
                points.append(f"🎯 **vs Target**: {abs(deviation):.1f}pp {'above' if deviation > 0 else 'below'} 2% target - {'significant overshoot' if deviation > 1 else 'notable undershoot'}")
    
    # Extract GDP mentions with more context
    gdp_pattern = r'GDP[:\s]+([+-]?[0-9.]+)%'
    gdp_matches = re.findall(gdp_pattern, all_text, re.IGNORECASE)
    if gdp_matches:
        gdp_val = float(gdp_matches[-1])
        growth_assessment = "strong expansion" if gdp_val > 3 else "moderate growth" if gdp_val > 1 else "stagnation risk" if gdp_val > -0.5 else "recession"
        points.append(f"💹 **GDP Growth**: {gdp_val:+.1f}% ({growth_assessment})")
    
    # Employment indicators
    unemployment_pattern = r'unemployment[:\s]+([0-9.]+)%'
    unemployment_matches = re.findall(unemployment_pattern, all_text, re.IGNORECASE)
    if unemployment_matches:
        unemp_rate = float(unemployment_matches[-1])
        labor_market = "tight" if unemp_rate < 4.0 else "balanced" if unemp_rate < 5.5 else "slack"
        points.append(f"👥 **Unemployment**: {unemp_rate}% ({labor_market} labor market)")
    
    # Recession signals
    recession_keywords = re.findall(r'\b(recession|downturn|contraction|negative growth)\b', all_text, re.IGNORECASE)
    if recession_keywords:
        points.append(f"⚠️ **Recession Risk**: {len(recession_keywords)} mentions - elevated macro uncertainty")
    
    # Growth outlook based on score with nuance
    if score > 70:
        points.append("🟢 **Outlook**: Goldilocks (robust growth + controlled inflation)")
    elif score > 60:
        points.append("🟢 **Outlook**: Expansion phase with manageable price pressures")
    elif score > 45:
        points.append("🟡 **Outlook**: Moderate trajectory, data-dependent")
    elif score > 30:
        points.append("🟠 **Outlook**: Stagflation concerns (weak growth + sticky inflation)")
    else:
        points.append("🔴 **Outlook**: Severe contraction/recession risk")
    
    # News coverage breakdown with thematic analysis
    inflation_mentions = sum(1 for item in news_items if 'inflation' in (item['title'] + item.get('summary', '')).lower())
    growth_mentions = sum(1 for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['gdp', 'growth', 'expansion', 'recession']))
    employment_mentions = sum(1 for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['jobs', 'employment', 'unemployment', 'payroll']))
    
    if inflation_mentions + growth_mentions + employment_mentions > 0:
        total_econ = inflation_mentions + growth_mentions + employment_mentions
    points.append(f"📰 **Coverage**: {inflation_mentions} inflation, {growth_mentions} growth, {employment_mentions} employment ({total_econ} total)")
    
    return points if points else ['Insufficient inflation/growth data from recent news']

def _generate_score_drivers(news_items, score, metric_name):
    """Generate explanation of WHY the score is at this level based on actual news - WITH EXAMPLES"""
    import re
    
    if not news_items:
        return [f"Score based on general {metric_name.lower()} conditions", "Limited recent news coverage for this metric"]
    
    drivers = []
    
    # Extract key themes from titles
    titles = [item['title'] for item in news_items[:5]]
    all_text = ' '.join(titles).lower()
    
    # Common patterns that drive scores WITH specific examples
    if metric_name == 'Monetary Policy':
        if 'cut' in all_text or 'lower' in all_text or 'dovish' in all_text:
            example = [t for t in titles if any(kw in t.lower() for kw in ['cut', 'lower', 'dovish'])][0] if titles else "rate cut"
            drivers.append(f"📉 **Rate cut signals** detected (e.g., \"{example[:60]}...\")")
        if 'hike' in all_text or 'raise' in all_text or 'hawkish' in all_text:
            example = [t for t in titles if any(kw in t.lower() for kw in ['hike', 'raise', 'hawkish'])][0] if titles else "rate hike"
            drivers.append(f"📈 **Rate hike expectations** (e.g., \"{example[:60]}...\")")
        if 'pause' in all_text or 'hold' in all_text:
            drivers.append("⏸️ **Policy pause** or wait-and-see stance indicated")
        if 'inflation' in all_text:
            drivers.append("💹 **Inflation data** influencing policy trajectory")
    
    elif metric_name == 'Inflation & Growth':
        if any(word in all_text for word in ['inflation', 'cpi', 'pce', 'prices']):
            example = [t for t in titles if any(kw in t.lower() for kw in ['inflation', 'cpi', 'pce'])][0] if titles else "inflation"
            drivers.append(f"📊 **Inflation data releases** (e.g., \"{example[:60]}...\")")
        if any(word in all_text for word in ['gdp', 'growth', 'expansion', 'recession']):
            example = [t for t in titles if any(kw in t.lower() for kw in ['gdp', 'growth', 'recession'])][0] if titles else "growth"
            drivers.append(f"📈 **Economic growth updates** (e.g., \"{example[:60]}...\")")
        if 'jobs' in all_text or 'employment' in all_text or 'unemployment' in all_text:
            drivers.append("👥 **Labor market** developments affecting outlook")
    
    elif metric_name == 'Political Risk':
        if any(word in all_text for word in ['tariff', 'trade war', 'sanctions', 'trade']):
            example = [t for t in titles if any(kw in t.lower() for kw in ['tariff', 'trade war', 'sanctions'])][0] if titles else "trade"
            drivers.append(f"🌐 **Trade policy developments** (e.g., \"{example[:60]}...\")")
        if any(word in all_text for word in ['election', 'vote', 'government']):
            drivers.append("🗳️ **Political events** and electoral developments")
        if any(word in all_text for word in ['geopolitical', 'tension', 'conflict', 'war']):
            example = [t for t in titles if any(kw in t.lower() for kw in ['tension', 'conflict'])][0] if titles else "geopolitics"
            drivers.append(f"⚠️ **Geopolitical tensions** (e.g., \"{example[:60]}...\")")
        if any(word in all_text for word in ['regulation', 'policy', 'reform']):
            drivers.append("📜 **Regulatory changes** affecting business environment")
    
    elif metric_name == 'Currency Strength':
        if any(word in all_text for word in ['dollar', 'euro', 'yen', 'yuan', 'forex', 'fx']):
            drivers.append("💱 **FX market movements** impacting competitiveness")
        if 'intervention' in all_text:
            drivers.append("🏦 **Central bank intervention** actions in currency markets")
    
    elif metric_name == 'Investor Sentiment':
        if any(word in all_text for word in ['rally', 'gain', 'surge', 'rise', 'bull']):
            example = [t for t in titles if any(kw in t.lower() for kw in ['rally', 'surge', 'gain'])][0] if titles else "rally"
            drivers.append(f"📈 **Risk-on sentiment** (e.g., \"{example[:60]}...\")")
        if any(word in all_text for word in ['fall', 'drop', 'plunge', 'decline', 'bear']):
            example = [t for t in titles if any(kw in t.lower() for kw in ['fall', 'drop', 'decline'])][0] if titles else "selloff"
            drivers.append(f"📉 **Market selloffs** (e.g., \"{example[:60]}...\")")
        if any(word in all_text for word in ['volatility', 'vix', 'uncertainty']):
            drivers.append("📊 **Elevated volatility** and uncertainty")
    
    elif metric_name == 'Fiscal Health':
        if any(word in all_text for word in ['debt', 'deficit', 'budget']):
            drivers.append("💰 **Debt/deficit concerns** shaping fiscal outlook")
        if any(word in all_text for word in ['spending', 'stimulus', 'package']):
            drivers.append("💵 **Fiscal stimulus** programs proposed/enacted")
    
    elif metric_name == 'External Vulnerability':
        if any(word in all_text for word in ['reserves', 'balance', 'trade']):
            drivers.append("📊 **Trade balance** and reserve levels monitored")
        if any(word in all_text for word in ['sanctions', 'embargo']):
            example = [t for t in titles if any(kw in t.lower() for kw in ['sanctions', 'embargo'])][0] if titles else "sanctions"
            drivers.append(f"🚫 **Sanctions/restrictions** (e.g., \"{example[:60]}...\")")
    
    # Add headline count
    if len(titles) > 0:
        drivers.append(f"📰 **Based on {len(titles)} recent {metric_name.lower()} headlines**")
    
    # Score interpretation with context
    if score > 70:
        drivers.append(f"✅ **Strong positive signals** → {score:.0f}/100 score")
    elif score > 50:
        drivers.append(f"🟡 **Moderately positive** → {score:.0f}/100 score")
    elif score > 30:
        drivers.append(f"⚠️ **Mixed/cautious signals** → {score:.0f}/100 score")
    else:
        drivers.append(f"🔴 **Concerning developments** → {score:.0f}/100 score")
    
    # Always return array
    if not drivers:
        drivers = [f"Score based on general {metric_name.lower()} sentiment", f"Limited recent news coverage for this metric"]
    
    return drivers


def generate_hexagon_metrics(news_items, country_code='Global'):
    """
    Generates 7 hexagon metrics (0-100 scale) for macro dashboard.
    Returns data for center + 6 surrounding hexagons.
    """
    if not news_items or len(news_items) == 0:
        # Return simulated defaults with some variance for demonstration
        import random
        random.seed(hash(country_code))  # Consistent per country
        base_scores = {
            'monetary': random.randint(45, 75),
            'inflation': random.randint(40, 70),
            'currency': random.randint(45, 65),
            'political': random.randint(50, 70),
            'sentiment': random.randint(45, 75),
            'fiscal': random.randint(40, 65),
            'external': random.randint(45, 70)
        }
        master = sum(base_scores.values()) / 7
        regime = 'Risk-On' if master >= 65 else 'Cautiously Optimistic' if master >= 55 else 'Neutral' if master >= 45 else 'Cautious'
        
        return {
            'center': {
                'score': round(master, 1),
                'label': 'Macro Score',
                'regime': regime,
                'breakdown': {
                    'description': f'Simulated macro health score for {country_code} (limited news data).',
                    'market_implications': f'Demo mode: showing sample {regime.lower()} environment.',
                    'components': [f'{k.title()}: {v}%' for k, v in base_scores.items()]
                }
            },
            'hexagons': [
                {'position': 'top', 'label': 'Monetary Policy', 'score': base_scores['monetary'], 'detail': f'{base_scores["monetary"]}% stance', 
                 'breakdown': {'description': 'Demo: Central bank policy.', 'market_implications': 'Simulated data', 'data_points': ['Demo mode active']}},
                {'position': 'topRight', 'label': 'Inflation & Growth', 'score': base_scores['inflation'], 'detail': f'{base_scores["inflation"]}% outlook',
                 'breakdown': {'description': 'Demo: Price stability.', 'market_implications': 'Simulated data', 'data_points': ['Demo mode active']}},
                {'position': 'right', 'label': 'Currency Strength', 'score': base_scores['currency'], 'detail': f'{base_scores["currency"]}% strength',
                 'breakdown': {'description': 'Demo: FX dynamics.', 'market_implications': 'Simulated data', 'data_points': ['Demo mode active']}},
                {'position': 'bottomRight', 'label': 'Political Risk', 'score': base_scores['political'], 'detail': f'{base_scores["political"]}% stability',
                 'breakdown': {'description': 'Demo: Governance.', 'market_implications': 'Simulated data', 'data_points': ['Demo mode active']}},
                {'position': 'bottomLeft', 'label': 'Investor Sentiment', 'score': base_scores['sentiment'], 'detail': f'{base_scores["sentiment"]}% positive',
                 'breakdown': {'description': 'Demo: Market psychology.', 'market_implications': 'Simulated data', 'data_points': ['Demo mode active']}},
                {'position': 'left', 'label': 'Fiscal Health', 'score': base_scores['fiscal'], 'detail': f'{base_scores["fiscal"]}% sustainability',
                 'breakdown': {'description': 'Demo: Govt finances.', 'market_implications': 'Simulated data', 'data_points': ['Demo mode active']}},
                {'position': 'topLeft', 'label': 'External Vulnerability', 'score': base_scores['external'], 'detail': f'{base_scores["external"]}% resilience',
                 'breakdown': {'description': 'Demo: External shocks.', 'market_implications': 'Simulated data', 'data_points': ['Demo mode active']}}
            ]
        }
    
    # Analyze news for each metric
    monetary_score = 50
    inflation_score = 50
    currency_score = 50
    political_score = 50
    sentiment_score = 50
    fiscal_score = 50
    external_score = 50
    
    # Monetary Policy: Higher score = dovish (good for risk), lower = hawkish
    monetary_keywords = ['rate cut', 'dovish', 'stimulus', 'easing', 'accommodation']
    hawkish_keywords = ['rate hike', 'hawkish', 'tightening', 'restrictive']
    
    for item in news_items:
        text = (item['title'] + ' ' + item.get('summary', '')).lower()
        
        # Monetary Policy
        if any(kw in text for kw in monetary_keywords):
            monetary_score += 5
        if any(kw in text for kw in hawkish_keywords):
            monetary_score -= 5
            
        # Inflation (lower is better)
        if 'inflation' in text:
            if 'rising' in text or 'surge' in text or 'spike' in text:
                inflation_score -= 4
            elif 'falling' in text or 'decline' in text or 'ease' in text:
                inflation_score += 4
                
        # Currency (strength from trade/export news)
        if 'export' in text or 'trade surplus' in text:
            currency_score += 3
        if 'import' in text or 'trade deficit' in text:
            currency_score -= 3
            
        # Political Risk (stability vs chaos)
        if item['category'] == 'Politics':
            if item['sentiment'] == 'Negative':
                political_score -= 4
            elif item['sentiment'] == 'Positive':
                political_score += 4
                
        # Investor Sentiment (from overall sentiment)
        if item['sentiment'] == 'Positive':
            sentiment_score += 2
        elif item['sentiment'] == 'Negative':
            sentiment_score -= 2
            
        # Fiscal Health (debt/deficit keywords)
        if 'deficit' in text or 'debt crisis' in text:
            fiscal_score -= 3
        if 'surplus' in text or 'fiscal responsibility' in text:
            fiscal_score += 3
            
        # External Vulnerability (trade wars, sanctions)
        if 'sanctions' in text or 'tariff' in text or 'trade war' in text:
            external_score -= 4
        if 'trade deal' in text or 'cooperation' in text:
            external_score += 4
    
    # Clamp scores to 0-100
    def clamp(val):
        return max(0, min(100, val))
    
    monetary_score = clamp(monetary_score)
    inflation_score = clamp(inflation_score)
    currency_score = clamp(currency_score)
    political_score = clamp(political_score)
    sentiment_score = clamp(sentiment_score)
    fiscal_score = clamp(fiscal_score)
    external_score = clamp(external_score)
    
    # Calculate master score (weighted average)
    master_score = (
        monetary_score * 0.20 +
        inflation_score * 0.20 +
        currency_score * 0.10 +
        political_score * 0.15 +
        sentiment_score * 0.15 +
        fiscal_score * 0.10 +
        external_score * 0.10
    )
    
    # Determine regime based on master score and key metrics
    regime = 'Neutral'
    if master_score >= 70:
        regime = 'Risk-On' if sentiment_score >= 60 else 'Bullish'
    elif master_score >= 55:
        regime = 'Cautiously Optimistic'
    elif master_score <= 30:
        regime = 'Risk-Off' if sentiment_score <= 40 else 'Defensive'
    elif master_score <= 45:
        regime = 'Cautious'
    
    # Check for stagflation (low growth + high inflation signals)
    if inflation_score < 40 and monetary_score < 45:
        regime = 'Stagflation Watch'
    
    return {
        'center': {
            'score': round(master_score, 1),
            'label': 'Macro Score',
            'regime': regime,
            'breakdown': {
                'description': f'Composite macro health score aggregating {len(news_items)} news sources across 7 key metrics.',
                'market_implications': f'Current regime suggests a {regime.lower()} environment. ' + 
                    ('Favorable for risk assets with accommodative conditions.' if master_score >= 65 else
                     'Mixed conditions require selective positioning.' if master_score >= 45 else
                     'Defensive positioning recommended given elevated risks.'),
                'components': [
                    f'Monetary Policy: {round(monetary_score)}%',
                    f'Inflation/Growth: {round(inflation_score)}%', 
                    f'Currency: {round(currency_score)}%',
                    f'Politics: {round(political_score)}%',
                    f'Sentiment: {round(sentiment_score)}%',
                    f'Fiscal: {round(fiscal_score)}%'
                ]
            }
        },
        'hexagons': [
            {
                'position': 'top',
                'label': 'Monetary Policy',
                'score': round(monetary_score, 1),
                'detail': f'{round(monetary_score)}% favorable stance',
                'breakdown': {
                    'description': 'Central bank policy stance affecting liquidity and borrowing costs.',
                    'market_implications': generate_contextual_insight('Monetary Policy', monetary_score, news_items, country_code),
                    'data_points': _get_monetary_data_points(news_items, monetary_score),
                    'score_drivers': _generate_score_drivers(
                        [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['rate', 'fed', 'ecb', 'boj', 'monetary', 'policy'])][:3],
                        monetary_score, 'Monetary Policy'
                    ),
                    'top_sources': [{'title': item['title'], 'url': item.get('link', ''), 'publisher': item.get('publisher', 'Unknown')} 
                                    for item in [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['rate', 'fed', 'ecb', 'boj', 'monetary', 'policy'])][:3]]
                }
            },
            {
                'position': 'topRight',
                'label': 'Inflation & Growth',
                'score': round(inflation_score, 1),
                'detail': f'{round(inflation_score)}% growth outlook',
                'breakdown': {
                    'description': 'Assesses economic growth momentum, inflation trajectory, and stagflation risk through GDP, CPI, and employment data.',
                    'market_implications': generate_contextual_insight('Inflation & Growth', inflation_score, news_items, country_code),
                    'data_points': _get_inflation_data_points(news_items, inflation_score),
                    'score_drivers': _generate_score_drivers(
                        [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['inflation', 'cpi', 'gdp', 'growth', 'recession'])][:3],
                        inflation_score, 'Inflation & Growth'
                    ),
                    'top_sources': [{'title': item['title'], 'url': item.get('link', ''), 'publisher': item.get('publisher', 'Unknown')} 
                                    for item in [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['inflation', 'cpi', 'gdp', 'growth', 'recession'])][:3]]
                }
            },
            {
                'position': 'right',
                'label': 'Currency Strength',
                'score': round(currency_score, 1),
                'detail': f'{round(currency_score)}% strength',
                'breakdown': {
                    'description': 'Tracks currency valuation, FX interventions, and exchange rate stability impacting trade competitiveness.',
                    'market_implications': generate_contextual_insight('Currency Strength', currency_score, news_items, country_code),
                    'data_points': [
                        f"FX Sentiment: {'Strong' if currency_score > 60 else 'Weak' if currency_score < 40 else 'Stable'}",
                        f"Currency News Coverage: {len([item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['dollar', 'euro', 'yen', 'forex', 'fx', 'currency'])])} mentions"
                    ],
                    'score_drivers': _generate_score_drivers(
                        [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['dollar', 'euro', 'yen', 'forex', 'fx', 'currency'])][:3],
                        currency_score, 'Currency Strength'
                    ),
                    'top_sources': [{'title': item['title'], 'url': item.get('link', ''), 'publisher': item.get('publisher', 'Unknown')} 
                                    for item in [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['dollar', 'euro', 'yen', 'forex', 'fx', 'currency'])][:3]]
                }
            },
            {
                'position': 'bottomRight',
                'label': 'Political Risk',
                'score': round(political_score, 1),
                'detail': f'{round(political_score)}% stability',
                'breakdown': {
                    'description': 'Evaluates political stability, regulatory certainty, trade policy, and geopolitical tensions.',
                    'market_implications': generate_contextual_insight('Political Risk', political_score, news_items, country_code),
                    'data_points': [
                        f"Political Stability: {'High' if political_score > 60 else 'Moderate' if political_score > 40 else 'Elevated Risk'}",
                        f"Policy Events Tracked: {len([item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['election', 'government', 'political', 'tariff', 'trade war'])])} developments"
                    ],
                    'score_drivers': _generate_score_drivers(
                        [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['election', 'government', 'political', 'tariff', 'trade war', 'sanctions'])][:3],
                        political_score, 'Political Risk'
                    ),
                    'top_sources': [{'title': item['title'], 'url': item.get('link', ''), 'publisher': item.get('publisher', 'Unknown')} 
                                    for item in [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['election', 'government', 'political', 'tariff', 'trade war', 'sanctions'])][:3]]
                }
            },
            {
                'position': 'bottomLeft',
                'label': 'Investor Sentiment',
                'score': round(sentiment_score, 1),
                'detail': f'{round(sentiment_score)}% positive flows',
                'breakdown': {
                    'description': 'Measures market risk appetite, volatility levels, and positioning through equity flows and sentiment indicators.',
                    'market_implications': generate_contextual_insight('Investor Sentiment', sentiment_score, news_items, country_code),
                    'data_points': [
                        f"Risk Appetite: {'Risk-On' if sentiment_score > 60 else 'Risk-Off' if sentiment_score < 40 else 'Neutral'}",
                        f"Market Sentiment Coverage: {len([item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['market', 'stock', 'rally', 'selloff'])])} articles"
                    ],
                    'score_drivers': _generate_score_drivers(
                        [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['market', 'stock', 'rally', 'selloff', 'volatility'])][:3],
                        sentiment_score, 'Investor Sentiment'
                    ),
                    'top_sources': [{'title': item['title'], 'url': item.get('link', ''), 'publisher': item.get('publisher', 'Unknown')} 
                                    for item in [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['market', 'stock', 'rally', 'selloff', 'volatility'])][:3]]
                }
            },
            {
                'position': 'left',
                'label': 'Fiscal Health',
                'score': round(fiscal_score, 1),
                'detail': f'{round(fiscal_score)}% sustainability',
                'breakdown': {
                    'description': 'Analyzes government debt sustainability, deficit trends, and fiscal policy space for countercyclical measures.',
                    'market_implications': generate_contextual_insight('Fiscal Health', fiscal_score, news_items, country_code),
                    'data_points': [
                        f"Fiscal Condition: {'Strong' if fiscal_score > 60 else 'Concerning' if fiscal_score < 40 else 'Moderate'}",
                        f"Fiscal Policy News: {len([item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['debt', 'deficit', 'budget', 'spending', 'fiscal'])])} mentions"
                    ],
                    'score_drivers': _generate_score_drivers(
                        [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['debt', 'deficit', 'budget', 'spending', 'fiscal'])][:3],
                        fiscal_score, 'Fiscal Health'
                    ),
                    'top_sources': [{'title': item['title'], 'url': item.get('link', ''), 'publisher': item.get('publisher', 'Unknown')} 
                                    for item in [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['debt', 'deficit', 'budget', 'spending', 'fiscal'])][:3]]
                }
            },
            {
                'position': 'topLeft',
                'label': 'External Vulnerability',
                'score': round(external_score, 1),
                'detail': f'{round(external_score)}% resilience',
                'breakdown': {
                    'description': 'Assesses trade balance, foreign reserve adequacy, sanctions exposure, and dependence on external financing.',
                    'market_implications': generate_contextual_insight('External Vulnerability', external_score, news_items, country_code),
                    'data_points': [
                        f"External Risk: {'Low' if external_score > 60 else 'High' if external_score < 40 else 'Moderate'}",
                        f"Trade/Sanction News: {len([item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['trade', 'sanctions', 'tariff', 'reserves'])])} events"
                    ],
                    'score_drivers': _generate_score_drivers(
                        [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['trade', 'sanctions', 'tariff', 'reserves', 'balance'])][:3],
                        external_score, 'External Vulnerability'
                    ),
                    'top_sources': [{'title': item['title'], 'url': item.get('link', ''), 'publisher': item.get('publisher', 'Unknown')} 
                                    for item in [item for item in news_items if any(kw in (item['title'] + item.get('summary', '')).lower() for kw in ['trade', 'sanctions', 'tariff', 'reserves', 'balance'])][:3]]
                }
            }
        ]
    }
