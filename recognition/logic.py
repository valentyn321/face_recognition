import boto3
import face_recognition
from numpy import ndarray
import io
import os


from face_recognition_project.settings import AWS_STORAGE_BUCKET_NAME
from django.core.files.uploadedfile import InMemoryUploadedFile

from PIL import Image, ImageDraw
from cv2 import cv2

import tempfile
from time import time_ns


def convert_pil_image_to_in_memory_file(image: Image) -> io.BytesIO():
    in_memory_file = io.BytesIO()
    image.save(in_memory_file, "png")
    in_memory_file.seek(0)
    return in_memory_file


def upload_in_memory_file_to_s3(
    boto3_client: boto3.client,
    bucket_name: str,
    in_memory_file: io.BytesIO,
    filename: str,
    timestamp: int,
) -> str:
    boto3_client.upload_fileobj(
        in_memory_file,
        bucket_name,
        f"media/{filename}_{timestamp}.png",
    )
    return f"media/{filename}_{timestamp}.png"


class Recognizer:

    boto_client = boto3.client("s3", region_name="eu-central-1")

    def picture_face_recognition(self, in_memory_image: InMemoryUploadedFile) -> tuple:
        """
        Input:
            in_memory_image - in memory uploaded file
        Output:
            Tuple with loaded image and face coordinates (if they are)
        """
        if type(in_memory_image) == InMemoryUploadedFile:
            image = face_recognition.load_image_file(in_memory_image)
            face_locations = face_recognition.face_locations(image)
            if face_locations:
                return (image, face_locations)
            return "There is no faces on this image!"
        return "You have not inserted an InMemoryUploadedFile!"

    def mark_faces_on_image(
        self, loaded_image: ndarray, face_coordinates: list
    ) -> Image:
        """
        Input:
            1. loaded image (output of
            face_recognition.load_image_file function)
            2. face_coordianates (output of
            face_recognition.face_locations fucntion)
        Output:
            PIL.Image with drawings (if faces are present)
        """
        pil_image = Image.fromarray(loaded_image)
        draw = ImageDraw.Draw(pil_image)

        for (top, right, bottom, left) in face_coordinates:
            draw.rectangle(
                ((left, top), (right, bottom)), outline=(255, 69, 0), width=5
            )

        del draw

        return pil_image

    def upload_pair_of_pictures_to_s3(
        self, loaded_image: ndarray, pil_image: Image
    ) -> tuple:
        """
        Input:
            1. loaded image (output of
            face_recognition.load_image_file function)
            2. PIL Image (output of self.mark_faces_on_image - image
            with rectangles on faces)
        Output:
        tuple with urls to bare picture and picture with rectangles
        Desc:
            Takes bare image and picture with rectangles on faces and upload
            them to s3 bucket with the same timestamp
        """
        timestamp = time_ns()
        bare_image = Image.fromarray(loaded_image)
        bare_image = convert_pil_image_to_in_memory_file(bare_image)

        input_url = upload_in_memory_file_to_s3(
            self.boto_client,
            AWS_STORAGE_BUCKET_NAME,
            bare_image,
            "image_before_processing",
            timestamp,
        )

        processed_image = convert_pil_image_to_in_memory_file(pil_image)
        output_url = upload_in_memory_file_to_s3(
            self.boto_client,
            AWS_STORAGE_BUCKET_NAME,
            processed_image,
            "image_after_processing",
            timestamp,
        )

        return (input_url, output_url)

    def compare_two_faces(self, loaded_img1: ndarray, loaded_img2: ndarray) -> bool:
        """
        Input:
            Two images, which are preloaded with
            face_recognition.load_image_file fucntion
        Output:
            Result of comparison
        """
        try:
            breakpoint()
            img1_encoding = face_recognition.face_encodings(loaded_img1)[0]
            img2_encoding = face_recognition.face_encodings(loaded_img2)[0]
            result = face_recognition.compare_faces([img1_encoding], img2_encoding)
            return result
        except TypeError:
            return "Not empty ndarrays should be inputs of this function!"
        except IndexError:
            return "Not empty ndarrays should be inputs of this function!"

    def video_detection(self, videopath: str) -> str:
        """
        Input:
            path to video for processing
        Output:
            path to local processed video
        """
        timestamp = time_ns()
        with tempfile.NamedTemporaryFile(suffix=".mp4") as input_video:
            input_video.write(videopath.file.read())

            input_video = cv2.VideoCapture(input_video.name)
            fourcc = cv2.VideoWriter_fourcc(*"MP4V")
            fps = input_video.get(5)
            size = (int(input_video.get(3)), int(input_video.get(4)))

            result = cv2.VideoWriter(
                f"result_{timestamp}.mp4",
                fourcc,
                fps,
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

    def video_upload_and_cleanup(self, url: str) -> None:
        self.boto_client.upload_file(
            url,
            AWS_STORAGE_BUCKET_NAME,
            f"media/{url}",
        )

        os.remove(url)
