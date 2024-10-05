from rest_framework import serializers
from .models import Tweet
from .models import Like

class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields ="__all__"


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

class TweetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"
