from django.db import models
from projects.models import Project

class Task(models.Model):
    LOCATION_TYPE_CHOICES = [
        ('0', 'No location'),
        ('1', 'QR Code scan'),
        ('2', 'GPS location'),
    ]

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='tasks')
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=200, blank=True, null=True)
    startdatetime = models.DateTimeField(null=True, blank=True)
    enddatetime = models.DateTimeField(null=True, blank=True)
    locationType = models.CharField(max_length=1, choices=LOCATION_TYPE_CHOICES, default='0')

    def __str__(self):
        return f"{self.name} (Project: {self.project.name})"
