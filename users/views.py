import os
import random
from tokenize import TokenError

from django.http import FileResponse
from rest_framework import status, mixins
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView
import re

from common.aliyun_message import Sample
from djangoProject3.settings import MEDIA_ROOT
from users.models import User, Address, VerifCode
from .permission import UserPermission, AddrPermission
from .serializers import UserSerializer, AddrSerializer
from rest_framework.permissions import IsAuthenticated


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


class UserDetails(GenericViewSet, mixins.RetrieveModelMixin):
    # setting authentication
    permission_classes = [IsAuthenticated, UserPermission]
    """User Details Operation's ViewSet."""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def upload_avatar(self, request, *args, **kwargs):

        """upload user avatar"""
        avatar_url = request.data.get("avatar_url")
        print(avatar_url)
        if not avatar_url:
            return Response({"error": "upload failed,cannot be null"}, status.HTTP_400_BAD_REQUEST)
        size = avatar_url.size
        if size > 1024 * 300:
            return Response({"error": "upload failed, cannot be larger than 300kb"}, status.HTTP_400_BAD_REQUEST)
        # save file
        user = self.get_object()
        print(user)
        # gain serialization object
        serializer = self.get_serializer(user, data={"avatar": avatar_url}, partial=True)
        # verify
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"url": serializer.data["avatar"]}, status.HTTP_200_OK)


class FileView(APIView):
    def get(self, request, file_url):
        print(file_url)
        path = MEDIA_ROOT / file_url
        print(path)
        if not os.path.exists(path):
            return Response({"error": "file not exist"}, status.HTTP_400_BAD_REQUEST)
        return FileResponse(open(path, 'rb'), status.HTTP_200_OK)
        # return Response({"msg": "success"}, status.HTTP_200_OK)


class AddrView(GenericViewSet,
               mixins.ListModelMixin,
               mixins.CreateModelMixin,
               mixins.DestroyModelMixin,
               mixins.UpdateModelMixin):
    queryset = Address.objects.all()
    serializer_class = AddrSerializer
    permission_classes = [IsAuthenticated, AddrPermission]

    # config field filter
    # filterset_fields = ("user",)
    def list(self, request, *args, **kwargs):
        print(request.user)
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.filter(user=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def set_default_addr(self, request, *args, **kwargs):
        """setting default delivery address"""
        obj = self.get_object()
        obj.is_default = True
        obj.save()

        queryset = self.get_queryset().filter(user=request.user)
        for i in queryset:
            if i != obj:
                i.is_default = False
                i.save()
        return Response({"msg": "setting successfully"}, status.HTTP_200_OK)


class SendSMSView(APIView):
    throttle_classes = (AnonRateThrottle,)

    def post(self, request):
        mobile = request.data.get("mobile", "")
        if not re.match(r"^1[35678]\d{9}$", mobile):
            return Response({"error": "mobile number must be legal"}, status.HTTP_400_BAD_REQUEST)
        code = self.get_random_code()
        result = Sample.main(mobile, code)
        print(result)
        if result["code"] == "OK":
            obj = VerifCode.objects.create(mobile=mobile, code=code)
            result["codeID"] = obj.id
            return Response(result, status.HTTP_200_OK)
        else:
            return Response(result, status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return Response({"msg": "success send message code"}, status.HTTP_200_OK)

    def get_random_code(self):
        code = ''
        for i in range(6):
            n = random.choice(range(9))
            code += str(n)
        return code
