from rest_framework import generics
from ..models import MyUsers
from rest_framework.response import Response
from ..serializer import UserSerializer, CreateUserSerializer, EditUserSerializer, ChangePassworSerializer, EditAvatar
from rest_framework import permissions, status, parsers
from ..permissions import user_permission
from ..utils import generate_access_token, generate_refresh_token, generate_active_token, generate_reset_password_token
from django.core.mail import EmailMessage
from django.template.loader import get_template
from django.conf import settings
import jwt


class Login(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        if username and password:
            user = MyUsers.objects.filter(username=username).first()
            if user is None:
                return Response({"message": ["Tài khoản không tồn tại"]},
                                status=status.HTTP_400_BAD_REQUEST)
            if not user.check_password(password):
                return Response({"message": ["Mật khẩu không chính xác"]},
                                status=status.HTTP_400_BAD_REQUEST)
            if not user.is_active:
                return Response({"message": ["Tài khoản chưa được kích hoạt"]},
                                status=status.HTTP_400_BAD_REQUEST)
            serialized_user = UserSerializer(user).data
            access_token = generate_access_token(user)
            refresh_token = generate_refresh_token(user)

            response = Response()
            response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
            response.data = {
                'token': access_token,
                'user': serialized_user,
            }

            return response
        else:
            return Response({"message": ["Vui lòng điền đầy đủ tài khoản và mật khẩu"]},
                            status=status.HTTP_400_BAD_REQUEST)

class Logout(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class ChangePassword(generics.ListCreateAPIView):
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            old_password = request.data['old_password']
            if user.check_password(old_password):
                user.set_password(request.data['password'])
                user.save()
                respone = {"message": ["Thay đổi mật khẩu thành công"]}
                return Response(respone, status=status.HTTP_200_OK)
            else:
                respone = {"message": ["Mật khẩu cũ không đúng, vui lòng nhập lại"]}
                return Response(respone, status=status.HTTP_400_BAD_REQUEST)
        except:
            respone = {"message": ["Đã có lỗi sảy ra. Bạn vui lòng thử lại sau"]}
            return Response(respone, status=status.HTTP_400_BAD_REQUEST)


class SendResetPassword(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        if not username:
            return Response({"message": ["Vui lòng cung cấp tên tài khoản"]}, status=status.HTTP_400_BAD_REQUEST)
        user = MyUsers.objects.filter(username=username).first()
        if user is None:
            return Response({"message": ["Không tìm thấy tài khoản nào trùng với tên tài khoản đã cung cấp"]},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.email:
            return Response({"message": ["Tài khoản chưa liên kết email"]}, status=status.HTTP_400_BAD_REQUEST)
        # print("user", user.username)
        # import pdb; pdb.set_trace()
        mess = {
            "fullname": "{} {}".format(user.first_name, user.last_name),
            "href": "{}/reset-password?reset_password_token={}".format(settings.HOST_FRONTEND, generate_reset_password_token(user)),
        }
        message = get_template("send_email_reset_password.html").render({
            'message': mess
        })
        mail = EmailMessage(
            subject="Quên mật khẩu",
            body=message,
            to=[user.email]
        )
        mail.content_subtype = "html"
        mail.send()

        return Response(
            {"message": ["Chúng tôi đã gửi email tới bạn. Bạn vui lòng kiểm tra email để cập nhật mật khẩu mới"]},
            status=status.HTTP_200_OK)

class ResetPassword(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        password = request.data.get("password")
        reset_password_token = request.data.get("reset_password_token")
        if not password:
            return Response({"message": ["Vui lòng cung mật khẩu"]}, status=status.HTTP_400_BAD_REQUEST)
        if not reset_password_token:
            return Response({"message": "Vui lòng cung cấp tên tài khoản"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            payload = jwt.decode(
                reset_password_token, settings.RESET_PASS_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            return Response({"message": ["Token đã hết hạn, bạn vui lòng gửi lại yêu cầu để thay đổi mật khẩu"]}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"message": ["Token bị lỗi"]}, status=status.HTTP_400_BAD_REQUEST)
        user = MyUsers.objects.filter(id=payload['user_id']).first()
        if user is None:
            return Response({"message": ["Tài khoản không tồn tại"]}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(password)
        user.save()
        return Response({"message": ["Đổi mật khẩu thành công, bạn vui lòng đăng nhập lại"]},status=status.HTTP_200_OK)