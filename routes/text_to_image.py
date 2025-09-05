from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import os
import uuid

router = APIRouter()

class TextToImageRequest(BaseModel):
    text: str

@router.post("/text-to-image")
def text_to_image(request: TextToImageRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")
    img = Image.new('RGB', (400, 200), color=(255, 255, 255))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()
    d.text((10, 80), text, fill=(0, 0, 0), font=font)
    filename = f"{uuid.uuid4().hex}.png"
    image_path = os.path.join("static", filename)
    img.save(image_path)
    image_url = f"/static/{filename}"
    return {"text": text, "image_url": image_url}