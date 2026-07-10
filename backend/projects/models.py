from django.conf import settings
from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="projects", blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
