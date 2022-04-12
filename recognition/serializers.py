from rest_framework import serializers

from recognition.models import Image, DoubleImageForComparison


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"


class DoubleImageForComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubleImageForComparison
        fields = "__all__"
