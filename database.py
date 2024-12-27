from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv
import os
import time
load_dotenv()
pc = Pinecone(api_key=os.getenv('PINECONE_API'))

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

# data = [
#     {"id": "vec1", "text": "Apple is a popular fruit known for its sweetness and crisp texture."},
#     {"id": "vec2", "text": "The tech company Apple is known for its innovative products like the iPhone."},
#     {"id": "vec3", "text": "Many people enjoy eating apples as a healthy snack."},
#     {"id": "vec4", "text": "Apple Inc. has revolutionized the tech industry with its sleek designs and user-friendly interfaces."},
#     {"id": "vec5", "text": "An apple a day keeps the doctor away, as the saying goes."},
#     {"id": "vec6", "text": "Apple Computer Company was founded on April 1, 1976, by Steve Jobs, Steve Wozniak, and Ronald Wayne as a partnership."}
# ]

# # generating vectors
# embeddings = pc.inference.embed(
#     model="multilingual-e5-large",
#     inputs=[d['text'] for d in data],
#     parameters={"input_type": "passage", "truncate": "END"}
# )
# print(embeddings[0])

# # Wait for the index to be ready
# while not pc.describe_index(index_name).status['ready']:
#     time.sleep(1)

# index = pc.Index(index_name)

# # preparing records for upset
# vectors = []
# for d, e in zip(data, embeddings):
#     vectors.append({
#         "id": d['id'],
#         "values": e['values'],
#         "metadata": {'text': d['text']}
#     })

# index.upsert(
#     vectors=vectors,
#     namespace="ns1"
# )