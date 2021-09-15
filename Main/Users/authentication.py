import jwt
from rest_framework.authentication import BaseAuthentication
from django.middleware.csrf import CsrfViewMiddleware
from rest_framework import exceptions
from django.conf import settings
from .models import MyUsers


class CSRFCheck(CsrfViewMiddleware):
    def _reject(self, request, reason):
        return reason


class SafeJWTAuthentication(BaseAuthentication):

    def authenticate(self, request):
        authorization_heaader = request.headers.get('Authorization')
        if not authorization_heaader:
            return None
        try:
            access_token = authorization_heaader.split(' ')[1]
            payload = jwt.decode(
                access_token, settings.SECRET_KEY, algorithms=['HS256'])

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed('Access_token đã hết hạn')
        except:
            raise exceptions.AuthenticationFailed('Token bị lỗi')

        user = MyUsers.objects.filter(id=payload['user_id']).first()
        if user is None:
            raise exceptions.AuthenticationFailed('Không có tài khoản này')
        if not user.is_active:
            raise exceptions.AuthenticationFailed('Tài khoản chưa được kích hoạt')

        self.enforce_csrf(request)
        return (user, None)

    def enforce_csrf(self, request):
        check = CSRFCheck()
        check.process_request(request)
        reason = check.process_view(request, None, (), {})
        print(reason)
        if reason:
            raise exceptions.PermissionDenied('CSRF Failed: %s' % reason)