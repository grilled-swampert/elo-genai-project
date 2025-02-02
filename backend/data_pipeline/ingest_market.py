import os
import requests

def get_market_data(ticker):
    """Simple market data fetcher"""
    try:
        api_key = '3eAai8EH0P6cgZKVqN3B0YAycxmTVWhw'
        url = f"https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={api_key}"
        data = requests.get(url).json()
        data['historical'] = data['historical'][:14]
        print("market")

        # print(data)
        # quote = data.get('Global Quote', {})
        # return {
        #     'price': quote.get('05. price', 'N/A'),
        #     'change': quote.get('10. change percent', 'N/A')
        # }
    except:
        return {'error': 'Failed to fetch market data'}
    
# get_market_data("AAPL")