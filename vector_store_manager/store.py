import chromadb
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from chromadb.config import Settings
import vector_store_manager.config as config

# Инициализация эмбеддингов с использованием модели из конфигурации
embeddings = HuggingFaceEmbeddings(
    model_name=config.EMBEDDING_MODEL,
)

# Создание клиента для подключения к ChromaDB
client = chromadb.HttpClient(
    host=config.CHROMA_HOST,
    port=config.CHROMA_PORT,
    settings=Settings(
        chroma_client_auth_provider="chromadb.auth.basic_authn.BasicAuthClientProvider",
        chroma_client_auth_credentials=config.CHROMA_CREDS
    )
)

# Инициализация векторного хранилища с использованием клиента и функции эмбеддингов
vector_store = Chroma(
    client=client,
    embedding_function=embeddings,    
)