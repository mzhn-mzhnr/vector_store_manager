from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from langchain_community.document_loaders.parsers import PyMuPDFParser
from vector_store_manager.doc_prepare import preprocess_text, default_text_splitter
from langchain_core.documents import Document
from langchain_core.documents.base import Blob
from vector_store_manager.store import vector_store
from vector_store_manager.fileservice import upload_file

router = APIRouter()

pymupdf_parser = PyMuPDFParser()

@router.put("/files")
async def add_files(files: List[UploadFile] = File(...)):
    uploaded_files = []
    for file in files:
        if file.content_type == "application/pdf":
            contents = await file.read()
            file_id = upload_file(file.filename, contents, file.content_type)
            uploaded_files.append({
                "filename": file.filename, 
                "content_type": file.content_type
            })
            
            pages = [
                page.page_content for page in pymupdf_parser.lazy_parse(Blob.from_data(contents))
            ]
            
            documents = []
            
            page_number = 1
            for page in pages:
                if not page.strip():
                    page_number += 1
                    continue
               
                preproc = preprocess_text(page)
                splits = default_text_splitter.split_text(preproc)
                
                for split in splits:
                    documents.append(
                        Document(
                            page_content=split,
                            metadata={
                                "content_type": "application/txt",
                                "page_number": page_number,
                                "file_name": file.filename,
                                "file_id": file_id
                            }
                        )
                    )
                    
                page_number += 1
        
            for i in range(0, len(documents), 5000):
                vector_store.add_documents(documents=documents[i:i+5000])
        
            
    return (
        { 
            "message": "OK", 
            "data": { 
                "files": uploaded_files 
            }
        }
    )
    
@router.get("/files")
def get_all_files():
    docs = vector_store.get(include=['metadatas'])
    out = []
    unique_file_ids = set()  # Использование множества для уникальных file_id
    print("get metadata")
    for meta in docs['metadatas']:
        if meta['file_id'] not in unique_file_ids:
            out.append({
                "file_id": meta['file_id'],
                "file_name": meta['file_name'],
            })
            unique_file_ids.add(meta['file_id'])  # Добавление в множество
        
    return {"files": out}    

@router.delete("/files/{id}")
def remove_files(file_id: str):
    return vector_store._collection.delete(where={"file_id": file_id})