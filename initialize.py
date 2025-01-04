import sqlite3

def init():

    DATABASE = 'database.db'

    connection = sqlite3.connect(DATABASE)
    cur = connection.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS saves(saveindex, event, choice, char, spk, msg)")
    cur.execute("CREATE TABLE IF NOT EXISTS summaries(saveindex, char, sum, affection, thumbnail, date)")
    cur.execute("CREATE TABLE IF NOT EXISTS endings (char, type)")
    cur.execute("CREATE TABLE IF NOT EXISTS settings (resolution, steps, deformity, volume)")

    connection.commit()
    connection.close()
    