from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
# Create your views here.

@api_view()
def user_tweets(request, user_id):
        user = User.objects.get(pk=user_id)
        tweets = user.tweets.all()
        return Response(
            {
                "ok": True,
                "user_tweets": tweets
            },
        )
