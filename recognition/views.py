from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status

from recognition.logic import Recognizer
from recognition.models import Image, DoubleImageForComparison
from recognition.serializers import ImageSerializer


class ImageListCreateAPIView(ListCreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.validated_data.get("input_url", None)
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
            serializer.save()
