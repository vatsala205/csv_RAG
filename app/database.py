import pandas as pd
import sqlite3

def load_csv_to_sqlite(csv_path='data/churn.csv', db_path='churn.db'):
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql("customers", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()
# This function loads a CSV file into a SQLite database.