from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import TweetSerializer, LikeSerializer

from .models import Tweet, Like

class Tweets(APIView):

    def get(self, request):
        """
        Return a list of all Tweets
        """
        all_tweets = Tweet.objects.all()
        serializer = TweetSerializer(
            all_tweets,
            many=True,
        )
        return Response(serializer.data)


class Likes(APIView):
    def get(self, request):
        """
        Return a list of all Likes
        """
        likes = Like.objects.all()
        serializer = LikeSerializer(
            likes,
            many=True,
        )
        return Response(serializer.data)


class TweetDetail(APIView):
    def get(self, request, pk):
        """
        Return a Tweet Data
        """
        try:
            tweet = Tweet.objects.get(pk=pk)
            tweet_data = TweetSerializer(tweet).data

            likes = Like.objects.filter(tweet=tweet)
            likes_data = LikeSerializer(likes, many=True,).data

            tweet_data['likes'] = likes_data

            return Response(tweet_data)

        except Tweet.DoesNotExist:
            return Response({"error": "Tweet not found"}, status=404)
