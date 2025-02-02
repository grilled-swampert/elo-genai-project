import io
import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image, PageBreak
import openai

# ✅ OpenAI API Key (Updated for Latest API Version)
openai.api_key = "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"

# ✅ Color Themes
DARK_BLUE = "#2d3436"
ACCENT_BLUE = "#0984e3"
LIGHT_GRAY = "#dfe6e9"

def create_financial_report(output_path, df, total_revenue, total_profit, avg_stock_price, expenses):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        title="Financial Report",
        author="AutoReporter",
        subject="Company Performance Analysis"
    )
    elements = []
    styles = getSampleStyleSheet()
    
    # ✅ Custom Styles
    title_style = ParagraphStyle(
        "MainTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=colors.HexColor(DARK_BLUE),
        alignment=1,
        spaceAfter=24
    )

    # ✅ Dummy Company Information
    company_info = {
        "Company Name": "XYZ Corp.",
        "Registration No.": "XYZ-2025001",
        "GST No.": "GSTIN123456789",
        "Industry": "Technology",
        "Headquarters": "Silicon Valley, USA",
        "Year Established": "1998",
        "CEO/Founder": "John Doe",
        "Number of Employees": "15,000+",
        "Stock Symbol": "XYZ",
        "Website": "www.xyzcorporation.com"
    }

    # ✅ Cover Page (Company Details)
    elements.append(Paragraph("Company Financial Report", title_style))
    elements.append(Spacer(1, 0.5 * inch))

    # ✅ Add Company Information
    company_data = [[key, value] for key, value in company_info.items()]
    company_table = Table(company_data, colWidths=[3 * inch, 3 * inch])
    company_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(LIGHT_GRAY)),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black)
    ]))

    elements.append(company_table)
    elements.append(Spacer(1, 0.5 * inch))
    # elements.append(PageBreak())

    # ✅ Key Metrics
    elements.append(Paragraph("Executive Summary", styles["Heading2"]))
    metrics = [
        ["Total Revenue", f"${total_revenue:,.2f}M"],
        ["Net Profit", f"${total_profit:,.2f}M"],
        ["Average Stock Price", f"${avg_stock_price:,.2f}"],
        ["Total Expenses", f"${expenses:,.2f}M"],
        ["Reporting Period", f"{df['Date'].min().strftime('%b %Y')} to {df['Date'].max().strftime('%b %Y')}"]
    ]
    table = Table(metrics, colWidths=[3 * inch, 3 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(LIGHT_GRAY)),
        ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.black)
    ]))
    elements.append(table)
    elements.append(PageBreak())

    # ✅ Financial Charts
    add_financial_charts(elements, df)
    elements.append(PageBreak())

    # ✅ AI Analysis
    elements.append(Paragraph("Current Status", styles["Heading2"]))
    analysis = analysis
    elements.append(Paragraph(analysis, styles["Normal"]))

    elements.append(Paragraph("Suggested Action", styles["Heading2"]))
    analysis = generate_ai_analysis(df)
    elements.append(Paragraph(analysis, styles["Normal"]))

    doc.build(elements)

def add_financial_charts(elements, df):
    """Generates financial charts and adds them to the report."""
    
    # ✅ Revenue & Profit Trend
    fig, ax = plt.subplots(figsize=(10, 5))
    df.plot(x="Date", y=["Revenue (in million $)", "Profit (in million $)"], ax=ax, style=["-o", "-^"], linewidth=2)
    ax.set_title("Revenue & Profit Trends", fontsize=14)
    ax.set_ylabel("USD (Millions)")
    ax.grid(True, alpha=0.3)
    
    revenue_chart_buffer = io.BytesIO()
    plt.savefig(revenue_chart_buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    elements.append(Image(revenue_chart_buffer, width=6.5 * inch, height=4 * inch))

    # ✅ Stock Price Trend (Restored)
    fig, ax = plt.subplots(figsize=(10, 5))
    df.plot(x="Date", y="Stock Price ($)", kind="line", color=ACCENT_BLUE, linewidth=2, marker="o", ax=ax)
    ax.set_title("Stock Price Movement", fontsize=14)
    ax.set_ylabel("Stock Price ($)")
    ax.grid(True, alpha=0.3)
    
    stock_chart_buffer = io.BytesIO()
    plt.savefig(stock_chart_buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    elements.append(Image(stock_chart_buffer, width=6.5 * inch, height=4 * inch))

def generate_ai_analysis(df):
    """Generates AI-powered financial insights using OpenAI API"""
    try:
        analysis_prompt = f"""
        Analyze the following financial data for investment insights:

        - Revenue Growth: {((df['Revenue (in million $)'].iloc[-1]/df['Revenue (in million $)'].iloc[0])-1)*100:.1f}%
        - Profit Margin: {(df['Profit (in million $)'].sum()/df['Revenue (in million $)'].sum())*100:.1f}%
        - Stock Price Trend: {df['Stock Price ($)'].pct_change().mean()*100:.1f}%
        - Market Sentiment Analysis: {df['Market Sentiment'].value_counts().idxmax()}

        Provide:
        • Three key performance highlights
        • Two potential investment risks
        • Three strategic recommendations

        Format the response as bullet points for better readability.
        """

        # ✅ Explicitly passing API Key when initializing the client
        client = openai.OpenAI(api_key=openai.api_key)

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a financial analyst providing executive-level insights."},
                {"role": "user", "content": analysis_prompt}
            ],
            temperature=0.5,
            max_tokens=500
        )

        structured_response = response.choices[0].message.content

        # ✅ Convert response into bullet points
        structured_response = structured_response.replace("1.", "•").replace("2.", "•").replace("3.", "•")

        return structured_response

    except Exception as e:
        return f"AI Analysis Unavailable. Error: {str(e)}"
