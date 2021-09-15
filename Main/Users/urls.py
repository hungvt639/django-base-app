from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login.as_view()),
    path('register', views.CreateUser.as_view()),
    path('active_user', views.ActiveUser.as_view()),
    path('profile', views.Profile.as_view()),
    path('change-password', views.ChangePassword.as_view()),
    path('send-reset-password', views.SendResetPassword.as_view()),
    path('logout', views.Logout.as_view()),
    path('change-avatar', views.Avatar.as_view()),
]