from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Project, UserProject
from .serializers import ProjectSerializer, ProjectDetailSerializer, UserSerializer
from accounts.models import User
from django.shortcuts import get_object_or_404


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = ProjectDetailSerializer(project)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def assign_user(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role', None)
        if not user_id:
            return Response({"detail": "Pole user_id jest wymagane."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(User, pk=user_id)
        # Sprawdzamy czy user już przypisany
        if UserProject.objects.filter(user=user, project=project).exists():
            return Response({"detail": "Użytkownik jest już przypisany do projektu."}, status=status.HTTP_400_BAD_REQUEST)
        
        UserProject.objects.create(user=user, project=project, role=role)
        return Response({"detail": "Użytkownik został przypisany do projektu."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def remove_user(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            return Response({"detail": "Pole user_id jest wymagane."}, status=status.HTTP_400_BAD_REQUEST)
        
        user_project = UserProject.objects.filter(user_id=user_id, project=project).first()
        if not user_project:
            return Response({"detail": "Użytkownik nie jest przypisany do projektu."}, status=status.HTTP_404_NOT_FOUND)

        user_project.delete()
        return Response({"detail": "Użytkownik został usunięty z projektu."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def users(self, request, pk=None):
        project = self.get_object()
        user_projects = UserProject.objects.filter(project=project)
        data = []
        for up in user_projects:
            data.append({
                "id": up.user.id,
                "login": up.user.login,
                "name": up.user.name,
                "surname": up.user.surname,
                "role": up.role
            })
        return Response(data, status=status.HTTP_200_OK)
