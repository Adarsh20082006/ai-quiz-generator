# vector_service.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_faiss_index(article_text: str):
    """
    Build a FAISS vector index from article text using ultra-light local embeddings.
    - Free and low-memory (<200MB total usage)
    - Ideal for Render free tier (512MB)
    """

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    chunks = text_splitter.split_text(article_text)

    # Ultra-tiny multilingual embedding model
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L3-v2",  # lighter than paraphrase model
        cache_folder="/tmp"  # helps Render memory management
    )

    vector_store = FAISS.from_texts(chunks, embedding=embeddings)
    return vector_store, chunks
