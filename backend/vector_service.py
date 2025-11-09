# vector_service.py
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


def build_faiss_index(article_text: str):
    """
    Build a FAISS vector index from article text using local Hugging Face embeddings.
    - No external API calls
    - Works offline
    """

    # Split text into manageable chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=400,
        separators=["\n\n", "\n", ".", "!", "?"]
    )
    chunks = text_splitter.split_text(article_text)

    # Use local sentence-transformer model for embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Create FAISS vector store
    vector_store = FAISS.from_texts(chunks, embedding=embeddings)

    return vector_store, chunks
