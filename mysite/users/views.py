from django.contrib.auth import authenticate, login, logout

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import status

from .models import User
from .serializers import PublicUserSerializer, LoginSerializer

from tweets.models import Tweet
from tweets.serializers import TweetSerializer


class Users(APIView):
    def get(self, request):
        users = User.objects.all()
        users_data = PublicUserSerializer(users, many=True).data
        return Response(users_data)
    

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        name = request.data.get('name', '') 
        avatar = request.data.get('avatar', '') 
        
        if not username or not password or not email:
            raise ValidationError("아이디, 비밀번호, 이메일을 모두 입력해주세요.")
        
        # 이미 존재하는 사용자 이름인지 확인
        if User.objects.filter(username=username).exists():
            raise ValidationError("사용할 수 없는 아이디입니다.")
    

        return
    

class PublicUser(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        user_data = PublicUserSerializer(user).data
        return Response(user_data)



class TweetsByUser(APIView):
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        tweets = Tweet.objects.filter(user=user) 
        tweet_data = TweetSerializer(
            tweets,
            many=True,
        )
        return Response(tweet_data)


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):

        user = request.user
        if not user:
            raise AuthenticationFailed("잘못된 접근입니다. 사용자 인증정보가 없습니다. ")
        
        current_password = request.data.get("current_password")
        new_password = request.data.get("password")
        if not current_password or not new_password:
            raise ValidationError("기존의 비밀번호와 새로운 비밀번호를 전부 입력해주세요.")
        
        if not user.check_password(current_password):
            raise AuthenticationFailed("현재 비밀번호가 잘못 입력되었습니다.")
        
        user.set_password(new_password)
        user.save()

        return Response(data="비밀번호를 성공적으로 변경하였습니다.", status=status.HTTP_200_OK)


class Login(APIView):
    def post(self, request):
        user_data = request.data
        serializer = LoginSerializer(user_data)
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data["user"]
        login(request, user)

        user_data = PublicUserSerializer(user).data
        
        return Response(data={"message": "로그인 되었습니다.", "user_data": serializer.data}, status=status.HTTP_200_OK)
        
class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request):
        logout(request)
        return Response(data="로그아웃 되었습니다.", status=status.HTTP_200_OK)