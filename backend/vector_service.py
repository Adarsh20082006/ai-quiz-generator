# vector_service.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_faiss_index(article_text: str):
    """
    Builds a lightweight FAISS vector index from article text.
    - Uses a small local embedding model (no API key required)
    - Optimized for Render's free tier (low memory, CPU-friendly)
    """

    # Split text into small overlapping chunks for better context retention
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1500,  # smaller chunks → lower memory
        chunk_overlap=250,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    chunks = text_splitter.split_text(article_text)

    # Load a lightweight embedding model
    # ~80 MB memory footprint, perfect for Render free instance
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-MiniLM-L3-v2"
    )

    # Create FAISS vector store from text chunks
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)

    return vector_store, chunks
