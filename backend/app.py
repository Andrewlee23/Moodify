from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os
from collections import Counter
from predict import predict

DB_PATH = os.getenv("DB_PATH", "./scraper.db")

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])  # frontend

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS posts")
    c.execute("""
        CREATE TABLE posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT,
            text TEXT,
            label TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.before_request
def before_request():
    # initialize DB if it doesn't exist
    if not os.path.exists(DB_PATH):
        init_db()

@app.route("/predict", methods=["POST"])
def predict_text():
    data = request.json
    text = data.get("text", "")
    if not text:
        return jsonify({"error": "No text provided"}), 400

    result = predict(text)

    # store in DB
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO posts (source, text, label) VALUES (?, ?, ?)",
              ("api", text, result["label"]))
    conn.commit()
    conn.close()

    return jsonify(result)

@app.route("/mood-distribution", methods=["GET"])
def mood_distribution():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT label FROM posts")
    rows = cur.fetchall()
    conn.close()

    labels = [r[0] for r in rows if r[0] not in (None, "error")]
    counts = Counter(labels)
    total = sum(counts.values())

    distribution = {
        mood: round((count / total) * 100, 2) if total > 0 else 0.0
        for mood, count in counts.items()
    }

    return jsonify({"total": total, "distribution": distribution})

if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=8000, debug=True)
