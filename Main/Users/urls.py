from django.urls import path
# from . import views
from .views import login, register, user
urlpatterns = [
    path('register', register.CreateUser.as_view()),
    path('active_user', register.ActiveUser.as_view()),

    path('login', login.Login.as_view()),
    path('change-password', login.ChangePassword.as_view()),
    path('send-reset-password', login.SendResetPassword.as_view()),
    path('reset-password', login.ResetPassword.as_view()),
    path('logout', login.Logout.as_view()),

    path('profile', user.Profile.as_view()),
    path('change-avatar', user.Avatar.as_view()),
]