from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

app = FastAPI()

# Mount static directory for serving images
app.mount("/static", StaticFiles(directory="static"), name="static")

PROJECT_INFO = {
    "name": "Sample FastAPI Project",
    "version": "1.0.0",
    "last_updated": "2025-09-05",
    "deployed": "2025-09-05",
    "author": "Your Name",
    "description": "A sample FastAPI project with info, hello, and text-to-image endpoints.",
    "server_time": datetime.now().isoformat(),
    "server": "FastAPI",
    "server_status": "running"
}

class TextToImageRequest(BaseModel):
    text: str

@app.get("/api/info")
def get_info():
    return PROJECT_INFO

@app.post("/api/text-to-image")
def text_to_image(request: TextToImageRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")
    # Generate image from text using PIL
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    d.text((10, 80), text, fill=(0, 0, 0), font=font)
    # Save image to static folder
    filename = f"{uuid.uuid4().hex}.png"
    image_path = os.path.join("static", filename)
    img.save(image_path)
    image_url = f"/static/{filename}"
    return {"text": text, "image_url": image_url}

class ClearImageRequest(BaseModel):
    filename: str

# New endpoint to clear/delete generated image
@app.post("/api/clear")
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

# The root endpoint
@app.get("/")
def serve_index():
    return FileResponse("static/index.html", media_type="text/html")
