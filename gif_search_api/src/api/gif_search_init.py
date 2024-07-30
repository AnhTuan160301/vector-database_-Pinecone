import os

import pinecone
from sentence_transformers import SentenceTransformer


def init_pinecone(key: str):
    # find API key at app.pinecone.io
    pc = pinecone.Pinecone(api_key=key, environment="us-west1-gcp")
    return pc.Index('gif-search')


def init_retriever():
    return SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


api_key = os.getenv("PINECONE_API_KEY")

index = init_pinecone(key=api_key)
retriever = init_retriever()
