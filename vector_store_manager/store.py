from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from vector_store_manager.config import EMBEDDING_MODEL

embeddings = HuggingFaceEmbeddings(
    model_name=EMBEDDING_MODEL,
)

vector_store = Chroma(
    embedding_function=embeddings,
    persist_directory="./chroma"
)