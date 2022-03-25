from django.urls import path
from recognition import views as recognition_views

urlpatterns = [
    path("", recognition_views.welcome, name="welcome"),
    path(
        "detection/",
        recognition_views.ImageDetectionFormView.as_view(),
        name="face_detection",
    ),
    path(
        "detection-result/",
        recognition_views.detection_result,
        name="detection-result",
    ),
]
