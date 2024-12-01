# accounts/views.py

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .models import User
from .serializers import (
    UserRegistrationSerializer,
    CustomAuthTokenSerializer,
    ChangePasswordSerializer,
    UpdateProfileSerializer
)
from django.contrib.auth import authenticate

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

        response = Response({
            'user_id': user.pk,
            'login': user.login,
            'name': user.name,
            'surname': user.surname,
        })

        response.set_cookie(
            key='auth_token',
            value=token.key,
            httponly=True,
            secure=False,  # Set to True in production
            samesite='Lax'
        )

        return response

class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ChangePasswordView, self).dispatch(*args, **kwargs)

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
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        response = Response({"detail": "Pomyślnie wylogowano."}, status=status.HTTP_200_OK)
        response.delete_cookie('auth_token')
        return response

class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        serializer = UpdateProfileSerializer(user, data=request.data, partial=True, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Profil został zaktualizowany."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
