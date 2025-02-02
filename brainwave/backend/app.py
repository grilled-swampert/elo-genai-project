import os
import pandas as pd
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pymongo import MongoClient
from report_generator import create_financial_report
from datetime import datetime
import re
import matplotlib
import openai

matplotlib.use('Agg')  # Required for non-GUI environments

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})
os.makedirs("reports", exist_ok=True)

# ✅ OpenAI API Key
openai.api_key = "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"

# ✅ MongoDB Connection
try:
    client = MongoClient("mongodb+srv://pchintrate:vaYumGnRjKAsRHHF@cluster0.h4kyr.mongodb.net/?retryWrites=false&tls=true")
    db = client["company_data"]
    collection = db["financial_reports"]
    print("✅ MongoDB Connected Successfully!")
except Exception as e:
    print(f"❌ MongoDB Connection Failed: {e}")
    collection = None  # Prevent crashes

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
    if df.empty:
        raise ValueError("❌ Uploaded file is empty.")

    # ✅ Clean column names
    df.columns = [clean_column_name(col) for col in df.columns]

    # ✅ Check for required columns
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"❌ Missing required columns: {missing}")

    # ✅ Print raw date column before conversion (debugging)
    print("\n🔍 Raw Date Values Before Cleaning:", df["Date"].head(10).tolist())

    # ✅ If Date column contains only years, convert them to full dates
    if df["Date"].dtype in ["int64", "float64"]:
        df["Date"] = df["Date"].astype(int).astype(str) + "-01-01"  # Convert "2029" → "2029-01-01"

    # ✅ Try multiple date formats
    date_formats = ["%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"]
    for fmt in date_formats:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce", format=fmt)
        if df["Date"].notna().sum() > 0:
            break  # ✅ Stop once a working format is found

    # ✅ Filter out invalid dates
    df = df.dropna(subset=["Date"])

    # ✅ Print cleaned date column for verification
    print("\n✅ Cleaned Date Values After Conversion:", df["Date"].head(10).tolist())

    if df.empty:
        raise ValueError("❌ No valid dates found after cleaning. Please check the date format in the file.")

    return df[REQUIRED_COLUMNS]


@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "❌ No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "❌ No file selected"}), 400

    try:
        # ✅ Read file
        df = pd.read_csv(file) if file.filename.endswith(".csv") else pd.read_excel(file)

        print("\nOriginal columns:", df.columns.tolist())  # Debugging info

        # ✅ Clean and validate data
        df = clean_data(df)

        print("Cleaned columns:", df.columns.tolist())  # Debugging info
        print("First row:", df.iloc[0].to_dict())  # Debugging info

        # ✅ Handle edge cases for dataset size
        if len(df) < 2:
            raise ValueError("❌ Dataset must have at least 2 rows for analysis.")

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
        print(f"❌ Error trace: {str(e)}")
        return jsonify({"error": f"❌ Processing failed: {str(e)}"}), 500

@app.route("/download/<filename>", methods=["GET"])
def download_file(filename):
    """Handles PDF downloads properly."""
    file_path = os.path.join("reports", filename)
    if os.path.exists(file_path):
        return send_file(
            file_path,
            as_attachment=True,
            mimetype="application/pdf",  # ✅ Correct MIME type for PDF
            download_name=filename
        )
    return jsonify({"error": "❌ File not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
