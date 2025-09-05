from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import os

router = APIRouter()

class ClearImageRequest(BaseModel):
    filename: str

@router.post("/clear")
def clear_image(request: ClearImageRequest):
    filename = request.filename.strip()
    if not filename or '/' in filename or '\\' in filename:
        raise HTTPException(status_code=400, detail="Invalid filename.")
    image_path = os.path.join("static", filename)
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found.")
    try:
        os.remove(image_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete image: {str(e)}")
    return {"detail": "Image deleted successfully."}