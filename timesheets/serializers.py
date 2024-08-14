from rest_framework import serializers

from schedules.models import Schedule
from timesheets.models import Timesheet


class TimesheetSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.email")
    shift = serializers.SlugRelatedField(
        slug_field="reference", queryset=Schedule.objects.all()
    )

    class Meta:
        model = Timesheet
        fields = (
            "id",
            "user",
            "shift",
            "date",
            "checkin",
            "checkout",
            "total_hours",
            "is_overtime",
            "status",
        )
