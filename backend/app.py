# from flask import Flask, request, jsonify
# import os
# import pandas as pd
# from pymongo import MongoClient
# from ml.forecast import run_forecast
# from rag.chat import handle_chat_query


# app = Flask(__name__)

# MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
# client = MongoClient(MONGO_URI)
# db = client["finance_db"]


# @app.route("/api/portfolio/upload", methods=["POST"])
# def upload_portfolio():

#     if "file" not in request.files:
#         return jsonify({"error": "No file part"}), 400

#     file = request.files["file"]

#     if file.filename == "":
#         return jsonify({"error": "No selected file"}), 400

#     if file and file.filename.endswith(".csv"):
#         try:
#             df = pd.read_csv(file)

#             portfolio_data = df.to_dict(orient="records")

#             # Store in MongoDB
#             db['portfolios'].insert_many(portfolio_data)

#             return jsonify({"status": "Portfolio uploaded successfully"}), 200
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
#     else:
#         return jsonify({"error": "Invalid file type, only CSV allowed"}), 400


# @app.route("/api/predictions/<ticker>", methods=["GET"])
# def get_predictions(ticker):
#     # Query the predictions collection
#     prediction_doc = db.predictions.find_one({"ticker": ticker}, sort=[("prediction_date", -1)])
#     if not prediction_doc:
#         return jsonify({"error": "No predictions found for ticker"}), 404
#     return jsonify(prediction_doc), 200


# @app.route("/api/chat", methods=["POST"])
# def chat():
#     user_query = request.json.get("query", "")
#     # Pass to RAG pipeline
#     response = handle_chat_query(user_query)
#     return jsonify({"answer": response})

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)



import os
import asyncio
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from data_pipeline.ingest_portfolio import process_portfolio
from data_pipeline.ingest_market import get_market_data
from data_pipeline.ingest_news import fetch_nse_news_newsapi
from data_pipeline.data_preparation import generate_stock_analysis

# Load environment variables
load_dotenv()

# Initialize Flask app
# app = Flask(__name__)
# CORS(app)

# Check if functions are async, then wrap them in sync calls
try:
    if asyncio.iscoroutinefunction(get_market_data):
        def get_market_data_sync(ticker):
            return asyncio.run(get_market_data(ticker))
    else:
        get_market_data_sync = get_market_data

    if asyncio.iscoroutinefunction(fetch_nse_news_newsapi):
        def fetch_nse_news_sync(ticker):
            return asyncio.run(fetch_nse_news_newsapi(ticker))
    else:
        fetch_nse_news_sync = fetch_nse_news_newsapi

except Exception as e:
    print(f"Error setting up async handling: {e}")

# @app.route('/analyze', methods=['POST'])
def analyze():
    """Handles portfolio file upload and performs market/news analysis."""
    
    # if 'file' not in request.files:
    #     return jsonify({"error": "No file uploaded"}), 400

    # # Process portfolio file
    # portfolio_file = request.files['file']

    portfolio_file = r"C:\Users\Eshaan\Downloads\elo-genai-project\backend\data_pipeline\iport.csv"
    portfolio, error = process_portfolio(portfolio_file)
    
    # if error:
    #     return jsonify({"error": error}), 400

    results = []

    for holding in portfolio:
        try:
            ticker = holding['ticker']
            print(f"🔍 Processing {ticker}...")

            # Ensure data is fetched synchronously
            market_data = get_market_data_sync(ticker)
            print(f"📈 Market Data for {ticker}: {market_data}")

            news_analysis = fetch_nse_news_sync(ticker)
            print(f"📰 News Analysis for {ticker}: {news_analysis}")

            # Prepare analysis context
            context = {
                "ticker": ticker,
                "market_trends": market_data,
                "news_summary": news_analysis,
            }
            
            # Perform stock analysis
            analysis = None
            # analysis = generate_stock_analysis(context)
            print(f"📊 Stock Analysis for {ticker}: {analysis}")

            results.append(analysis)

        except Exception as e:
            results.append({
                "ticker": ticker,
                "error": str(e)
            })
    
    # return jsonify(results)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    analyze()
