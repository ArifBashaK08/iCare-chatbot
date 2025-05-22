# ==================== RUN THIS FILE ONLY ONCE ==================== #

# In the beginning - Run this file to upload data in PineconeDB
# This is used to tokenize the data/file and upload those on the vectorDB - PineconeDB

# ==================== xxxxxxxxxxxxxxxxxxxxxxx ==================== #

import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from src.helper import load_pdf_file, tokenizer, download_huggingface_embeddings

load_dotenv()
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY

extracted_data = load_pdf_file(data="Data/")
tokens = tokenizer(extracted_data)
embeddings = download_huggingface_embeddings()

pc = Pinecone(api_key=PINECONE_API_KEY)
index_name = "icarechatbot"

pc.create_index(
    name=index_name,
    dimension=384,  # Replace with your model dimensions
    metric="cosine",  # Replace with your model metric
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)

docsearch = PineconeVectorStore.from_documents(
    documents=tokens, index_name=index_name, embedding=embeddings
)
