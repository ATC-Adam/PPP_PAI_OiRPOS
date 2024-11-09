# accounts/urls.py

from django.urls import path
from .views import (
    UserRegistrationView,
    CustomAuthToken,
    LogoutView,
    ChangePasswordView,
    UpdateProfileView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
]
