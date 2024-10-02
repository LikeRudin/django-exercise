from django.shortcuts import render

# Create your views here.
from .models import Tweet

def detail(request):
    tweets = Tweet.objects.all()
    return render(request, "tweets.html", {"tweets": tweets})