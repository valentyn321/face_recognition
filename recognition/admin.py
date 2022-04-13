from django.contrib import admin
from recognition.models import Image, DoubleImageForComparison, Video

admin.site.register(Image)
admin.site.register(Video)
admin.site.register(DoubleImageForComparison)
