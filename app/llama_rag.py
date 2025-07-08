import os
import requests
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
LLAMA_MODEL = "meta-llama/llama-3-8b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "HTTP-Referer": "http://localhost",  # Change this if deployed
    "X-Title": "Churn SQL RAG App",
    "Content-Type": "application/json"
}


def generate_sql(question):
    schema = """
    Table: customers
    Columns:
    - customerID (TEXT)
    - gender (TEXT)
    - SeniorCitizen (INTEGER, 0 or 1)
    - Partner (TEXT, 'Yes' or 'No')
    - Dependents (TEXT, 'Yes' or 'No')
    - tenure (INTEGER, number of months)
    - PhoneService (TEXT, 'Yes' or 'No')
    - MultipleLines (TEXT)
    - InternetService (TEXT)
    - OnlineSecurity (TEXT)
    - OnlineBackup (TEXT)
    - DeviceProtection (TEXT)
    - TechSupport (TEXT)
    - StreamingTV (TEXT)
    - StreamingMovies (TEXT)
    - Contract (TEXT)
    - PaperlessBilling (TEXT)
    - PaymentMethod (TEXT)
    - MonthlyCharges (REAL)
    - TotalCharges (REAL)
    - Churn (TEXT, 'Yes' or 'No')
    """

    system_msg = f"""
You are an AI assistant that writes SQL queries for a SQLite database. The database has the following schema:
{schema}
Only use column names from the schema. Always check for values like 'Yes'/'No' when filtering text fields. Return queries that are valid SQLite.
"""

    payload = {
        "model": LLAMA_MODEL,
        "messages": [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": question}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()


def summarize_response(user_question, sql_query, result_rows):
    # Simple summarization fallback
    result_preview = str(result_rows[:3]) if result_rows else "No data returned."
    return (
        f"For your question: '{user_question}', I generated this SQL:\n"
        f"{sql_query}\nTop results:\n{result_preview}"
    )
