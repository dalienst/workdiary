from rest_framework import serializers

from company.models import Company
from schedules.models import Schedule


class ScheduleSerializer(serializers.ModelSerializer):
    company = serializers.SlugRelatedField(
        slug_field="reference", queryset=Company.objects.all()
    )
    name = serializers.CharField(max_length=255)
    workdays = serializers.ListField(child=serializers.CharField(max_length=10))
    start_time = serializers.TimeField()
    end_time = serializers.TimeField()
    user = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Schedule
        fields = (
            "id",
            "company",
            "name",
            "workdays",
            "start_time",
            "end_time",
            "user",
            "created_at",
            "updated_at",
            "slug",
            "reference",
        )
