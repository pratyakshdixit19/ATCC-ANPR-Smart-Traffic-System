from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import numpy as np
import cv2
from PIL import Image
import io

app = FastAPI()

# ✅ Allow React frontend to access this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://localhost:5173"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Welcome to ANPR Backend"}

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = np.array(Image.open(io.BytesIO(contents)))

    reader = easyocr.Reader(['en'])
    results = reader.readtext(image)

    plate_text = " ".join([res[1] for res in results]) if results else "No plate detected"
    return {"plate_number": plate_text}
