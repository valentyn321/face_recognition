from rest_framework import serializers

from recognition.models import Image, DoubleImageForComparison, Video


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"


class DoubleImageForComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubleImageForComparison
        fields = "__all__"
