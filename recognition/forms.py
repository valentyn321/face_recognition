from dataclasses import fields
from django.forms import ModelForm
from recognition.models import Image


class ImageForm(ModelForm):
    class Meta:
        model = Image
        fields = ["input_url"]
