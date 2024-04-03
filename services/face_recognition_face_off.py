import face_recognition
from PIL import Image, ImageDraw

def extract_faces(image_path):
    # Load the image with face_recognition
    image = face_recognition.load_image_file(image_path)

    # Find all face locations in the image
    face_locations = face_recognition.face_locations(image)

    # Create a PIL ImageDraw instance
    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # Loop through each face location
    for top, right, bottom, left in face_locations:
        # Draw a rectangle around the face
        draw.rectangle(((left, top), (right, bottom)), outline=(255, 0, 0), width=2)

        # Crop and save each face
        face_image = image[top:bottom, left:right]
        cropped_image = Image.fromarray(face_image)
        cropped_image.show()  # Display the extracted face
        cropped_image.save(f"extracted_face_{top}_{right}_{bottom}_{left}.png")

    # Display the image with detected faces
    pil_image.show()

# Hardcoded path to the image
image_path = "test.jpg"

# Call the function to extract faces
extract_faces(image_path)

