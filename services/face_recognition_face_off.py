import asyncio
import face_recognition
from PIL import Image, ImageDraw
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import io
import base64

app = FastAPI()


async def extract_faces(image_bytes, scale_factor=1.0, aspect_ratio=1.0):
    try:
        # Load the image with face_recognition
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))

        # Find all face locations in the image
        face_locations = face_recognition.face_locations(image)

        extracted_faces = []

        # Loop through each face location
        for i, (top, right, bottom, left) in enumerate(face_locations):
            # Expand or shrink the bounding box based on the scale factor
            height = bottom - top
            width = right - left

            # Calculate new bounding box coordinates
            expanded_top = max(0, int(top - scale_factor * height))
            expanded_bottom = min(image.shape[0], int(bottom + scale_factor * height))
            expanded_left = max(0, int(left - scale_factor * width))
            expanded_right = min(image.shape[1], int(right + scale_factor * width))

            # Crop each face
            face_image = image[expanded_top:expanded_bottom, expanded_left:expanded_right]

            # Calculate the width and height of the cropped image
            new_width = face_image.shape[1]
            new_height = int(new_width / aspect_ratio)

            # Ensure the image has the desired aspect ratio
            if new_height > face_image.shape[0]:
                new_height = face_image.shape[0]
                new_width = int(new_height * aspect_ratio)

            # Calculate the center coordinates for cropping a rectangle
            center_x = face_image.shape[1] // 2
            center_y = face_image.shape[0] // 2

            # Calculate the coordinates for cropping a rectangle around the center
            crop_left = max(0, center_x - new_width // 2)
            crop_right = min(face_image.shape[1], center_x + new_width // 2)
            crop_top = max(0, center_y - new_height // 2)
            crop_bottom = min(face_image.shape[0], center_y + new_height // 2)

            # Crop the image to a rectangle
            face_image = face_image[crop_top:crop_bottom, crop_left:crop_right]

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
