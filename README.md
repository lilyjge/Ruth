# Ruth's Super Amazing AI Adventure!

AI powered visual novel. Uses LangChain with Groq API for LLM text generation, Huggingface's diffusers library for image generation, Pinecone RAG for character memory, and SQLite database for saves. Runs locally, that is, your computer hosts the Flask server and the game runs as a web application in your browser. 

Disclaimer: I don't any responsibility for any of the AI generated content or the actions of any users.

## Requirements

- GPU for smooth gameplay
- [Python](https://www.python.org/downloads/) (tested with version 3.12)
- [Groq](https://console.groq.com/keys) API key
- [Pinecone](https://www.pinecone.io/) API key
- Flask secret key (you can generate one in terminal with python -c 'import secrets; print(secrets.token_hex())' )

## Installation

Open a terminal in the folder you want to install it in and enter the following commands:
```
git clone https://github.com/lilyjge/Ruth.git
cd Ruth
python -m venv venv
.\venv\Scripts\activate 
pip install -r requirements.txt
```

Make a file named .env in the Ruth folder to put your keys. It should look like this:
```
GROQ=...
PINECONE=...
FLASK=...
```
Alternatively, you can enter the keys in the terminal after running the program. You will only have to enter them once as they will be saved in a local database in the game directory. 

Next, run app.py with the following:
```
python app.py
```
Wait for it to load and it should open a tab in your default browser with the game.

Remember to quit the program from the terminal when you want to close it.

## Configuration

Click the settings button on the webpage.


## Troubleshooting

Observe the terminal output when app.py is ran. If the GPU is being used, "cuda" should be printed. If CPU is printed instead, run the following:
```
pip uninstall torch
```
Then go [here](https://pytorch.org/get-started/locally/) to install the appropriate version of PyTorch for your system. You only need torch, not torchvision nor torchaudio.

Be patient with it and don't click any buttons multiple times in a row. If a bug happens, reload the page or the program. Be warned the saving is not available until the introduction is done and when the ending begins.
