from constants import events, interlude, prologue, epilogue

import thisllm
from charac import Character
model = thisllm.LLM_Model()

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
    items = []
    for choice, result in event["choices"].items():
        oneChoice = (choice, result)
        items.append(oneChoice)
    result = display_menu(items)
    char = result["character"].lower()

    model.begin_conv(result["llm_prompt"] + characters[char].personality, characters[char].affection)
    while True:
        player_input = input()
        output = model.respond(player_input, char)
        print(output)
        if_end = model.check_stats(char)
        if if_end["end"]:
            break

    summary = model.end_conv(char)
    characters[char].affection = summary["affection"]
    characters[char].awareness += 1
