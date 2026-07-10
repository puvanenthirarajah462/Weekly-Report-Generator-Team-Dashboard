from rest_framework import serializers
from .models import Project


class ProjectSerializer(serializers.ModelSerializer):
    member_ids = serializers.PrimaryKeyRelatedField(
        source="members", many=True, queryset=Project.members.field.related_model.objects.all(),
        required=False, write_only=True,
    )
    members = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Project
        fields = ["id", "name", "description", "is_active", "members", "member_ids", "created_at"]

    def get_members(self, obj):
        return [{"id": m.id, "username": m.username} for m in obj.members.all()]
