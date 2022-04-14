from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from recognition.logic import Recognizer
from recognition.models import Image, DoubleImageForComparison, Video
from recognition.serializers import (
    ImageSerializer,
    DoubleImageForComparisonSerializer,
    VideoSerializer,
)


class ImageListCreateAPIView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        image, face_coordinates = Recognizer().picture_face_recognition(
            serializer.validated_data.get("input_url", None)
        )
        if face_coordinates:
            input_url, output_url = Recognizer().mark_faces(
                image,
                face_coordinates,
            )
            serializer.validated_data["input_url"] = input_url
            serializer.validated_data["output_url"] = output_url
            serializer.validated_data["faces_presence"] = 1
            serializer.save()


class ImagesComparingListCreateAPIView(ListCreateAPIView):
    queryset = DoubleImageForComparison.objects.all()
    serializer_class = DoubleImageForComparisonSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        image1, face_coordinates1 = Recognizer().picture_face_recognition(
            serializer.validated_data.get("first_input_url")
        )
        image2, face_coordinates2 = Recognizer().picture_face_recognition(
            serializer.validated_data.get("second_input_url")
        )

        if all([face_coordinates1, face_coordinates2]):
            input_url1, output_url1 = Recognizer().mark_faces(
                image1,
                face_coordinates1,
            )
            input_url2, output_url2 = Recognizer().mark_faces(
                image2,
                face_coordinates2,
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
    queryset = Video.objects.all()
    serializer_class = VideoSerializer

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
