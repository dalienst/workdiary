from rest_framework import serializers

from projects.models import Project


class ProjectSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    owner = serializers.CharField(read_only=True, source="owner.username")

    class Meta:
        model = Project
        fields = (
            "id",
            "name",
            "slug",
            "start_date",
            "end_date",
            "owner",
            "reference",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError(
                "The start date cannot be after the end date"
            )
        return attrs
