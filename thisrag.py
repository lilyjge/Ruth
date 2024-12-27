from langchain_huggingface import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")

from langchain_pinecone import PineconeVectorStore
from langchain.docstore.document import Document
from pinecone import Pinecone, ServerlessSpec
import os
from dotenv import load_dotenv
load_dotenv()
index_name = "ruth"

pc = Pinecone(api_key=os.getenv('PINECONE_API'))

index = pc.Index(index_name)

vector_store = PineconeVectorStore(embedding=embeddings, index=index)

def retrieve(question, name):
    retrieved = vector_store.similarity_search(question, namespace=name)
    # print(f"question {question}, name {name.lower()}, found {retrieved}")
    return retrieved

def add_memory(summary, name):
    doc = Document(page_content=summary)
    # print(doc)
    document_ids = vector_store.add_documents(documents=[doc], namespace=name)
    # print(document_ids)

if __name__ == "__main__":
    from langchain_community.document_loaders import DirectoryLoader
    from langchain_community.document_loaders import TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,  # chunk size (characters)
        chunk_overlap=40,  # chunk overlap (characters)
        add_start_index=True,  # track index in original document
    )

    loader = DirectoryLoader("lore/", glob="**/interlude.txt", loader_cls=TextLoader)
    docs = loader.load()
    print(docs[0])
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store.add_documents(documents=all_splits, namespace="interlude")
    print(document_ids[:3])

    loader = DirectoryLoader("lore/", glob="**/prologue.txt", loader_cls=TextLoader)
    docs = loader.load()
    print(docs[0])
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store.add_documents(documents=all_splits, namespace="prologue")
    print(document_ids[:3])

    loader = DirectoryLoader("lore/", glob="**/epilogue.txt", loader_cls=TextLoader)
    docs = loader.load()
    print(docs[0])
    all_splits = text_splitter.split_documents(docs)
    document_ids = vector_store.add_documents(documents=all_splits, namespace="epilogue")
    print(document_ids[:3])