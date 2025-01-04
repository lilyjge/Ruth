import sqlite3

DATABASE = 'database.db'

connection = sqlite3.connect(DATABASE)
cur = connection.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS saves(saveindex, event, choice, char, spk, msg)")
cur.execute("CREATE TABLE IF NOT EXISTS summaries(saveindex, char, sum, affection, thumbnail, date)")
cur.execute("CREATE TABLE IF NOT EXISTS endings (char, type)")
cur.execute("CREATE TABLE IF NOT EXISTS settings (resolution, steps, deformity, volume)")

connection.commit()
connection.close()

from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import getpass
load_dotenv()
pc_key = os.getenv('PINECONE')
if not pc_key:
    pc_key = getpass.getpass("Enter API key for Pinecone: ")
pc = Pinecone(api_key=pc_key)

index_name = "ruth"

if index_name in pc.list_indexes().names():
    pc.delete_index(index_name)

pc.create_index(
    name=index_name,
    dimension=768, # Replace with your model dimensions
    metric="cosine", # Replace with your model metric
    spec=ServerlessSpec(
        cloud="aws",
        region="us-east-1"
        ) 
)

from diffusers import StableDiffusionPipeline
pipeline = StableDiffusionPipeline.from_single_file("https://huggingface.co/mdl-mirror/dark-sushi-mix/blob/main/darkSushiMixMix_darkerPruned.safetensors")