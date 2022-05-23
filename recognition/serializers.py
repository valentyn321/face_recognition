from rest_framework import serializers

from recognition.models import Image, DoubleImageForComparison, Video


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = "__all__"
        read_only_fields = ("output_url", "author", "faces_presense", "created_at")


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = "__all__"
        read_only_fields = ("author", "created_at")


class DoubleImageForComparisonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoubleImageForComparison
        fields = "__all__"
        read_only_fields = (
            "first_output_url",
            "second_output_url",
            "author",
            "difference",
            "created_at",
        )
