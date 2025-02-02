import requests
import datetime
from newspaper import Article

# Set API Key for NewsAPI.org
news_api_key = "fa4a9d7493f84261a83c4d6a586ec31d"

def fetch_nse_news_newsapi(ticker):
    """Fetch latest news articles for NSE-listed stocks using NewsAPI.org"""
    
    url = f"https://newsapi.org/v2/everything?q={ticker}&language=en&sortBy=publishedAt&apiKey={news_api_key}"

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
                    news_articles.append({
                        "title": article["title"],
                        "url": article["url"]
                    })

                if len(news_articles) >= 3:
                    break  # Limit to 3 articles

    news_articles = news_articles if news_articles else [{"title": "No news found", "url": None}]

    for article in news_articles:
        article["content"] = scrape_news_content(article["url"])

    return news_articles


def scrape_news_content(url):
    """Scrape the full news content from the given URL using newspaper3k."""
    if url is None:
        return "No article found."

    try:
        article = Article(url)
        article.download()
        article.parse()

        return article.text  # Extracted full article content
    except Exception as e:
        print(f"⚠️ Error scraping {url}: {e}")
        return "Failed to retrieve article content."

# Main function to fetch news for NSE stocks and scrape full content
# def nse_investment_news():
#     tickers = ['GAYAPROJ', 'SASKEN', 'RELIANCE', 'TCS']  # Add more NSE tickers

#     news_dict = {}

#     for ticker in tickers:
#         articles = fetch_nse_news_newsapi(ticker)
        
#         # Scrape full content for each article
#         for article in articles:
#             article["content"] = scrape_news_content(article["url"])

#         news_dict[ticker] = articles

#     return news_dict

# # Run the function
# nse_news_results = nse_investment_news()

# articles = fetch_nse_news_newsapi("APP")
# print(articles)
# for article in articles:
#         print(f"🔹 Title: {article['title']}")
#         print(f"🔗 Link: {article['url']}")
#         print(f"📰 Full Content:\n{article['content']}\n" + "-"*80)


