from django.forms import ModelForm
from recognition.models import Image, DoubleImageForComparison


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["input_url"]


class DoubleImagesForm(ModelForm):
    class Meta:
        model = DoubleImageForComparison
        fields = ["first_input_url", "second_input_url"]
