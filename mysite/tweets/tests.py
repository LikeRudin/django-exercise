from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from .models import Tweet
from users.models import User

"""
CRUD를 테스트 했습니다.

views에서 tweet의 user를 설정할때에는 그냥 집어넣어주기만 하면되었는데,
테스트할때에는 pk값을 제공해야하네요.. 어째서..?

HTTP Status code가 무엇이 옳은지 몰라서 애먹었습니다.
Django는 사전에 많은것을 만들어서 제공해주지만, 그만큼 공식 dic을 열심히봐야하네요.
Django에 능통한사람은 아주빠르게 개발을 할 수있겠지만, 그렇지않다면, 그냥 이거저거 직접만드는게 나을지도 모르겠다는 생각이 들었습니다.
"""


class TweetTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        self.tweet = Tweet.objects.create(user=self.user, payload='This is a test tweet')
        Tweet.objects.create(user=self.user, payload='This is a test tweet2')
        
        self.tweets_url = reverse('tweets')
        self.single_tweet_url = reverse('tweet-rud',kwargs={'pk': self.tweet.pk})

    def test_get_all_tweets(self):
        """
        GET /api/v1/tweets: 모든 트윗을 가져오는 테스트
        """
        response = self.client.get(self.tweets_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_tweet(self):
        """
        POST /api/v1/tweets: 트윗 생성 테스트
        """
        data = {
            'payload': 'This is a new tweet',
            "user": self.user.pk
        }
        response = self.client.post(self.tweets_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_tweet(self):
        """
        PUT /api/v1/tweets/<int:pk>: 트윗 수정 테스트
        """
       
        data = {
            'payload': '업데이트된 payload'
        }
        response = self.client.put(self.single_tweet_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tweet.refresh_from_db()
        self.assertEqual(self.tweet.payload, '업데이트된 payload')

    def test_delete_tweet(self):
        """
        DELETE /api/v1/tweets/<int:pk>: 트윗 삭제 테스트
        """
        response = self.client.delete(self.single_tweet_url )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Tweet.objects.count(), 1)