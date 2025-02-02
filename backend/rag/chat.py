
import requests
import datetime

# Set API Key for NewsAPI.org
news_api_key = "fa4a9d7493f84261a83c4d6a586ec31d"

def fetch_nse_news_newsapi(ticker):
    """Fetch latest news articles for NSE-listed stocks using NewsAPI.org"""
    
    # Use 'everything' endpoint for broader results
    url = f"https://newsapi.org/v2/everything?q={ticker} NSE India&sortBy=publishedAt&apiKey={news_api_key}"

    response = requests.get(url)
    data = response.json()

    # Debugging: Check raw response
    # print(f"🔍 Searching for: {ticker} NSE stock news")
    # print(f"📡 Raw API Response: {data}")

    news_articles = []
    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)

    if "articles" in data:
        for article in data["articles"]:
            if "url" in article and "publishedAt" in article:
                published_date = datetime.datetime.strptime(article["publishedAt"], "%Y-%m-%dT%H:%M:%SZ")

                # Filter for news within the last 2 weeks
                if published_date >= two_weeks_ago:
                    news_articles.append(article["url"])

                if len(news_articles) >= 3:
                    break  # Limit to 3 articles

    return news_articles if news_articles else ["No news found"]

# Main function to fetch news for NSE stocks
def nse_investment_news():
    tickers = ['GAYAPROJ', 'SASKEN', 'RELIANCE', 'TCS']  # Add more NSE tickers as needed

    news_dict = {}

    for ticker in tickers:
        news_dict[ticker] = fetch_nse_news_newsapi(ticker)

    return news_dict

# Run the function
nse_news_results = nse_investment_news()

# Print output
print(nse_news_results)
