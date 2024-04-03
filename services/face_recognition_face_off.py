import asyncio
import face_recognition
from PIL import Image, ImageDraw
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import io
import base64

app = FastAPI()


async def extract_faces(image_bytes):
    try:
        # Load the image with face_recognition
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))

        # Find all face locations in the image
        face_locations = face_recognition.face_locations(image)

        extracted_faces = []

        # Loop through each face location
        for i, (top, right, bottom, left) in enumerate(face_locations):
            # Crop each face
            face_image = image[top:bottom, left:right]
            pil_image = Image.fromarray(face_image)

            # Convert PIL image to bytes
            img_byte_array = io.BytesIO()
            pil_image.save(img_byte_array, format="PNG")
            img_byte_array.seek(0)

            # Append the image bytes and filename to the list
            extracted_faces.append((f"face_{i + 1}.png", img_byte_array))

        return extracted_faces
    except Exception as e:
        return [str(e)]



@app.post("/process_image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read image file as bytes
        image_bytes = await file.read()

        # Run face extraction in the background
        extracted_faces = await asyncio.create_task(extract_faces(image_bytes))

        # Return the array of extracted faces
        return JSONResponse(content={"extracted_faces": extracted_faces})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
