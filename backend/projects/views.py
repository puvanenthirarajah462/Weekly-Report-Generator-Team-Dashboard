from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer
from accounts.permissions import IsManager


class ProjectViewSet(viewsets.ModelViewSet):
    """
    List/retrieve: any authenticated user (so team members can tag reports with a project).
    Create/update/delete: managers only.
    """

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated(), IsManager()]
