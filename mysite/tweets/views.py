from rest_framework import status

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, AuthenticationFailed
from rest_framework.permissions import IsAuthenticatedOrReadOnly

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

    def post(self, request):
        """
        Create a Tweet
        """
        serializer = TweetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

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
     
     permission_classes = [IsAuthenticatedOrReadOnly]

     def get_tweet_or_404(self, pk, user):
        try:
            tweet = Tweet.objects.get(pk=pk)
        except Tweet.DoesNotExist:
            raise NotFound("존재하지 않는 Tweet 입니다.")
        
        if tweet.user != user:
            raise AuthenticationFailed("Tweet은 작성자 본인만이 수정/삭제할 수 있습니다.")
        return tweet
     
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
            return NotFound({"error": "Tweet not found"}, status=404)
        
        
     def put(self, request, pk):
        '''
        Edit a tweet
        '''
        tweet = self.get_tweet_or_404(pk, request.user)
        
        serializer = TweetSerializer(instance=tweet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
     def delete(self, request,pk):
        '''
        delete a tweet
        '''
        tweet = self.get_tweet_or_404(pk, request.user)
        
        tweet.delete()
        return Response(data="Tweet을 삭제했습니다", status=status.HTTP_200_OK)
    