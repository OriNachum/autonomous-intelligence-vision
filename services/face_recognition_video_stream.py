import cv2
import face_recognition
from collections import deque
from fastapi import FastAPI, Response
import uvicorn

# Initialize the video capture
cap = cv2.VideoCapture(0)  # Replace 0 with the appropriate camera index

# Initialize the face recognition data structure
face_data = deque(maxlen=10)  # Keep the last 10 faces

# Initialize the FastAPI app
app = FastAPI()

# Helper function to encode face image as JPEG
def encode_face_image(face_image):
    _, encoded_image = cv2.imencode(".jpg", face_image)
    return encoded_image.tobytes()

# Function to process the video feed and detect faces
def process_video_feed():
    while True:
        # Capture the frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # Add the detected faces to the face_data deque
        for face_encoding, face_location in zip(face_encodings, face_locations):
            top, right, bottom, left = face_location
            face_image = frame[top:bottom, left:right]
            face_data.append((face_image, face_encoding))

# API endpoint to retrieve the latest face photos
@app.get("/faces")
def get_face_photos():
    face_images = []
    for face_image, _ in face_data:
        encoded_image = encode_face_image(face_image)
        face_images.append(encoded_image)

    return Response(content=b"".join(face_images), media_type="image/jpeg")

# Start the video feed processing in a separate thread
import threading
video_thread = threading.Thread(target=process_video_feed)
video_thread.start()

# Start the FastAPI server
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
