from fastapi import APIRouter
from pydantic import BaseModel, Field
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List

router = APIRouter()

@router.put("/files")
async def add_files(files: List[UploadFile] = File(...)):
    uploaded_files = []
    for file in files:
        contents = await file.read()
        uploaded_files.append({"filename": file.filename, "content_type": file.content_type})
        
    return { "message": "OK", "data": { "files": uploaded_files }}

@router.delete("/files/{id}")
def remove_files(id: str):
    return {"message": "OK"}