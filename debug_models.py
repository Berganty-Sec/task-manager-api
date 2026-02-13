import os
import sqlite3

db_path = os.path.abspath("./database.db")
print("Usando DB:", db_path)

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
print("Tabelas encontradas:", cursor.fetchall())
