from rest_framework.serializers import ModelSerializer, Serializer
from .models import Tweet
from .models import Like

class TweetSerializer(ModelSerializer):
    class Meta:
        model = Tweet
        fields ="__all__"


class LikeSerializer(ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"

class TweetDetailSerializer(ModelSerializer):
    class Meta:
        model = Tweet
        fields = "__all__"

