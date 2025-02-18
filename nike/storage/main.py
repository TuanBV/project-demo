from fastapi import FastAPI, UploadFile, File
import shutil
from datetime import datetime

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload an image file.
    """
    current_image = datetime.now().timestamp()
    file_path = f"./images/{current_image}_{file.filename}"
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_path": file_path}
