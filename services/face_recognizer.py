import os
import face_recognition

class FaceRecognizer:
    def __init__(self, known_faces_dir):
        self.known_faces_dir = known_faces_dir
        self.known_faces = []
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

    def detect_faces(self, image_paths):
        results = []
        for image_path in image_paths:
            unknown_image = face_recognition.load_image_file(image_path)
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            match_index = next((i for i, x in enumerate(face_recognition.compare_faces(self.known_faces, unknown_face_encoding)) if x), None)
            if match_index is not None:
                results.append((image_path, match_index + 1))
            else:
                results.append((image_path, None))
        return results
