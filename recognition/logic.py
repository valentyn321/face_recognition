import face_recognition
from face_recognition_project.settings import MEDIA_URL
from time import time_ns

from PIL import Image, ImageDraw


class Recognizer:
    def picture_face_recognition(self, image_path):
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        if face_locations:
            return (image, face_locations)

    def mark_faces(self, loaded_image, face_coordinates):
        """
        Saves 2 images - without frame and with it (better to override in the future)
        """
        timestamp = time_ns() * 100

        bare_image = Image.fromarray(loaded_image)
        bare_image.save(f"{MEDIA_URL}image_before_processing_{timestamp}.jpg")

        image = Image.fromarray(loaded_image)
        draw = ImageDraw.Draw(image)

        for (top, right, bottom, left) in face_coordinates:
            draw.rectangle(
                ((left, top), (right, bottom)), outline=(255, 69, 0), width=5
            )

        del draw
        image.save(f"{MEDIA_URL}image_after_processing_{timestamp}.jpg")

        return (
            f"{MEDIA_URL}image_before_processing_{timestamp}.jpg",
            f"{MEDIA_URL}image_after_processing_{timestamp}.jpg",
        )
