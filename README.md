```rag_sql_churn/
├── app/
│   ├── __init__.py
│   ├── routes.py
│   ├── database.py
│   └── openai_rag.py
├── templates/
│   └── index.html
├── static/
│   └── style.css
├── data/
│   └── churn.csv
├── churn.db                ← SQLite database created from your CSV
├── main.py                 ← Run Flask app
├── requirements.txt
└── .env                    ← Store your OpenAI API key
```
a SQL-RAG: natural language → GPT generates SQL → run SQL → summarize result → natural language answer.

**🧪 How to Run This**



python3 -m venv venv && source venv/bin/activate

pip install -r requirements.txt

Create .env and paste your OpenAI key

Place churn.csv in data/

python main.py

Go to http://127.0.0.1:5000/ in your browser