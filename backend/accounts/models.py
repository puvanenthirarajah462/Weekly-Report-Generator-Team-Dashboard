from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        TEAM_MEMBER = "team_member", "Team Member"
        MANAGER = "manager", "Manager"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.TEAM_MEMBER)
    email = models.EmailField(unique=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    @property
    def is_manager(self):
        return self.role == self.Role.MANAGER

    def __str__(self):
        return f"{self.username} ({self.role})"
