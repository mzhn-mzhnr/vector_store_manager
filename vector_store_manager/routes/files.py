from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from langchain_community.document_loaders.parsers import PyMuPDFParser
from vector_store_manager.doc_prepare import preprocess_text, default_text_splitter
from langchain_core.documents import Document
from langchain_core.documents.base import Blob
from vector_store_manager.store import vector_store

router = APIRouter()

pymupdf_parser = PyMuPDFParser()

@router.put("/files")
async def add_files(files: List[UploadFile] = File(...)):
    uploaded_files = []
    for file in files:
        if file.content_type == "application/pdf":
            contents = await file.read()
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
                
                preprocessed_page = preprocess_text(page)
                splits = default_text_splitter.split_text(preprocessed_page)
                
                for split in splits:
                    documents.append(
                        Document(
                            page_content=split,
                            metadata={
                                "page_number": page_number,
                                "file_name": file.filename,
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

@router.delete("/files/{id}")
def remove_files(id: str):
    return {"message": "OK"}