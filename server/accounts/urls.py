# accounts/urls.py

from django.urls import path
from .views import UserRegistrationView, CustomAuthToken, LogoutView, ChangePasswordView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]
