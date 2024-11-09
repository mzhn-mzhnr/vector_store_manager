import os
import time
import regex as re
import nltk
from langchain_community.document_loaders import PyMuPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, SnowballStemmer

nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

stop_words = set(stopwords.words('russian') + stopwords.words('english'))
en_stemmer = PorterStemmer()
ru_stemmer = SnowballStemmer("russian")

def preprocess_text(text):
    """ Предобрабатывает текст, преобразуя его в нижний регистр, удаляя специальные символы, 
        токенизуя и стеммируя."""
    text = text.lower()
    text = re.sub(r"[^\w\s\p{Sc}%#@&*()+/\-]+", "", text, flags=re.UNICODE)
    words = word_tokenize(text)
    
    # processed_words = [
    #     (ru_stemmer.stem(word) if re.match(r'[а-яё]', word) else
    #      en_stemmer.stem(word) if re.match(r'^[a-z]+$', word) else word)
    #     for word in words if word not in stop_words
    # ]
    
    processed_words = words
    return ' '.join(processed_words)

default_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)