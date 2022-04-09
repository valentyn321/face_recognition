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
    path(
        "comparison/",
        login_required(recognition_views.ImagesComparingFormView.as_view()),
        name="face_comparison",
    ),
    path(
        "comparison-result/",
        login_required(recognition_views.comparison_result),
        name="comparison-result",
    ),
]
