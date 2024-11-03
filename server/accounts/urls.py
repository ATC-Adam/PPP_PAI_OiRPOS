from django.urls import path
from .views import UserRegistrationView, CustomAuthToken, LogoutView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),
    path('login/', CustomAuthToken.as_view(), name='api_login'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
]
