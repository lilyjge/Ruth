from flask import Flask, render_template, request, jsonify, session

from constants import events, characters

import thisllm
model = thisllm.LLM_Model()

# from sd import generate_scene

def display_menu(items):
    mapping = {}
    for choice, result in items:
        mapping[choice] = result
        print(choice)
    answer = input()
    return list(mapping.values())[int(answer)]

app = Flask(__name__)
app.secret_key = b'bb86f0d54acd8a8fde4338d5bd03946bc20875e02cb00f5af09d4d9e18a6fd60'

@app.route('/api/initialize', methods=['GET'])
def initialize():
    index = session["index"]
    items = []
    for choice, result in events[index]["choices"].items():
        items.append(choice)
    print("before generate", flush=True)
    # img = generate_scene(events[index]["scene"])
    # img.save("gameplay.png")
    print("after generate", flush=True)
    data = {}
    data["text"] = events[index]["description"]
    data["choices"] = items
    return jsonify(data)

@app.route('/api/choice', methods=['POST'])
def handle_choice():
    data = request.json
    choice = data.get("choice")

    index = session["index"]
    result = events[index]["choices"][choice] # character, llm prompt, sd prompt
    char = result["character"].lower()
    session["char"] = char
    model.begin_conv(result["llm_prompt"] + characters[char].personality, characters[char].affection, char)

    data = {}
    data["text"] = result["stable_diffusion_prompt"]
    data["choices"] = []

    return jsonify(data)

@app.route('/api/input', methods=['POST'])
def handle_input():
    data = request.json
    player_input = data.get("input")

    char = session["char"]
    output = model.respond(player_input)
    data["text"] = output
    data["choices"] = []
    if_end = model.check_stats()
    if if_end["end"]:
        data["end"] = True
        session["index"] += 1
        summary = model.end_conv()
        characters[char].affection = summary["affection"]
        characters[char].awareness += 1

    return jsonify(data)

@app.route('/')
def do_stuff():
    session["index"] = 0
    session["char"] = ""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)