from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.responses import JSONResponse, StreamingResponse
from PIL import Image
import io
import numpy as np
import uvicorn
import asyncio
#from services.face_recognition_face_off import extract_faces
from services.face_recognizer import FaceRecognizer
import os
import zipfile

app = FastAPI()


@app.post("/detect_faces/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read image file as bytes
        image_bytes = await file.read()

        # Process the image
        faceRecognizer = FaceRecognizer("./face_bank")
        faceRecognizer.load_known_faces()
        processed_images = faceRecognizer.detect_faces(image_bytes)
        print(f"packing {len(processed_images)} images"
        # Return the processed images as a multipart response
        headers = {"Content-Disposition": "attachment; filename=processed_faces.zip"}
        return StreamingResponse(
            content=_generate_zip(processed_images),
            headers=headers,
            media_type="application/zip"
        )
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/remember_face/")
async def remember_face(image: UploadFile = File(...), name: str = ""):
    try:
        # Get the filename
        filename = image.filename
        
        # Extract the file extension
        file_extension = os.path.splitext(filename)[1]

        # Read image file as bytes
        image_bytes = await image.read()
                # Get the filename

        print(len(image_bytes))
        # Process the image and remember the face
        faceRecognizer = FaceRecognizer("./face_bank")
        faceRecognizer.remember_face(image_bytes, file_extension, name)
        
        return JSONResponse(content={"message": "Face remembered successfully"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/forget_face/")
async def forget_face(image: UploadFile = File(...), name: str = ""):
    try:
        # Get the filename
        filename = image.filename
        
        # Extract the file extension
        file_extension = os.path.splitext(filename)[1]

        # Read image file as bytes
        image_bytes = await image.read()
                # Get the filename

        print(len(image_bytes))
        # Process the image and remember the face
        faceRecognizer = FaceRecognizer("./face_bank")
        faceRecognizer.forget_face(image_bytes, file_extension, name)
        
        return JSONResponse(content={"message": "Face remembered successfully"}, status_code=200)
    except Exception as e:
        print(e)
        return JSONResponse(content={"error": str(e)}, status_code=500)


def _generate_zip(files):
    """
    Generates a zip file containing the provided files.
    """
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for filename, file_bytes in files:
            zip_file.writestr(filename, file_bytes.getvalue())
    zip_buffer.seek(0)
    return zip_buffer

if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(uvicorn.run(app, host="0.0.0.0", port=8000))

