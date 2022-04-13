import face_recognition
from face_recognition_project.settings import MEDIA_URL
from time import time_ns

from PIL import Image, ImageDraw
from cv2 import cv2

import tempfile


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
            f"image_before_processing_{timestamp}.jpg",
            f"image_after_processing_{timestamp}.jpg",
        )

    def compare_two_faces(self, loaded_img1, loaded_img2):
        """
        Returns result based on comparison result
        """
        img1_encoding = face_recognition.face_encodings(loaded_img1)[0]
        img2_encoding = face_recognition.face_encodings(loaded_img2)[0]
        result = face_recognition.compare_faces([img1_encoding], img2_encoding)

        return result

    def video_detection(self, videopath):
        """
        Saves only resulted video
        """
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(videopath.file.read())

            timestamp = time_ns() * 100
            input_video = cv2.VideoCapture(temp.name)
            size = (int(input_video.get(3)), int(input_video.get(4)))

            result = cv2.VideoWriter(
                f"{MEDIA_URL}result_{timestamp}.mp4",
                cv2.VideoWriter_fourcc(*"MP4V"),
                20.0,
                size,
            )

            while True:
                ret, frame = input_video.read()

                if not ret:
                    break

                rgb_frame = frame[:, :, ::-1]

                face_locations = face_recognition.face_locations(rgb_frame)
                for (top, right, bottom, left) in face_locations:
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                result.write(frame)

            return f"result_{timestamp}.mp4"
