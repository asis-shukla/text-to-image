from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

PROJECT_INFO = {
    "name": "Text-to-Image Web Application",
    "version": "1.0.0",
    "last_updated": "2025-09-05",
    "deployed": "2025-09-05",
    "author": "Your Name",
    "description": "A FastAPI project to generate images from text.",
    "server_time": datetime.now().isoformat(),
    "server": "FastAPI",
    "server_status": "running"
}

@router.get("/info")
def get_info():
    return PROJECT_INFO