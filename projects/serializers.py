from rest_framework import serializers

from projects.models import Project
from tasks.serializers import TaskSerializer


class ProjectSerializer(serializers.ModelSerializer):
    # end_date = serializers.DateField()
    name = serializers.CharField(max_length=255)
    project_tasks = serializers.SerializerMethodField(read_only=True)
    # start_date = serializers.DateField()
    user = serializers.CharField(read_only=True, source="user.username")
    status = serializers.CharField(max_length=50, default="pending")

    class Meta:
        model = Project
        fields = (
            "created_at",
            # "end_date",
            "id",
            "name",
            "project_tasks",
            "reference",
            "status",
            "slug",
            # "start_date",
            "updated_at",
            "user",
            "description",
        )

    # def validate(self, attrs):
    #     start_date = attrs.get(
    #         "start_date", self.instance.start_date if self.instance else None
    #     )
    #     end_date = attrs.get(
    #         "end_date", self.instance.end_date if self.instance else None
    #     )

    #     if start_date and end_date and start_date > end_date:
    #         raise serializers.ValidationError(
    #             "The start date cannot be after the end date"
    #         )

    #     return attrs

    def get_project_tasks(self, obj):
        project_tasks = obj.project_tasks.all()
        serializer = TaskSerializer(project_tasks, many=True)
        return serializer.data
