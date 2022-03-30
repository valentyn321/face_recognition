from django.urls import path
from recognition import views as recognition_views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path("", recognition_views.welcome, name="welcome"),
    path(
        "detection/",
        login_required(recognition_views.ImageDetectionFormView.as_view()),
        name="face_detection",
    ),
    path(
        "detection-result/",
        login_required(recognition_views.detection_result),
        name="detection-result",
    ),
]
