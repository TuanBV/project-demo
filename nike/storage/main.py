import base64
import os
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

UPLOAD_DIR = "images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

class ImageRequest(BaseModel):
    """
        Model request image
    """
    filename: str
    data: str  # Dữ liệu Base64

@app.post("/upload/")
async def upload_image(image: ImageRequest):
    """
      Upload image
    """
    try:
        image_data = base64.b64decode(image.data)
        file_path = os.path.join(UPLOAD_DIR, image.filename)

        with open(file_path, "wb") as f:
            f.write(image_data)

        return {"filename": image.filename, "url": f"/images/{image.filename}"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/upload/{filename}")
async def get_uploaded_file(filename: str):
    """
      Get image
    """
    file_path = os.path.join(UPLOAD_DIR, filename)
    if os.path.exists(file_path):
        return {"message": "File exists", "url": f"/images/{filename}"}
    return {"error": "File not found"}
