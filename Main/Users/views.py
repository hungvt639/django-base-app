from rest_framework import generics
from .models import MyUsers
from rest_framework.response import Response
from .serializer import UserSerializer, CreateUserSerializer, EditUserSerializer, ChangePassworSerializer, EditAvatar
from rest_framework import permissions, status, parsers
from .permissions import user_permission
from .utils import generate_access_token, generate_refresh_token, generate_active_token
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
                    "href": "{}/user/active?active_token={}".format(settings.HOST_FRONTEND, generate_active_token(user)),
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


class Logout(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


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


class SendResetPassword(generics.ListCreateAPIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        if not username:
            return Response({"message": "Vui lòng cung cấp tên tài khoản"}, status=status.HTTP_400_BAD_REQUEST)
        user = MyUsers.objects.filter(username=username).first()
        if user is None:
            return Response({"message": "Không tìm thấy tài khoản nào trùng với tên tài khoản đã cung cấp"},
                            status=status.HTTP_400_BAD_REQUEST)
        if not user.email:
            return Response({"message": "Tài khoản chưa liên kết email"}, status=status.HTTP_400_BAD_REQUEST)
        email = EmailMessage('Reset Password',
                             'Chúng tôi đã nhận được yêu cầu đổi mật khẩu cảu bạn. Vui lòng bấm vào <a>đây</a>',
                             to=[user.email])
        email.send()
        return Response(
            {"message": "Chúng tôi đã gửi email tới bạn. Bạn vui lòng kiểm tra email để cập nhật mật khẩu mới"},
            status=status.HTTP_400_BAD_REQUEST)
