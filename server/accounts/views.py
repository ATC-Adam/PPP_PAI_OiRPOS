# accounts/views.py

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    CustomAuthTokenSerializer,
    ChangePasswordSerializer
)
from django.contrib.auth import authenticate
from rest_framework.authtoken.views import ObtainAuthToken

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class CustomAuthToken(ObtainAuthToken):
    serializer_class = CustomAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'login': user.login,
            'name': user.name,
            'surname': user.surname,
        })

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get('old_password')):
                return Response({"old_password": "Stare hasło jest nieprawidłowe."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.data.get('new_password'))
            user.save()
            return Response({"detail": "Hasło zostało zmienione."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        token_key = request.data.get('auth_token')

        if not token_key:
            return Response({"detail": "Brak tokenu uwierzytelniającego."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = Token.objects.get(key=token_key)
            token.delete()
            return Response({"detail": "Pomyślnie wylogowano."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "Nieprawidłowy token."}, status=status.HTTP_400_BAD_REQUEST)