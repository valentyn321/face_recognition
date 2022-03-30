from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Image(models.Model):
    input_url = models.ImageField()
    output_url = models.ImageField(null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)