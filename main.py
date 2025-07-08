from flask import Flask
from app.routes import bp
from app.database import load_csv_to_sqlite

app = Flask(__name__)
app.register_blueprint(bp)

# One-time load from CSV to DB
load_csv_to_sqlite()

if __name__ == '__main__':
    app.run(debug=True)
