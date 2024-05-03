from rest_framework import serializers

from glasses.products.models import Frame, Lens


class FrameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Frame
        fields = "__all__"


class LensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lens
        fields = "__all__"
