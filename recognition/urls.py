from django.urls import path
from recognition import views as recognition_views

urlpatterns = [
    path(
        "detection/",
        recognition_views.ImageListCreateAPIView.as_view(),
        name="face_detection",
    ),
    path(
        "comparison/",
        recognition_views.ImagesComparingListCreateAPIView.as_view(),
        name="face_comparison",
    ),
    path(
        "video-detection/",
        recognition_views.VideoListCreateAPIView.as_view(),
        name="video_face_detection",
    ),
]
