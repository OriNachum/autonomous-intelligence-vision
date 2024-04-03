from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import io
import numpy as np
import uvicorn
import asyncio

app = FastAPI()

def process_image(image_bytes):
    # Open image using PIL
    img = Image.open(io.BytesIO(image_bytes))
    # Convert image to numpy array
    img_array = np.array(img)
    # Process your image here (for demonstration, we'll just return the original image)
    processed_images = [img_array]  # In a real scenario, you would process the image and generate an array of images
    return processed_images

@app.post("/process_image/")
async def upload_image(file: UploadFile = File(...)):
    try:
        # Read image file as bytes
        image_bytes = await file.read()
        # Process the image
        processed_images = process_image(image_bytes)
        # Return the array of processed images
        return JSONResponse(content={"processed_images": processed_images})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

if __name__ == "__main__":
    #uvicorn.run(app, host="0.0.0.0", port=8000)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(uvicorn.run(app, host="0.0.0.0", port=8000))

