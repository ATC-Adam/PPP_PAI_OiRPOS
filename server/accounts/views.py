from rest_framework import generics, permissions, status
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class LogoutView(APIView):
    # Pozwalamy na dostęp bez uwierzytelniania
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Pobieramy token z ciała żądania
        token_key = request.data.get('auth_token')

        # Sprawdzamy, czy token został przekazany
        if not token_key:
            return Response({"detail": "Brak tokenu uwierzytelniającego."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Próbujemy znaleźć token w bazie danych
            token = Token.objects.get(key=token_key)
            # Usuwamy token (wylogowanie)
            token.delete()
            return Response({"detail": "Pomyślnie wylogowano."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            # Jeśli token nie istnieje, zwracamy błąd
            return Response({"detail": "Nieprawidłowy token."}, status=status.HTTP_400_BAD_REQUEST)