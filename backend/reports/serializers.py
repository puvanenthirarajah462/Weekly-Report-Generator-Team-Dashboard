from django.utils import timezone
from rest_framework import serializers
from .models import WeeklyReport


class WeeklyReportSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    project_name = serializers.CharField(source="project.name", read_only=True, default=None)

    class Meta:
        model = WeeklyReport
        fields = [
            "id", "user", "username", "project", "project_name", "week_start",
            "tasks_completed", "tasks_planned", "blockers", "hours_worked",
            "notes", "status", "submitted_at", "created_at", "updated_at",
        ]
        read_only_fields = ["user", "submitted_at", "created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        if validated_data.get("status") == WeeklyReport.Status.SUBMITTED:
            validated_data["submitted_at"] = timezone.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        becoming_submitted = (
            validated_data.get("status") == WeeklyReport.Status.SUBMITTED
            and instance.status != WeeklyReport.Status.SUBMITTED
        )
        if becoming_submitted:
            validated_data["submitted_at"] = timezone.now()
        return super().update(instance, validated_data)
