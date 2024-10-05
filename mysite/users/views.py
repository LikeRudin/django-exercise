from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User
from .serializers import PublicUserSerializer


class Users(APIView):
    def get(self, request):
        users = User.objects.all()
        users_data = PublicUserSerializer(users, many=True).data
        return Response(users_data)

class PublicUser(APIView):
    def get(self, request, username):
        user = User.objects.get(username=username)
        user_data = PublicUserSerializer(user).data
        return Response(user_data)
