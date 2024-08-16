from django.contrib.auth import get_user_model
from rest_framework import serializers

from payroll.models import Payroll
from schedules.models import Schedule

# from timesheets.models import Timesheet

User = get_user_model()


class PayrollSerializer(serializers.ModelSerializer):
    """
    generate payroll and deductions
    send email to employee
    """

    user = serializers.CharField(read_only=True, source="user.email")
    employee = serializers.SlugRelatedField(
        slug_field="email", queryset=User.objects.all()
    )
    start = serializers.DateField()
    end = serializers.DateField()
    schedule = serializers.SlugRelatedField(
        slug_field="reference", queryset=Schedule.objects.all()
    )

    class Meta:
        model = Payroll
        fields = (
            "id",
            "user",
            "employee",
            "start",
            "end",
            "schedule",
            "regular_hours",
            "overtime_hours",
            "gross_pay",
            "deductions",
            "net_pay",
            "is_locked",
            "reference",
            "created_at",
            "updated_at",
            "slug",
        )
