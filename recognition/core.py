from recognition.face_recognition_logic import Recognizer

recognizer = Recognizer()


def process_validated_image(serializer, author):
    image, face_coordinates = recognizer.picture_face_recognition(
        serializer.validated_data.get("input_url", None)
    )
    if face_coordinates:
        image_with_rectangles_on_faces = recognizer.mark_faces_on_image(
            image,
            face_coordinates,
        )
        input_url, output_url = recognizer.upload_pair_of_pictures_to_s3(
            image, image_with_rectangles_on_faces
        )
        serializer.validated_data["input_url"] = input_url
        serializer.validated_data["output_url"] = output_url
        serializer.validated_data["author"] = author
        serializer.validated_data["faces_presence"] = 1
        serializer.save()


def process_validated_double_image(serializer, author):
    image1, face_coordinates1 = recognizer.picture_face_recognition(
        serializer.validated_data.get("first_input_url")
    )

    image2, face_coordinates2 = recognizer.picture_face_recognition(
        serializer.validated_data.get("second_input_url")
    )

    if all([face_coordinates1, face_coordinates2]):

        image1_with_rectangles_on_faces = recognizer.mark_faces_on_image(
            image1,
            face_coordinates1,
        )
        image2_with_rectangles_on_faces = recognizer.mark_faces_on_image(
            image2,
            face_coordinates2,
        )

        input_url1, output_url1 = recognizer.upload_pair_of_pictures_to_s3(
            image1, image1_with_rectangles_on_faces
        )
        input_url2, output_url2 = recognizer.upload_pair_of_pictures_to_s3(
            image2, image2_with_rectangles_on_faces
        )

        serializer.validated_data["first_input_url"] = input_url1
        serializer.validated_data["second_input_url"] = input_url2
        serializer.validated_data["first_output_url"] = output_url1
        serializer.validated_data["second_output_url"] = output_url2
        serializer.validated_data["author"] = author

        if Recognizer().compare_two_faces(image1, image2)[0]:
            serializer.validated_data["difference"] = False
        else:
            serializer.validated_data["difference"] = True

        serializer.save()


def process_validated_video(serializer, author):
    url = recognizer.video_detection(
        serializer.validated_data.get("url", None),
    )

    recognizer.video_upload_and_cleanup(url)

    serializer.validated_data["url"] = url
    serializer.validated_data["author"] = author
    serializer.save()
