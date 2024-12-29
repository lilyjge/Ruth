import sqlite3

DATABASE = 'database.db'

connection = sqlite3.connect(DATABASE)
cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS saves(saveindex, event, choice, char, spk, msg)")
cur.execute("CREATE TABLE IF NOT EXISTS summaries(saveindex, char, sum, affection, awareness)")

connection.commit()
connection.close()

# rag stuff