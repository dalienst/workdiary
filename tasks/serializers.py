from rest_framework import serializers

from projects.models import Project

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.username")
    project = serializers.SlugRelatedField(
        slug_field="slug", queryset=Project.objects.all()
    )
    name = serializers.CharField(max_length=1000)
    status = serializers.CharField(max_length=50, default="todo")
    priority = serializers.CharField(max_length=50, default="low")
    due_date = serializers.DateField()

    class Meta:
        model = Task
        fields = (
            "id",
            "user",
            "project",
            "name",
            "description",
            "story_points",
            "status",
            "priority",
            "due_date",
            "slug",
            "created_at",
            "updated_at",
        )

    def validate(self, data):
        project = data.get("project")
        due_date = data.get("due_date")

        if due_date and project and due_date > project.end_date:
            raise serializers.ValidationError(
                "The due date cannot be after the project end date"
            )

        return data
