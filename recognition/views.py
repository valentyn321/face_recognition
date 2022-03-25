from multiprocessing import context
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView

from recognition.forms import ImageForm
from recognition.logic import Recognizer
from recognition.models import Image


def welcome(request):
    return render(request=request, template_name="recognition/base.html")


def detection_result(request):
    result_image = Image.objects.filter(author=request.user).last()
    return render(
        request=request,
        template_name="recognition/face_detection_result.html",
        context={"result_image": result_image.output_url},
    )


class ImageDetectionFormView(FormView):
    template_name = "recognition/face_detection.html"
    form_class = ImageForm

    def get_success_url(self):
        return reverse("detection-result")

    def form_valid(self, form):
        image, face_coordinates = Recognizer().picture_face_recognition(
            form.files.get("input_url")
        )
        if face_coordinates:
            input_url, output_url = Recognizer().mark_faces(
                image,
                face_coordinates,
            )
            Image.objects.create(
                input_url=input_url,
                output_url=output_url,
                author=self.request.user,
            )
        return super().form_valid(form)
