from rest_framework.serializers import ModelSerializer, Serializer, CharField
from rest_framework.exceptions import ValidationError, AuthenticationFailed

from django.contrib.auth import authenticate

from .models import User


class PublicUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = (
            "name",
            "avatar",
            "username",
        )


class LoginSerializer(Serializer):
    username = CharField(write_only=True)
    password = CharField(write_only=True, style={'input_type': 'password'})
    
    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise ValidationError("아이디와 비밀번호를 모두 입력해주세요.")
        
        user = authenticate(username=username, password=password)
        
        if not user:
            raise AuthenticationFailed("아이디 또는 비밀번호가 올바르지 않습니다.")
        
        data["user"] = user
        return data
    
