from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from routes.info import router as info_router
from routes.text_to_image import router as text_to_image_router
from routes.clear import router as clear_router

app = FastAPI()

# Mount static directory for serving images
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(info_router, prefix="/api")
app.include_router(text_to_image_router, prefix="/api")
app.include_router(clear_router, prefix="/api")

# The root endpoint
@app.get("/")
def serve_index():
    return FileResponse("static/index.html", media_type="text/html")
