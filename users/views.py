from tokenize import TokenError

from django.shortcuts import render
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
import re

from users.models import User


# Create your views here.
class Login(TokenObtainPairView):
    """Login"""

    def get_serializer_class(self) -> Serializer:
        return super().get_serializer_class()

    def get_authenticate_header(self, request: Request) -> str:
        return super().get_authenticate_header(request)

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])
        #
        result = serializer.validated_data
        result["mobile"] = serializer.user.mobile
        result["email"] = serializer.user.email
        result["username"] = serializer.user.username
        result["token"] = result.pop("access")
        result["refresh_token"] = result.pop("refresh")
        result["id"] = serializer.user.id
        print(result)
        return Response(result, status=status.HTTP_200_OK)


class Register(APIView):
    """Register"""

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        password_confirmation = request.data.get('password_confirmation')

        # validate parameters
        if not all([username, email, password_confirmation, password]):
            return Response({'error': 'all parameters must not be null'}, status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return Response({'error': 'username already exists'}, status.HTTP_400_BAD_REQUEST)
        if password != password_confirmation:
            return Response({'error': "password and password_confirmation are not match"}, status.HTTP_400_BAD_REQUEST)
        if not (6 < len(password) < 18):
            return Response({'error': "password's length must in 6 to 18"}, status.HTTP_400_BAD_REQUEST)
        if not re.match(
                r'^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$',
                email):
            return Response({'error': "email must legal'"}, status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return Response({'error': "email already exists"}, status.HTTP_400_BAD_REQUEST)
        user = User.objects.create_user(username=username, password=password, email=email)
        # user.set_password(password)
        print(user)
        res = {
            "username": username,
            "id": user.id,
            "email": user.email
        }
        return Response(res, status.HTTP_201_CREATED)
