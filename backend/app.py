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


