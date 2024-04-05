import os
import face_recognition
from PIL import Image
import io

class FaceRecognitionManager:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_faces = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        if self.known_faces:
            return

        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.known_faces_dir, filename)
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                self.known_faces.append(face_encoding)
                self.known_face_names.append(os.path.splitext(filename)[0])

    async def extract_and_recognize_faces(self, image_bytes):
        try:
            # Load the image with face_recognition
            image = face_recognition.load_image_file(io.BytesIO(image_bytes))

            # Find all face locations in the image
            face_locations = face_recognition.face_locations(image)
            face_encodings = face_recognition.face_encodings(image, face_locations)

            extracted_faces = []
            for i, face_encoding in enumerate(face_encodings):
                # Compare the face encoding with the known faces
                matches = face_recognition.compare_faces(self.known_faces, face_encoding)
                name = "Unknown"
                for j, match in enumerate(matches):
                    if match:
                        name = self.known_face_names[j]
                        break

                # Crop each face
                top, right, bottom, left = face_locations[i]
                face_image = image[top:bottom, left:right]
                pil_image = Image.fromarray(face_image)

                # Convert PIL image to bytes
                img_byte_array = io.BytesIO()
                pil_image.save(img_byte_array, format="PNG")
                img_byte_array.seek(0)

                # Append the image bytes, filename, and name to the list
                extracted_faces.append((f"face_{i + 1}.png", img_byte_array, name))

            return extracted_faces
        except Exception as e:
            return [str(e)]

    def remember_face(self, image_path, name):
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        self.known_faces.append(face_encoding)
        self.known_face_names.append(name)

        # Save the image in the known faces directory
        filename = f"{name}.jpg"
        new_image_path = os.path.join(self.known_faces_dir, filename)
        image = Image.fromarray(image)
        image.save(new_image_path)

    def forget_face(self, name):
        try:
            name_index = self.known_face_names.index(name)
            del self.known_faces[name_index]
            del self.known_face_names[name_index]

            # Delete the image file
            filename = f"{name}.jpg"
            image_path = os.path.join(self.known_faces_dir, filename)
            os.remove(image_path)
        except ValueError:
            print(f"Face with name '{name}' not found.")