import webview
from flask import Flask, render_template, request, jsonify, session, stream_with_context, Response
from flask_session import Session

from constants import events, characters, menu_prompt, default_end, good_end, ruth
from initialize import init
init()
import thisllm
model = thisllm.LLM_Model()

import sd
art = sd.Art()
import os
cwd = os.getcwd()

from dotenv import load_dotenv
load_dotenv()
import base64

from threading import Timer

import sqlite3
from flask import g

import getpass

templatesDir = cwd + '/templates'
staticDir = cwd + '/static'

app = Flask(__name__, template_folder=templatesDir, static_folder=staticDir)
flask_key = os.environ.get('FLASK')
if not flask_key:
    flask_key = getpass.getpass("Enter secret key for Flask: ")
os.environ["FLASK"] = flask_key
app.secret_key = base64.b64decode(bytes(flask_key, "utf-8"))
app.config["SESSION_TYPE"] = "filesystem"  # Store sessions on the server filesystem
app.config["SESSION_FILE_DIR"] = "./flask_session"  # Directory for session files
app.config["SESSION_PERMANENT"] = False  # Sessions expire when the browser is closed
app.config["SESSION_USE_SIGNER"] = True  # Secure session cookies
Session(app)
# SESSION VARIABLES: index(event), char(name), prompt(sd), choice(for cur event), messages(all msgs, object form), save(if already loaded from homepage), end("done" for redirect, otherwise end type), gen(whether image currently being generated)

from thisrag import init_namespaces, add_memory

def gen_image(prompt, filename):
    if session["gen"]:
        return
    session["gen"] = True
    img = art.generate_scene(prompt)
    img.save(f'{cwd}/static/{filename}.png')
    session["gen"] = False
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

# Endpoint to get current settings
@app.route('/api/get-settings', methods=['GET'])
def get_settings():
    settings = query_db("SELECT resolution, steps, deformity, volume FROM settings", one=True)

    # Default settings if no data found
    if not settings:
        settings = {
            'resolution': 3,  # Medium
            'steps': 25,
            'deformity': False,
            'volume': 50
        }
    else:
        settings = {
            'resolution': settings["resolution"],
            'steps': settings['steps'],
            'deformity': settings["deformity"],
            "volume": settings["volume"]
        }
    # print(settings)
    return jsonify(settings)

@app.route('/api/save-settings', methods=['POST'])
def save_settings():
    data = request.json
    resolution = data.get('resolution', 3)
    steps = data.get('steps', 25)
    deformity = data.get('deformity', False)
    volume = data.get('volume', 50)

    # Save to database
    art.setValues(resolution, steps, deformity)
    con = get_db()
    cur = con.cursor()

    cur.execute("DELETE FROM settings")
    cur.execute("INSERT INTO settings (resolution, steps, deformity, volume) VALUES (?, ?, ?, ?)", [resolution, steps, deformity, volume])
    con.commit()

    return jsonify({'status': 'success'})

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
        session["gen"] = False
    else:
        session["save"] = False

    session["messages"] = [] # clear message hsitory
    session.pop("end", None)
    model.clear_conv() # clear state

    row = query_db("SELECT event, char, choice FROM saves WHERE saveindex=? ORDER BY rowid DESC LIMIT 1", [saveindex], one=True) # last row with information on cur speaker
    session["index"] = row["event"]

    init_namespaces()
    summaries = query_db("SELECT char, sum, affection FROM summaries WHERE saveindex=? ", [saveindex])
    for summary in summaries:
        char = summary["char"]
        characters[char]["affection"] = summary["affection"]
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
        
        event_msgs = cur_messages[:2] # first two elements
        for msg in event_msgs:
            m = {"event": session["index"], "choice": None, "char": "", "spk": msg["spk"], "msg": msg["msg"]}
            session["messages"].append(m)
        cur_messages = cur_messages[2:] # everything after first two elements

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

    for charac in characters.values():
        cur.execute("INSERT INTO summaries (saveindex, char, sum, affection, thumbnail, date) VALUES (?, ?, ?, ?, ?, ?)",
                    (saveindex, charac["name"], charac["summary"], charac["affection"], thumbnail, date))
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

@app.route('/api/endings', methods=['GET'])
def about_endings():
    messages = []
    for charac in characters.values():
        res = query_db("SELECT * FROM endings WHERE char = ?", [charac["name"]])
        for ending in res:
            if ending["type"] == "good":
                name = charac["name"].capitalize()
                messages.append(f"You've watched fireworks with {name}.")
            else:
                messages.append(charac["message"])
    if len(messages) == 6:
        messages.append(ruth)
    return jsonify({"messages": messages})

def check_end():
    good = []
    for charac in characters.values():
        if charac["affection"] >= 1000:
            good.append(charac["name"])
    if len(good) == 0:
        session["end"] = "neutral"
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
    if "end" in session and session["end"] != "begin bad":
        if session["end"] == "done": # happens after else
            data = {}
            data["ended"] = True
            events.pop(index - 1)
            return data
        else:
            data = {}
            data["choices"] = []
            data["inDialogue"] = False
            data["END"] = True
            data["text"] = session["end"].capitalize() + " End"
            if session["end"] != "neutral":
                res = query_db("SELECT * FROM endings WHERE char = ? AND type = ?", [session["char"], session["end"]])
                if res is None:
                    con = get_db()
                    cur = con.cursor()
                    cur.execute("INSERT INTO endings (char, type) VALUES (?, ?)", [session["char"], session["end"]])
                    con.commit()
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
    if index == NO_INTERACT_INDEX + 1:
        res = query_db("SELECT * FROM endings WHERE char = ?", [session["char"]])
        print(len(res))
        if len(res) == 2:
            items.append("Ask for the Truth")

    data["text"] = events[index]["description"]
    data["choices"] = items
    data["inDialogue"] = False
    session["messages"].append({"event": session["index"], "choice": None, "char": "", "spk": "Ruth", "msg": data["text"]})
    if "end" in session and session["end"] == "begin bad":
        session["end"] = "bad"
        data["ending"] = True
    if session["index"] <= NO_INTERACT_INDEX + 2:
        data["beginning"] = True
    elif "ending" not in data:
        data["middle"] = True
    session.modified = True
    # print(session["messages"])
    return jsonify(data)

@app.route('/api/choice', methods=['POST'])
def handle_choice():
    data = request.json
    choice = data.get("choice")

    index = session["index"]
    session["choice"] = choice
    if choice == "Ask for the Truth":
        data = {}
        data["text"] = "She falls silent for a moment. 'Do you really want to know? Well, I'll show you.'"
        model.power(characters[session["char"]]["personality"] + characters[session["char"]]["true"], characters[session["char"]]["affection"], session["char"])
        return data
    data = {}
    result = events[index]["choices"][choice] # character, llm prompt, sd prompt
    char = result["character"].lower()
    if char == "" or index != NO_INTERACT_INDEX + 1:
        session["char"] = char
        if index == 0 or index != NO_INTERACT_INDEX + 1:
            session["prompt"] = result["stable_diffusion_prompt"]
        data["text"] = result["stable_diffusion_prompt"]
    else: # at lunch, talk or truth
        session["prompt"] = result["stable_diffusion_prompt"] + characters[session["char"]]["appearance"]
        char = session["char"]
        data["text"] = session["prompt"]

    gen_image(session["prompt"], 'gameplay')

    data["choices"] = []        

    if char == "" or index == NO_INTERACT_INDEX or ("end" in session and session["end"] == "bad"):  # no talking option or seat picking
        session["char"] = char
        end_conv()
        data["end"] = True
    else:
        model.begin_conv(result["llm_prompt"] + characters[char]["personality"], characters[char]["affection"], char)
    
    session["messages"].append({"event": session["index"], "choice": None, "char": "", "spk": "Ruth", "msg": data["text"]})

    return jsonify(data)

@app.route('/api/input-data', methods=['POST'])
def save_input_data():
    data = request.json
    input_text = data.get("input")
    session["player_input"] = input_text  # Save input in session
    gen_image(session["prompt"], 'gameplay')
    return jsonify({"status": "Input received"}), 200

@app.route('/api/input', methods=['GET'])
def handle_input():
    player_input = session.pop("player_input", None)

    def generate_story():
        """Stream story text generation."""
        for chunk in model.respond(player_input):  # Assuming this yields chunks
            # print(chunk)
            yield f"data: {chunk}\n\n"
        yield "data: END_STREAM\n\n"

    response = Response(generate_story(), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    # response.headers["Connection"] = "keep-alive"
    response.headers["Content-Encoding"] = "none"
    return response

@app.route('/api/input/non-stream-data', methods=['POST'])
def fetch_non_stream_data():
    """Fetch the non-stream data for the completed request."""
    data = {}
    if_end = model.check_stats()
    if if_end["end"]:
        data["end"] = True
        end_conv()
    return jsonify(data)

def end_conv():
    session["index"] += 1
    char = session["char"]
    if (not(char in characters.keys())) or session["index"] - 1 == NO_INTERACT_INDEX or ("end" in session and session["end"] == "bad"):
        return
    summary, msgs = model.end_conv()
    for msg in msgs:
        m = {"event": session["index"] - 1, "choice": session["choice"], "char": session["char"], "spk": msg[0], "msg": msg[1]}
        session["messages"].append(m)
    characters[char]["affection"] = summary["affection"]
    characters[char]["summary"] += " " + summary["summary"]
    if characters[char]["affection"] <= 0:
        events.insert(session["index"], characters[char]["bad"])
        session["end"] = "begin bad"

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
        session["gen"] = False
        model.clear_conv()
        for name in characters:
            characters[name]["affection"] = 500
            characters[name]["summary"] = ""
        init_namespaces()
    session["save"] = False
    session.pop('end', None)
    return render_template('index.html')

@app.route('/home')
def serve_menu(): 
    session["gen"] = False
    settings = query_db("SELECT resolution, steps, deformity, volume FROM settings", one=True)

    # Default settings if no data found
    if not settings:
        art.setValues(3, 25, False)
    else:
        art.setValues(settings["resolution"], settings["steps"], settings["deformity"])
    gen_image(menu_prompt, 'menu')
    env = query_db("SELECT pinecone, groq, flask FROM env", one=True)
    if not env:
        con = get_db()
        cur = con.cursor()
        cur.execute("INSERT INTO env (pinecone, groq, flask) VALUES (?, ?, ?)", [os.environ["PINECONE"], os.environ["GROQ_API_KEY"], os.environ["FLASK"]])
        con.commit()
    return render_template('home.html')

class Api:

    def __init__(self):
        self._window = None

    def set_window(self, window):
        self._window = window

    def destroy(self):
        print('Destroying window..')
        self._window.destroy()
        print('Destroyed!')
        on_closed()

def on_closed():
    os._exit(1)

def run_server():
    app.run(debug=False)

if __name__ == '__main__':
    Timer(1, run_server).start()
    api = Api()
    window = webview.create_window("Ruth's Super Amazing AI Adventure!", "http://127.0.0.1:5000/home", js_api=api)
    api.set_window(window)
    window.events.closed += on_closed
    webview.start()
    