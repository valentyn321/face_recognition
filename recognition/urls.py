from django.urls import path
from recognition import views as recognition_views

urlpatterns = [
    path(
        "detection/",
        recognition_views.ImageListCreateAPIView.as_view(),
        name="face_detection",
    ),
    # path(
    #     "detection-result/",
    #     recognition_views.detection_result,
    #     name="detection-result",
    # ),
    # path(
    #     "comparison/",
    #     recognition_views.ImagesComparingFormView.as_view(),
    #     name="face_comparison",
    # ),
    # path(
    #     "comparison-result/",
    #     recognition_views.comparison_result,
    #     name="comparison-result",
    # ),
]
