import sqlite3
import os

db_path = os.path.abspath("instance/database.db")
print("Usando DB:", db_path)

conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tabelas encontradas:", cur.fetchall())
