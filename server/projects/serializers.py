from rest_framework import serializers
from .models import Project, UserProject
from accounts.models import User

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'description')


class ProjectDetailSerializer(serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', 'name', 'description', 'users')

    def get_users(self, obj):
        user_projects = UserProject.objects.filter(project=obj)
        return [
            {
                "id": up.user.id,
                "login": up.user.login,
                "name": up.user.name,
                "surname": up.user.surname,
                "role": up.role
            }
            for up in user_projects
        ]


class UserProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProject
        fields = ('id', 'user', 'project', 'role')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'login', 'name', 'surname')
