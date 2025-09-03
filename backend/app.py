from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import os

DB_PATH = os.getenv("DB_PATH", "./moodify.db")

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

@app.post("/predict/")
def save_post(post: Post):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO posts (platform, text, label) VALUES (?, ?, ?)",
              (post.platform, post.text, post.label))
    conn.commit()
    conn.close()
    return {"status": "ok", "saved": post}
