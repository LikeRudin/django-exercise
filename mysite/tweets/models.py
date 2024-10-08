from django.db import models
from users.models import User


class Tweet(models.Model):
    payload = models.TextField(max_length=180)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField()
    updated_at = models.DateField()
    likes = models.ManyToManyField(User, through='Like', related_name='liked_tweets')
    
    def __str__(self) -> str:
        return f"{super().__str__()} Tweet Model"
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE)
    created_at = models.DateField()
    updated_at = models.DateField()

     
    def __str__(self) -> str:
        return f"{super().__str__()} LikeModel"


