from rest_framework import generics
from ..models import MyUsers
from rest_framework.response import Response
from ..serializer import UserSerializer, CreateUserSerializer, EditUserSerializer, ChangePassworSerializer, EditAvatar
from rest_framework import permissions, status, parsers
from ..permissions import user_permission
from ..utils import generate_access_token, generate_refresh_token, generate_active_token
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings
import jwt


class Profile(generics.ListCreateAPIView):
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser, parsers.FileUploadParser,)

    def get(self, request, *args, **kwargs):
        try:
            serializer = UserSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            respone = {"message": ["Error"]}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = EditUserSerializer(user, request.data)
            # import pdb; pdb.set_trace()
            if serializer.is_valid():
                serializer.save()
                user = serializer.data.copy()
                return Response(user, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            respone = {"message": ["Error"]}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)


class Avatar(generics.ListCreateAPIView):
    parser_classes = (parsers.MultiPartParser, parsers.JSONParser, parsers.FileUploadParser,)

    def post(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        try:
            user = request.user
            serializer = EditAvatar(user, request.data)
            if serializer.is_valid():
                serializer.save()
                avatar = serializer.data.copy()
                return Response(avatar, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            respose = {"message": "Đã có lỗi sảy ra, bạn vui lòng thử lại"}
            return Response(respose, status=status.HTTP_400_BAD_REQUEST)
