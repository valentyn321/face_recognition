import boto3
import face_recognition
from numpy import ndarray
import io


from face_recognition_project.settings import AWS_STORAGE_BUCKET_NAME

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

    def picture_face_recognition(self, image_path: str) -> tuple:
        """
        Input:
            image_path (path to the file, which func need to processed)
        Output:
            Tuple with loaded image and face coordinates (if they are)
        """
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        if face_locations:
            return (image, face_locations)

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
        img1_encoding = face_recognition.face_encodings(loaded_img1)[0]
        img2_encoding = face_recognition.face_encodings(loaded_img2)[0]
        result = face_recognition.compare_faces([img1_encoding], img2_encoding)

        return result

    def video_detection(self, videopath: str) -> str:
        """
        Input:
            path to video for processing
        Output:
            path to s3 bucket with processed video
        """
        with tempfile.NamedTemporaryFile() as temp:
            temp.write(videopath.file.read())

            timestamp = time_ns() * 100
            input_video = cv2.VideoCapture(temp.name)
            size = (int(input_video.get(3)), int(input_video.get(4)))

            result = cv2.VideoWriter(
                f"result_{timestamp}.mp4",
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
