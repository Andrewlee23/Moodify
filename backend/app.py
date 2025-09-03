from collections import Counter
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "./scraper.db")

app = FastAPI()

class Post(BaseModel):
    platform: str
    text: str
    label: str

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
   
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            text TEXT,
            label TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

from fastapi import FastAPI, Request
from predict import predict

app = FastAPI()

@app.post("/predict")
async def predict_text(request: Request):
    payload = await request.json()
    text = payload.get("text", "")
    if not text:
        return {"error": "No text provided"}
    return predict(text)

from collections import Counter
import sqlite3

@app.get("/mood-distribution")
def mood_distribution():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT prediction FROM posts")
    rows = cursor.fetchall()
    conn.close()

    predictions = [r[0] for r in rows if r[0] not in (None, "error")]

    counts = Counter(predictions)
    total = sum(counts.values())

    distribution = {
        mood: round((count / total) * 100, 2) if total > 0 else 0
        for mood, count in counts.items()
    }

    return {"total": total, "distribution": distribution}


