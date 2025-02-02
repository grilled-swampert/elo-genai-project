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
from pymongo import MongoClient
import pandas as pd
import datetime
import re
import matplotlib
from report_generator import create_financial_report

# Load environment variables
load_dotenv()

matplotlib.use('Agg') 

try:
    client = MongoClient("mongodb+srv://pchintrate:vaYumGnRjKAsRHHF@cluster0.h4kyr.mongodb.net/?retryWrites=false&tls=true")
    db = client["company_data"]
    collection = db["financial_reports"]
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")
    collection = None  # Prevent crashes if MongoDB fails



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







# ✅ Required Columns
REQUIRED_COLUMNS = [
    "Date",
    "Revenue (in million $)",
    "Profit (in million $)",
    "Stock Price ($)",
    "Market Sentiment",
    "Number of New Customers",
    "Customer Retention Rate (%)",
    "Expenses (in million $)"
]

def clean_column_name(col):
    """Standardize column names using multiple replacement rules"""
    col = re.sub(r'[^a-zA-Z0-9$%() ]+', '', col)  # Remove special chars
    col = re.sub(r'\s+', ' ', col).strip()  # Normalize whitespace

    # ✅ Flexible matching for key columns
    replacements = {
        r'(?i)revenue.*million': 'Revenue (in million $)',
        r'(?i)profit.*million': 'Profit (in million $)',
        r'(?i)stock.*price': 'Stock Price ($)',
        r'(?i)market.*sentiment': 'Market Sentiment',
        r'(?i)number.*new.*customers': 'Number of New Customers',
        r'(?i)customer.*retention.*rate': 'Customer Retention Rate (%)',
        r'(?i)expenses.*million': 'Expenses (in million $)',
        r'(?i)date': 'Date'
    }
    
    for pattern, replacement in replacements.items():
        if re.search(pattern, col):
            return replacement
    return col

def clean_data(df):
    """Process and validate dataframe"""
    # ✅ Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]
    
    # ✅ Check for required columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # ✅ Convert and filter dates
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='%Y-%m-%d')
    df = df.dropna(subset=['Date'])
    
    return df[REQUIRED_COLUMNS]

# @app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # ✅ Read file
        df = pd.read_csv(file) if file.filename.endswith(".csv") else pd.read_excel(file)

        print("\nOriginal columns:", df.columns.tolist())  # Debugging info

        # ✅ Clean and validate data
        df = clean_data(df)

        print("Cleaned columns:", df.columns.tolist())  # Debugging info
        print("First row:", df.iloc[0].to_dict())  # Debugging info

        # ✅ Store in database (only if collection exists)
        if collection is not None:
            collection.insert_many(df.to_dict(orient="records"))

        # ✅ Generate report
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"Company_Report_{timestamp}.pdf"
        pdf_path = os.path.join("reports", filename)

        create_financial_report(
            pdf_path,
            df,
            total_revenue=df["Revenue (in million $)"].sum(),
            total_profit=df["Profit (in million $)"].sum(),
            avg_stock_price=df["Stock Price ($)"].mean(),
            expenses=df["Expenses (in million $)"].sum()
        )

        return jsonify({
            "pdfUrl": f"http://127.0.0.1:5000/download/{filename}",
            "filename": filename
        })

    except Exception as e:
        print(f"Error trace: {str(e)}")
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500

# @app.route("/download/<filename>", methods=["GET"])
# def download_file(filename):
#     """Handles PDF downloads properly."""
#     file_path = os.path.join("reports", filename)
#     if os.path.exists(file_path):
#         return send_file(
#             file_path,
#             as_attachment=True,
#             mimetype="application/pdf",  # ✅ Correct MIME type for PDF
#             download_name=filename
#         )
#     return jsonify({"error": "File not found"}), 404







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
            # analysis = None
            analysis = generate_stock_analysis(context)
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
