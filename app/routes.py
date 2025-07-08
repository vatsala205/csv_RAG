from flask import Blueprint, render_template, request
from app.llama_rag import generate_sql, summarize_response
import sqlite3
import re

bp = Blueprint('main', __name__)

# Utility: Extract SQL query from LLaMA response
def extract_sql(text):
    # Try to extract SQL from ``` blocks first
    match = re.search(r"```sql\s+(.*?)```", text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()

    # If not in markdown format, extract the first valid-looking SQL line
    lines = text.splitlines()
    for line in lines:
        if line.strip().lower().startswith(("select", "insert", "update", "delete", "with", "create", "drop")):
            return line.strip()

    # Fallback: return whole text (last resort)
    return text.strip()

@bp.route('/', methods=['GET', 'POST'])
def index():
    answer = query = result = ""
    if request.method == 'POST':
        question = request.form['question']
        query = generate_sql(question)
        query = extract_sql(query)  # 🛠️ clean query before execution

        try:
            conn = sqlite3.connect("churn.db")
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            col_names = [description[0] for description in cursor.description]
            result = [dict(zip(col_names, row)) for row in rows]
            conn.close()
            answer = summarize_response(question, query, result[:5])
        except Exception as e:
            result = str(e)

    return render_template("index.html", query=query, result=result, answer=answer)
