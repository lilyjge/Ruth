from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import time
load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE'))

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