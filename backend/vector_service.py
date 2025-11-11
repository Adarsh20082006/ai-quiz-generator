# vector_service.py
import os
import gc
from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()  # for local dev (ignored on Render)

def build_faiss_index(article_text: str):
    """
    Build a FAISS vector index using OpenAI embeddings.
    - Uses text-embedding-3-small (lightweight)
    - Optimized for low-memory environments
    """

    # 1️⃣ Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=100,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    chunks = text_splitter.split_text(article_text)

    # 2️⃣ Initialize lightweight cloud embeddings
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )

    # 3️⃣ Create FAISS vector index
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)

    # 4️⃣ Free memory
    del embeddings
    gc.collect()

    return vector_store, chunks
