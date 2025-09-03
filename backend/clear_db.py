import sqlite3

DB_PATH = "scraper.db"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
cur.execute("DELETE FROM posts")   
conn.commit()
conn.close()

print("Database cleared.")