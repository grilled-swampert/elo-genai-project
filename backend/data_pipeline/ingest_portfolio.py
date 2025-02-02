import pandas as pd

def process_portfolio(file_stream):
    try:
        df = pd.read_csv(file_stream)
        
        # Validate required columns
        required = ['Ticker', 'Quantity', 'PurchasePrice']
        if not set(required).issubset(df.columns):
            return None, f"Missing columns: {set(required)-set(df.columns)}"
        
        # Convert to standardized format
        portfolio = []
        for _, row in df.iterrows():
            portfolio.append({
                "ticker": row['Ticker'].strip().upper(),
                "quantity": float(row['Quantity']),
                "purchase_price": float(row['PurchasePrice'])
            })
            
        return portfolio, None
    
    except Exception as e:
        return None, f"File processing error: {str(e)}"
    
