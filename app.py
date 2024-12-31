from flask import Flask, render_template, request, jsonify, session

from constants import events, characters, menu_prompt

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

from thisrag import init_namespaces, add_memory
# SESSION VARIABLES: index(event), char(name), prompt(sd), choice(for cur event), messages(all msgs, object form), save(if already loaded from homepage)

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
    ids = query_db("SELECT DISTINCT saveindex FROM saves")
    slots = [False] * 6
    for id in ids:
        slots[id["saveindex"]] = True
    return slots

@app.route('/api/load', methods=['POST'])
def load():
    data = request.json
    saveindex = data.get("saveindex")
    if data.get("save"):
        session["save"] = True
    else:
        session["save"] = False

    session["messages"] = [] # clear message hsitory
    model.clear_conv() # clear state

    row = query_db("SELECT event, char, choice FROM saves WHERE saveindex=? ORDER BY rowid DESC LIMIT 1", [saveindex], one=True) # last row with information on cur speaker
    session["index"] = row["event"]

    init_namespaces()
    summaries = query_db("SELECT char, sum, affection, awareness FROM summaries WHERE saveindex=? ", [saveindex])
    for summary in summaries:
        char = summary["char"]
        characters[char]["affection"] = summary["affection"]
        characters[char]["awareness"] = summary["awareness"]
        characters["summary"] = summary["sum"]
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
    con = get_db()
    cur = con.cursor()

    cur.execute("DELETE FROM saves WHERE saveindex = ?", [saveindex])
    cur.execute("DELETE FROM summaries WHERE saveindex = ?", [saveindex])

    for charac in characters.values():
        cur.execute("INSERT INTO summaries (saveindex, char, sum, affection, awareness) VALUES (?, ?, ?, ?, ?)",
                    (saveindex, charac["name"], charac["summary"], charac["affection"], charac["awareness"]))
    con.commit()
    
    if session["messages"]:
        for msg in session["messages"]:
            print("inserting")
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
            print("inserting")
            cur.execute("INSERT INTO saves (saveindex, event, choice, char, spk, msg) VALUES (?, ?, ?, ?, ?, ?)",
                        (saveindex, index, session["choice"], char, msg[0], msg[1]))
        con.commit()
        print(query_db("SELECT msg FROM saves WHERE saveindex=?", [saveindex]))
    else:
        cur.execute("INSERT INTO saves (saveindex, event) VALUES (?, ?)",
                        (saveindex, session["index"]))
        con.commit()

    return [True]

@app.route('/api/history', methods=['GET'])
def message_history():
    messages = []

    for msg in session["messages"]:
        spk = "you"
        if msg["spk"] == "ai":
            spk = msg["char"]
        messages.append({"spk": spk, "msg": msg["msg"]})

    cur_msgs = model.save_conv()
    for msg in cur_msgs:
        spk = "you"
        if msg[0] == "ai":
            spk = session["char"]
        messages.append({"spk": spk, "msg": msg[1]})

    return jsonify({"messages": messages})

@app.route('/api/initialize', methods=['GET'])
def initialize():
    index = session["index"]
    gen_image(events[index]["scene"], 'scene')
    
    items = []
    for choice, result in events[index]["choices"].items():
        items.append(choice)
    data = {}
    data["text"] = events[index]["description"]
    data["choices"] = items
    data["inDialogue"] = False
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
    data["text"] = result["stable_diffusion_prompt"]
    data["choices"] = []

    if char == "" or index == NO_INTERACT_INDEX: 
        session["char"] = char
        end_conv()
        data["end"] = True
    else:
        model.begin_conv(result["llm_prompt"] + characters[char]["personality"], characters[char]["affection"], char)

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
    if char == "" or session["index"] - 1 == NO_INTERACT_INDEX:
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
        session["index"] = 0
        session["char"] = ""
        session["messages"] = []
        session["choice"] = ""
        session["prompt"] = ""
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