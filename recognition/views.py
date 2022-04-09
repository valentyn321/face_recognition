from django.shortcuts import render
from django.urls import reverse
from django.views.generic.edit import FormView

from recognition.forms import ImageForm, DoubleImagesForm
from recognition.logic import Recognizer
from recognition.models import Image, DoubleImageForComparison


def welcome(request):
    return render(request=request, template_name="recognition/base.html")


def detection_result(request):
    result_image = Image.objects.filter(author=request.user).last()
    return render(
        request=request,
        template_name="recognition/face_detection_result.html",
        context={"result_image": result_image.output_url},
    )


def comparison_result(request):
    result_images = DoubleImageForComparison.objects.filter(author=request.user).last()
    return render(
        request=request,
        template_name="recognition/face_comparison_result.html",
        context={"result_images": result_images},
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


class ImagesComparingFormView(FormView):
    template_name = "recognition/faces_comparison.html"
    form_class = DoubleImagesForm

    def get_success_url(self):
        return reverse("comparison-result")

    def form_valid(self, form):

        image1, face_coordinates1 = Recognizer().picture_face_recognition(
            form.files.get("first_input_url")
        )

        image2, face_coordinates2 = Recognizer().picture_face_recognition(
            form.files.get("second_input_url")
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
            if Recognizer().compare_two_faces(image1, image2)[0]:
                DoubleImageForComparison.objects.create(
                    first_input_url=input_url1,
                    first_output_url=output_url1,
                    second_input_url=input_url2,
                    second_output_url=output_url2,
                    difference=False,
                    author=self.request.user,
                )
            else:
                DoubleImageForComparison.objects.create(
                    first_input_url=input_url1,
                    first_output_url=output_url1,
                    second_input_url=input_url2,
                    second_output_url=output_url2,
                    difference=True,
                    author=self.request.user,
                )

        return super().form_valid(form)
