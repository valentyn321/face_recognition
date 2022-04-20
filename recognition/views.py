from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from recognition.logic import Recognizer
from recognition.models import Image, DoubleImageForComparison, Video
from recognition.serializers import (
    ImageSerializer,
    DoubleImageForComparisonSerializer,
    VideoSerializer,
)


class ImageListCreateAPIView(ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(author=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if not self.validate_author(serializer.validated_data["author"]):
            return Response(
                "You cannot create objects for another user!", status.HTTP_403_FORBIDDEN
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        recognizer_obj = Recognizer()
        image, face_coordinates = recognizer_obj.picture_face_recognition(
            serializer.validated_data.get("input_url", None)
        )
        if face_coordinates:
            image_with_rectangles_on_faces = recognizer_obj.mark_faces_on_image(
                image,
                face_coordinates,
            )
            input_url, output_url = recognizer_obj.upload_pair_of_pictures_to_s3(
                image, image_with_rectangles_on_faces
            )
            serializer.validated_data["input_url"] = input_url
            serializer.validated_data["output_url"] = output_url
            serializer.validated_data["faces_presence"] = 1
            serializer.save()

    def validate_author(self, author, *args, **kwargs):
        """
        This fucntion is here, because we need some data from the request
        """
        if self.request.user == author:
            return True
        else:
            return False


class ImagesComparingListCreateAPIView(ListCreateAPIView):
    serializer_class = DoubleImageForComparisonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(author=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        recognizer_obj = Recognizer()
        image1, face_coordinates1 = recognizer_obj.picture_face_recognition(
            serializer.validated_data.get("first_input_url")
        )
        image2, face_coordinates2 = recognizer_obj.picture_face_recognition(
            serializer.validated_data.get("second_input_url")
        )

        if all([face_coordinates1, face_coordinates2]):

            image1_with_rectangles_on_faces = recognizer_obj.mark_faces_on_image(
                image1,
                face_coordinates1,
            )
            image2_with_rectangles_on_faces = recognizer_obj.mark_faces_on_image(
                image2,
                face_coordinates2,
            )

            input_url1, output_url1 = recognizer_obj.upload_pair_of_pictures_to_s3(
                image1, image1_with_rectangles_on_faces
            )
            input_url2, output_url2 = recognizer_obj.upload_pair_of_pictures_to_s3(
                image2, image2_with_rectangles_on_faces
            )

            serializer.validated_data["first_input_url"] = input_url1
            serializer.validated_data["second_input_url"] = input_url2
            serializer.validated_data["first_output_url"] = output_url1
            serializer.validated_data["second_output_url"] = output_url2

            if Recognizer().compare_two_faces(image1, image2)[0]:
                serializer.validated_data["difference"] = False
            else:
                serializer.validated_data["difference"] = True

            serializer.save()


class VideoListCreateAPIView(ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(author=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        url = Recognizer().video_detection(
            serializer.validated_data.get("url", None),
        )
        serializer.validated_data["url"] = url
        serializer.save()
