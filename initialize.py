import sqlite3
import os

def init():

    DATABASE = 'database.db'

    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS saves(saveindex, event, choice, char, spk, msg)")
    cur.execute("CREATE TABLE IF NOT EXISTS summaries(saveindex, char, sum, affection, thumbnail, date)")
    cur.execute("CREATE TABLE IF NOT EXISTS endings (char, type)")
    cur.execute("CREATE TABLE IF NOT EXISTS settings (resolution, steps, deformity, volume)")
    cur.execute("CREATE TABLE IF NOT EXISTS env (pinecone, groq, flask)")
    connection.row_factory = sqlite3.Row
    cur = connection.execute("SELECT pinecone, groq, flask FROM env")
    rv = cur.fetchall()
    if rv:
        os.environ["PINECONE"] = rv[0]["pinecone"]
        os.environ["GROQ_API_KEY"] = rv[0]["groq"]
        os.environ["FLASK"] = rv[0]["flask"]

    connection.commit()
    connection.close()
    