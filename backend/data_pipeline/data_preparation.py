from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
import json
from langchain.chains import LLMChain  # Keep using LLMChain

def generate_stock_analysis(context):
    llm = ChatOpenAI(
        temperature=0.2,
        model_name="gpt-3.5-turbo",
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )

    ticker = context['ticker']
    market_trends = context['market_trends']
    news_summary = context['news_summary']

    # Define the template
    template = """Analyze this stock position and provide structured response:

**Company**: {ticker}
**Market Trends**: {market_trends}
**Recent News Content**: {news_summary}

Generate JSON output with:
1. sector: Primary business sector (based on company's core operations)
2. majority_consensus_news: Overall market sentiment from news (1 sentence)
3. hot_in_sector: Top 3 trending stocks in identified sector
4. status_summary: Market position analysis (2-3 sentences with compulsory numerical (you can come up with realistic numbers yourself) probabilistic/confidence interval consistencies and reasonings)
5. action: Specific recommended trade action with rationale (2-3 sentences)
6. use rupees as the currency in your outputs wherever any price is involved

Example Output:
{{
  "ticker": "TSLA",
  "sector": "Automotive & Clean Energy",
  "majority_consensus_news": "Positive sentiment around battery tech innovations",
  "hot_in_sector": ["RIVN", "LCID", "NIO"],
  "status_summary": "Strong growth potential but facing supply chain challenges",
  "action": "Hold with 5% trailing stop-loss"
}}

JSON Output:
"""

    # Create the prompt template
    prompt = PromptTemplate(
        template=template,
        input_variables=["ticker", "market_trends", "news_summary"]
    )

    # Create the LLMChain
    chain = LLMChain(llm=llm, prompt=prompt)

    try:
        # Invoke the chain with the context
        result = chain.invoke({
            "ticker": ticker,
            "market_trends": market_trends,
            "news_summary": news_summary
        })
        
        print(result)
        return parse_json(result)
    
    except Exception as e:
        return {"error": str(e)}

def parse_json(text):
    try:
        # Extract JSON using more robust pattern matching
        json_str = text.split('JSON Output:')[-1].strip()
        json_str = json_str[json_str.find('{'):json_str.rfind('}')+1]
        return json.loads(json_str)
    except Exception as e:
        return {"error": f"JSON parsing failed: {str(e)}"}
