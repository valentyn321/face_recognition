from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from recognition.models import Image, DoubleImageForComparison, Video
from recognition.serializers import (
    ImageSerializer,
    DoubleImageForComparisonSerializer,
    VideoSerializer,
)

from recognition import core


class ImageListCreateAPIView(ListCreateAPIView):
    serializer_class = ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Image.objects.filter(author=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        core.process_validated_image(serializer=serializer, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ImagesComparingListCreateAPIView(ListCreateAPIView):
    serializer_class = DoubleImageForComparisonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoubleImageForComparison.objects.filter(author=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        core.process_validated_double_image(serializer=serializer, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VideoListCreateAPIView(ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Video.objects.filter(author=self.request.user.id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        core.process_validated_video(serializer=serializer, author=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
