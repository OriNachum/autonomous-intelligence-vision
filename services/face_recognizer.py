import os
import face_recognition
import shutil

class FaceRecognizer:
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

    def remember_face(self, image_path, name):
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        self.known_faces.append(face_encoding)
        self.known_face_names.append(name)

        # Save the image in the known faces directory
        filename = f"{name}.jpg"
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

    def detect_faces(self, image_paths):
        results = []
        for image_path in image_paths:
            unknown_image = face_recognition.load_image_file(image_path)
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            match_indices = [i for i, x in enumerate(face_recognition.compare_faces(self.known_faces, unknown_face_encoding)) if x]
            if match_indices:
                match_names = [self.known_face_names[i] for i in match_indices]
                results.append((image_path, match_names))
            else:
                results.append((image_path, []))
        return results