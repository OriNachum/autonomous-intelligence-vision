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
        self.known_faces_encodings = []
        self.known_face_names = []
        self.load_known_faces()

    def load_known_faces(self):
        if self.known_faces_encodings:
            return

        for filename in os.listdir(self.known_faces_dir):
            if filename.endswith(".jpg") or filename.endswith(".png"):
                image_path = os.path.join(self.known_faces_dir, filename)
                image = face_recognition.load_image_file(image_path)
                face_encoding = face_recognition.face_encodings(image)[0]
                self.known_faces_encodings.append(face_encoding)
                self.known_face_names.append(os.path.splitext(filename)[0])

    def remember_face(self, image_bytes, file_extension, name):
        detected_faces = self._detect_faces(image_bytes)
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))
        face_encoding = face_recognition.face_encodings(image)[0]
        self.known_faces_encodings.append(face_encoding)
        self.known_face_names.append(name)

        # Save the image in the known faces directory
        filename = f"{name}.{file_extension}"
        new_image_path = os.path.join(self.known_faces_dir, filename)
        with open(new_image_path, "wb") as f:
            f.write(image_bytes)

    def forget_face(self, image_bytes, file_extension, name):
        try:
            print("forget_face: getting faces by name")
            name_index = self.known_face_names.index(name)
            known_face_encodings = self.known_faces_encodings[name_index]
            
            print("forget_face: getting faces from input")
            detected_faces = self._detect_faces(image_bytes)
            print("forget_face: loading known face")
            #known_face_loaded = face_recognition.load_image_file(io.BytesIO(known_face))
            print("forget_face: getting loaded known face encodings")
            #known_face_encoding = face_recognition.face_encodings(known_face_loaded)[0]

            # Filter detected faces by name
            filename = f"{name}.png"
            print("forget_face: getting detected faces with name")
            detected_faces_with_name = [(face_name, face_bytes) for face_name, face_bytes in detected_faces if face_name == filename]

            print("forget_face: handling detected faces with name")
            if detected_faces_with_name:
                # Compare embeddings of filtered detected faces with the known face
                for face_name, detected_face in detected_faces_with_name:
                    print(f"forget_face: handling detected faces with name {face_name}")
                    print("forget_face: loading known face")
                    detected_face_loaded = face_recognition.load_image_file(detected_face)
                    print("forget_face: getting loaded known face encodings")
                    detected_face_encoding = face_recognition.face_encodings(detected_face_loaded)[0]

                    print("forget_face: comparing faces")
                    if face_recognition.compare_faces([known_face_encodings], detected_face_encoding):
                        # Delete from memory
                        del self.known_faces_encodings[name_index]
                        del self.known_face_names[name_index]
                        
                        # Delete the image file
                        image_path = os.path.join(self.known_faces_dir, filename)
                        print(f"forget_face: trying to delete {image_path}")
                        if os.path.exists(image_path):
                            os.remove(image_path)
                            print(f"Face with name '{name}' forgotten successfully.")
                        else:
                            print(f"Image file for face with name '{name}' not found.")
                        return  # Exit the method after successful deletion
                    else:
                        print("forget_face: compare failed")
                raise ValueError(f"No detected face with name '{name}' matches the known face.")
            else:
                raise ValueError(f"No detected face with name '{name}' found.")
        except ValueError as e:
            print(e)
            raise ValueError(f"Face with name '{name}' not found.")

    def detect_faces(self, image_bytes):
        return self._detect_faces(image_bytes)

    def _detect_faces(self, image_bytes):
        results = []
        id=0
        faces = extract_faces(image_bytes)
        print(f"I have {len(self.known_faces_encodings)} faces in memory, found {len(faces)} in image")
        for face in faces:
            print(f"getting face{id}")
            unknown_image = face_recognition.load_image_file(face[1])
            unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
            match_indices = [i for i, x in enumerate(face_recognition.compare_faces(self.known_faces_encodings, unknown_face_encoding)) if x]
            if match_indices:
                print(f"successfully matched face{id} with {len(match_indices)} faces")
                for index in match_indices:
                    match_name = self.known_face_names[index]
                    print(f"adding to results face {match_name}") 
                    results.append((f"{match_name}.png", face[1]))
            else:
                print(f"could not match face{id}")
                results.append((f"face-{id}.png", face[1]))
            id=id+1
        print(f"returning {len(results)} faces")
        return results
        
if __name__ == "__main__":
    print("starting FaceRecognizer")
    with open("test.jpg", "rb") as f:
        # Read image file as bytes
        image_bytes = f.read()
    faceRecognizer = FaceRecognizer("./face_bank")
    faceRecognizer.load_known_faces()
            # Extract file extension from the image_path
    #file_extension = os.path.splitext(image_path)[1]
    #with open(image_path, "rb") as f:
    #    Read image file as bytes
    #    image_bytes = f.read()
    #    faceRecognizer.remember_face(image_bytes, "png", "romi")
    print(faceRecognizer.detect_faces(image_bytes))
