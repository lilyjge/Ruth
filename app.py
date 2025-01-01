from flask import Flask, render_template, request, jsonify, session
from flask_session import Session

from constants import events, characters, menu_prompt, default_end, good_end

import thisllm
model = thisllm.LLM_Model()

# from sd import generate_scene
import os
cwd = os.getcwd()

from dotenv import load_dotenv
load_dotenv()
import base64

import sqlite3
from flask import g

app = Flask(__name__)
app.secret_key = base64.b64decode(bytes(os.environ.get('FLASK'), "utf-8"))
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions on the server filesystem
app.config["SESSION_FILE_DIR"] = "./flask_session"  # Directory for session files
app.config["SESSION_PERMANENT"] = False  # Sessions expire when the browser is closed
app.config["SESSION_USE_SIGNER"] = True  # Secure session cookies
Session(app)
# SESSION VARIABLES: index(event), char(name), prompt(sd), choice(for cur event), messages(all msgs, object form), save(if already loaded from homepage), end("done" for redirect, otherwise end type)

from thisrag import init_namespaces, add_memory

def gen_image(prompt, filename):
    # img = generate_scene(prompt)
    # img.save(f'{cwd}/static/{filename}.png')
    return

DATABASE = 'database.db'
NO_INTERACT_INDEX = 4

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db # connection

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.route('/api/slots', methods=['GET'])
def get_saves():
    ids = query_db("SELECT DISTINCT saveindex FROM summaries")
    slots = [{"filled": False, "thumbnail": None, "date": None}] * 6
    for id in ids:
        img_row = query_db("SELECT thumbnail, date FROM summaries WHERE saveindex = ?", [id["saveindex"]], one=True)
        slots[id["saveindex"]] = {"filled": True, "thumbnail": img_row["thumbnail"], "date": img_row["date"]}
    return jsonify(slots)

@app.route('/api/load', methods=['POST'])
def load():
    data = request.json
    saveindex = data.get("saveindex")
    if data.get("save"):
        session["save"] = True
    else:
        session["save"] = False

    session["messages"] = [] # clear message hsitory
    session["end"] = False
    model.clear_conv() # clear state

    row = query_db("SELECT event, char, choice FROM saves WHERE saveindex=? ORDER BY rowid DESC LIMIT 1", [saveindex], one=True) # last row with information on cur speaker
    session["index"] = row["event"]

    init_namespaces()
    summaries = query_db("SELECT char, sum, affection, awareness FROM summaries WHERE saveindex=? ", [saveindex])
    for summary in summaries:
        char = summary["char"]
        characters[char]["affection"] = summary["affection"]
        characters[char]["awareness"] = summary["awareness"]
        characters[char]["summary"] = summary["sum"]
        add_memory(summary["sum"], char)

    all_messages = query_db("SELECT event, choice, char, spk, msg FROM saves WHERE saveindex=? AND event<?", [saveindex, session["index"]]) # all messages not in state
    for msg in all_messages:
        m = {"event": msg["event"], "choice": msg["choice"], "char": msg["char"], "spk": msg["spk"], "msg": msg["msg"]}
        session["messages"].append(m)

    choice = row["choice"]
    if choice:
        data["inDialogue"] = True
        char = row["char"]
        cur_messages = query_db("SELECT spk, msg FROM saves WHERE saveindex=? AND event=?", [saveindex, session["index"]])

        result = events[session["index"]]["choices"][choice] 
        session["choice"] = choice
        session["prompt"] = result["stable_diffusion_prompt"]
        session["char"] = char
        last_msg = model.load_conv(cur_messages, result["llm_prompt"] + characters[char]["personality"], characters[char]["affection"], char)

        data["text"] = last_msg
        data["choices"] = []

        if_end = model.check_stats()
        if if_end["end"]:
            data["end"] = True
            end_conv()

        gen_image(session["prompt"], 'gameplay')

        return jsonify(data)
    else:
        return initialize()

@app.route('/api/save', methods=['POST'])
def save():
    data = request.json
    saveindex = data.get("saveindex")
    inDialogue = data.get("inDialogue")
    inEvent = data.get("inEvent")
    thumbnail = data.get("thumbnail")
    date = data.get("date")
    con = get_db()
    cur = con.cursor()

    cur.execute("DELETE FROM saves WHERE saveindex = ?", [saveindex])
    cur.execute("DELETE FROM summaries WHERE saveindex = ?", [saveindex])

    for name, charac in characters.items():
        cur.execute("INSERT INTO summaries (saveindex, char, sum, affection, awareness, thumbnail, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (saveindex, charac["name"], charac["summary"], charac["affection"], charac["awareness"], thumbnail, date))
    con.commit()
    
    if session["messages"]:
        for msg in session["messages"]:
            print("inserting session msg")
            cur.execute("INSERT INTO saves (saveindex, event, choice, char, spk, msg) VALUES (?, ?, ?, ?, ?, ?)",
                        (saveindex, msg["event"], msg["choice"], msg["char"], msg["spk"], msg["msg"]))
        con.commit()

    if inDialogue:
        messages = model.save_conv()
        index = session["index"]
        if not inEvent:
            index -= 1
        char = session["char"]
        for msg in messages:
            print("inserting history msg")
            cur.execute("INSERT INTO saves (saveindex, event, choice, char, spk, msg) VALUES (?, ?, ?, ?, ?, ?)",
                        (saveindex, index, session["choice"], char, msg[0], msg[1]))
        con.commit()
        print(query_db("SELECT msg FROM saves WHERE saveindex=?", [saveindex]))
    else:
        print("inserting indexes")
        cur.execute("INSERT INTO saves (saveindex, event) VALUES (?, ?)",
                        (saveindex, session["index"]))
        con.commit()

    return [True]

@app.route('/api/history', methods=['GET'])
def message_history():
    messages = []
    # print(session)
    for msg in session["messages"]:
        spk = "Ruth"
        if msg["spk"] == "ai":
            spk = msg["char"]
        elif msg["spk"] == "human":
            spk = "you"
        messages.append({"spk": spk, "msg": msg["msg"]})

    cur_msgs = model.save_conv()
    for msg in cur_msgs:
        spk = "you"
        if msg[0] == "ai":
            spk = session["char"]
        messages.append({"spk": spk, "msg": msg[1]})

    return jsonify({"messages": messages})

def check_end():
    good = []
    for charac in characters.values():
        if charac["affection"] >= 1000:
            good.append(charac["name"])
    if len(good) == 0:
        session["end"] = "Neutral"
        return default_end
    else:
        for charac in characters.values():
            if not (charac["name"] in good):
                good_end["choices"].pop(charac["name"].capitalize())
        session["end"] = "good"
        return good_end

@app.route('/api/initialize', methods=['POST'])
def initialize():
    index = session["index"]
    if session["end"]:
        if session["end"] == "done": # happens after else
            data = {}
            data["ended"] = True
            events.pop()
            return data
        else:
            data = {}
            data["choices"] = []
            data["inDialogue"] = False
            data["END"] = True
            data["text"] = session["end"].capitalize() + " End"
            session["end"] = "done"
            session["messages"].append({"event": session["index"], "choice": None, "char": "", "spk": "Ruth", "msg": data["text"]})
            session.modified = True
            return data
        
    data = {}
    if index == len(events):
        event = check_end()
        events.append(event)
        data["ending"] = True
    gen_image(events[index]["scene"], 'scene')
    
    items = []
    for choice, result in events[index]["choices"].items():
        items.append(choice)
    data["text"] = events[index]["description"]
    data["choices"] = items
    data["inDialogue"] = False
    session["messages"].append({"event": session["index"], "choice": None, "char": "", "spk": "Ruth", "msg": data["text"]})
    session.modified = True
    # print(session)
    return jsonify(data)

@app.route('/api/choice', methods=['POST'])
def handle_choice():
    data = request.json
    choice = data.get("choice")

    index = session["index"]
    session["choice"] = choice
    result = events[index]["choices"][choice] # character, llm prompt, sd prompt
    char = result["character"].lower()
    if choice == "" or index != NO_INTERACT_INDEX + 1:
        session["char"] = char
        session["prompt"] = result["stable_diffusion_prompt"]
    else:
        session["prompt"] = result["stable_diffusion_prompt"] + characters[session["char"]]["appearance"]

    gen_image(session["prompt"], 'gameplay')

    data = {}
    data["text"] = session["prompt"]
    data["choices"] = []

    if index == NO_INTERACT_INDEX + 1 and char != "":
        char = session["char"]

    if char == "" or index == NO_INTERACT_INDEX: 
        session["char"] = char
        end_conv()
        data["end"] = True
    else:
        model.begin_conv(result["llm_prompt"] + characters[char]["personality"], characters[char]["affection"], char)
    
    session["messages"].append({"event": session["index"], "choice": None, "char": "", "spk": "Ruth", "msg": data["text"]})

    return jsonify(data)

@app.route('/api/input', methods=['POST'])
def handle_input():
    data = request.json
    player_input = data.get("input")

    gen_image(session["prompt"], 'gameplay')

    output = model.respond(player_input)
    data["text"] = output
    data["choices"] = []
    if_end = model.check_stats()
    if if_end["end"]:
        data["end"] = True
        end_conv()
        
    return jsonify(data)

def end_conv():
    session["index"] += 1
    char = session["char"]
    if (not(char in characters.keys())) or session["index"] - 1 == NO_INTERACT_INDEX:
        return
    summary, msgs = model.end_conv()
    for msg in msgs:
        m = {"event": session["index"] - 1, "choice": session["choice"], "char": session["char"], "spk": msg[0], "msg": msg[1]}
        session["messages"].append(m)
    characters[char]["affection"] = summary["affection"]
    characters[char]["awareness"] += 1
    characters[char]["summary"] += " " + summary["summary"]

@app.route('/')
def do_stuff(): 
    if (not "save" in session) or (session["save"] == False):
        # print("resetting")
        session["index"] = 0
        session["char"] = ""
        session["messages"] = []
        session["choice"] = ""
        session["prompt"] = ""
        session["end"] = False
        model.clear_conv()
        init_namespaces()
    session["save"] = False
    return render_template('index.html')

@app.route('/home')
def serve_menu(): 
    gen_image(menu_prompt, 'menu')
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)