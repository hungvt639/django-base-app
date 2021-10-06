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


class CreateUser(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = CreateUserSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = CreateUserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = serializer.data.copy()
                # user.pop('password')

                mess = {
                    "fullname": user['first_name'] + " " + user['last_name'],
                    "href": "{}/activate-user?active_token={}".format(settings.HOST_FRONTEND, generate_active_token(user)),
                }
                message = get_template("send_email_active.html").render({
                    'message': mess
                })
                mail = EmailMessage(
                    subject="Kích hoạt tài khoản",
                    body=message,
                    to=[user["email"]]
                )
                mail.content_subtype = "html"
                mail.send()

                # serializer.save()
                return Response(
                    {"message": ["Đăng ký thành công", "Bạn vui lòng kiểm tra email của mình để kích hoạt tài khoản"]},
                    status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except:
            respone = {"message": "Đã có lỗi sảy ra, bạn vui lòng thử lại sau"}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)


class ActiveUser(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            active_token = request.data.get('active_token', None)
            if not active_token:
                return Response({"message": ["Không được để trống token"]}, status=status.HTTP_400_BAD_REQUEST)
            try:
                payload = jwt.decode(
                    active_token, settings.ACTIVE_KEY, algorithms=['HS256'])
                user = MyUsers.objects.filter(id=payload['user_id']).first()
                if user is None:
                    return Response({"message": ["Tài khoản không tồn tại"]}, status=status.HTTP_400_BAD_REQUEST)
                user_permission(user.id, 'user')
                user.is_active = True
                user.save()
                return Response({"message": ["Kích hoạt tài khoản thành công"]}, status=status.HTTP_200_OK)
            except jwt.ExpiredSignatureError:
                return Response({"message": ["Token đã hết hạn"]}, status=status.HTTP_400_BAD_REQUEST)
            except IndexError:
                return Response({"message": ["Token bị lỗi"]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            respone = {"message": ["Đã có lỗi sảy ra, bạn vui lòng thử lại sau"]}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)
