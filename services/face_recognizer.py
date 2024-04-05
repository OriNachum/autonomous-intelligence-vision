import os
import face_recognition
import shutil
import io

if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.append(parent_dir)

from services.extract_faces import extract_faces

class FaceRecognizer:
    def __init__(self, known_faces_dir):
        if not os.path.isdir(known_faces_dir):
            os.makedirs(known_faces_dir)
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
                self.known_face_names.append(filename)

    def remember_face(self, image_path, name):
        # Extract file extension from the image_path
        file_extension = os.path.splitext(image_path)[1]

        with open(image_path, "rb") as f:
            # Read image file as bytes
            image_bytes = f.read()
            image = face_recognition.load_image_file(io.BytesIO(image_bytes))
        face_encoding = face_recognition.face_encodings(image)[0]
        self.known_faces.append(face_encoding)
        self.known_face_names.append(name)

        # Save the image in the known faces directory
        filename = f"{name}.{file_extension}"
        new_image_path = os.path.join(self.known_faces_dir, filename)
        shutil.copy(image_path, new_image_path)

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

    def detect_faces(self, image_bytes):
        results = []
        id=0
        faces = extract_faces(image_bytes)
        print(f"I have {len(self.known_faces)} faces in memory, found {len(faces)} in image")
        for face in faces:
            print(f"getting face{id}")
            unknown_image = face_recognition.load_image_file(face[1])
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            match_indices = [i for i, x in enumerate(face_recognition.compare_faces(self.known_faces, unknown_face_encoding)) if x]
            if match_indices:
                print(f"successfully matched face{id}")
                match_names = [self.known_face_names[i] for i in match_indices]
                results.append((match_names[0], face[1]))
            else:
                print(f"could not match face{id}")
                results.append((f"face{id}", face[1]))
            id=id+1
        return results
        
if __name__ == "__main__":
    print("starting FaceRecognizer")
    with open("test.jpg", "rb") as f:
        # Read image file as bytes
        image_bytes = f.read()
    faceRecognizer = FaceRecognizer("./face_bank")
    faceRecognizer.load_known_faces()
    # faceRecognizer.remember_face("face_1.png", "romi")
    print(faceRecognizer.detect_faces(image_bytes))
