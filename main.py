from constants import events, interlude, prologue, epilogue
# from PIL import Image
from sd import generate_scene
import thisllm
from charac import Character
model = thisllm.LLM_Model()
import os
cwd = os.getcwd()

characters = {}
characters["interlude"] = Character("Interlude", interlude)
characters["prologue"] = Character("Prologue", prologue)
characters["epilogue"] = Character("Epilogue", epilogue)

def display_menu(items):
    mapping = {}
    for choice, result in items:
        mapping[choice] = result
        print(choice)
    answer = input()
    return list(mapping.values())[int(answer)]

for event in events:
    description = event["description"]
    print(description)
    img = generate_scene(event["scene"])
    img.save(f'{cwd}/static/scene.png')
    items = []
    for choice, result in event["choices"].items():
        oneChoice = (choice, result)
        items.append(oneChoice)
    result = display_menu(items)
    char = result["character"].lower()

    model.begin_conv(result["llm_prompt"] + characters[char].personality, characters[char].affection, char)
    while True:
        img = generate_scene(result["stable_diffusion_prompt"])
        img.save(f'{cwd}/static/gameplay.png')
        player_input = input()
        print("done generating")
        output = model.respond(player_input)
        print(output)
        if_end = model.check_stats()
        if if_end["end"]:
            break

    summary = model.end_conv()
    characters[char].affection = summary["affection"]
    characters[char].awareness += 1
