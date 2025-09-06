from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from PIL import Image, ImageDraw, ImageFont
import os
import uuid
from diffusers import StableDiffusionPipeline
import torch

router = APIRouter()

# Optional cached Stable Diffusion pipeline loader
_sd_pipeline = None

def _get_sd_pipeline():
    global _sd_pipeline
    if _sd_pipeline is not None:
        return _sd_pipeline
    try:
        model_id = os.getenv("SD_MODEL_ID", 'prompthero/openjourney')
        device = "cuda" if torch.cuda.is_available() else "cpu"
        dtype = torch.float16 if device == "cuda" else torch.float32
        pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=dtype)
        print("pipe 2", pipe)
        if device == "cuda":
            pipe = pipe.to("cuda")
        else:
            # reduce memory usage on CPU
            try:
                pipe.enable_attention_slicing()
            except Exception:
                pass
        _sd_pipeline = pipe
        return _sd_pipeline
    except Exception:
        # diffusers not available or model load failed
        print("diffusers not available or model load failed")
        _sd_pipeline = None
        return None

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
    return {"text": text, "image_url": image_url, "engine": "pillow"}

@router.post("/text-to-image-v2")
def text_to_image_v2(request: TextToImageRequest):
    text = request.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text is required.")

    # Ensure the static directory exists
    os.makedirs("static", exist_ok=True)

    # Try using Stable Diffusion via diffusers if available; fall back to PIL text rendering
    image = None
    engine = "diffusers"

    pipe = _get_sd_pipeline()
    print("pipe", pipe)
    if pipe is not None:
        try:
            image = pipe(text).images[0]
        except Exception:
            image = None

    if image is None:
        engine = "pillow"
        img = Image.new('RGB', (512, 512), color=(255, 255, 255))
        d = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except Exception:
            font = ImageFont.load_default()
        d.text((10, 10), text, fill=(0, 0, 0), font=font)
        image = img

    filename = f"{uuid.uuid4().hex}.png"
    image_path = os.path.join("static", filename)
    image.save(image_path)
    image_url = f"/static/{filename}"

    return {"text": text, "image_url": image_url, "engine": engine}

