from django.db import models
from django.conf import settings

class Project(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name

class UserProject(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=32, blank=True, null=True)

    class Meta:
        unique_together = ('user', 'project')
