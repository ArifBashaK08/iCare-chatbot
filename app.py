from flask import Flask, jsonify, request
from src.helper import download_huggingface_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from dotenv import load_dotenv
from src.prompt import *
import os
from flask_cors import CORS
from langchain_google_genai import ChatGoogleGenerativeAI
import gradio as gr

load_dotenv()
HOST = os.environ.get("HOST")
BOT_NAME = os.environ.get("BOT_NAME")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL")

app = Flask(__name__)
CORS(app, origins=HOST)


embeddings = download_huggingface_embeddings()

# Stores the existing data from Pinecone
docsearch = PineconeVectorStore.from_existing_index(
    index_name=BOT_NAME, embedding=embeddings
)

# Gives 3 similar search results
retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Configuring OpenAI using Google's Gemini with streaming enabled
gemini_openai = ChatGoogleGenerativeAI(
    model=GEMINI_MODEL, google_api_key=GOOGLE_API_KEY, model_kwargs={"streaming": True}
)

# Creates a prompt template to use in RAG chain
prompt = ChatPromptTemplate.from_messages(
    [("system", SYSTEM_PROMPT), ("human", "{input}")]
)

# Creates a document QA chain
question_answer_chain = create_stuff_documents_chain(gemini_openai, prompt)

# Wraps the QA chain with a retriever - creating RAG chain
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


def chat_with_bot(question, history):
    if len(question) > 3000:
        return "⚠️ Your message is too long. Please keep it under 3000 characters."
    response = rag_chain.invoke({"input": question})
    return response["answer"]


interface = gr.ChatInterface(
    fn=chat_with_bot,
    title="ICare ChatBot",
    description="Ask health-related questions to the ICare LLM-powered bot. 🏥",
    type='messages'
)

interface.launch(share=True)
# @app.route("/", methods=["GET"])
# def index():
#     return jsonify({"message": "Flask backend is running"})


# @app.route("/chat", methods=["POST"])
# def chat():
#     data = request.get_json()
#     question = data.get("question")

#     if not question or not isinstance(question, str):
#         return jsonify({"error": "Invalid input message"}), 400

#     response = rag_chain.invoke({"input": question})
#     print(response)
#     return jsonify({"answer": response["answer"]})


# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8080, debug=True)
