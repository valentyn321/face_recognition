from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Image(models.Model):
    input_url = models.ImageField()
    output_url = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class Video(models.Model):
    url = models.FileField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class DoubleImageForComparison(models.Model):
    first_input_url = models.ImageField()
    first_output_url = models.ImageField(null=True, blank=True)
    second_input_url = models.ImageField()
    second_output_url = models.ImageField(null=True, blank=True)
    difference = models.BooleanField(default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
