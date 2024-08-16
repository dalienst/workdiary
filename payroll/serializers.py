from django.contrib.auth import get_user_model
from rest_framework import serializers

from payroll.models import Payroll
from schedules.models import Schedule
from timesheets.models import Timesheet

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

    def validate(self, data):
        # validate end date is not before start date
        if data["end"] < data["start"]:
            raise serializers.ValidationError("End date cannot be before start date")

        # Validate that the employee belongs to the selected schedule
        if data["employee"].company != data["schedule"].company:
            raise serializers.ValidationError(
                "Employee does not belong to the selected schedule"
            )

        # ensure payroll isnt overlapping with another period
        if Payroll.objects.filter(
            employee=data["employee"],
            start__lte=data["end"],
            end__gte=data["start"],
            schedule=data["schedule"],
        ).exists():
            raise serializers.ValidationError("Payroll overlaps with another period")

        return data

    def calculate_payroll(self, validated_data):
        """
        Calculate regular hours, overtime hours, gross pay, and deductions
        """
        # Retrieve all timesheets for the employee and schedule within the given period
        timesheets = Timesheet.objects.filter(
            user=validated_data["employee"],
            shift=validated_data["schedule"],
            date__range=[validated_data["start"], validated_data["end"]],
        )

        # Calculate working hours
        regular_hours = sum(ts.total_hours for ts in timesheets if not ts.is_overtime)
        overtime_hours = sum(ts.overtime_hours for ts in timesheets if ts.is_overtime)
        role = (
            validated_data["employee"]
            .employee_roles.filter(company=validated_data["schedule"].company)
            .first()
        )

        if role:
            pay_rate = role.pay_rate
            overtime_rate = role.overtime_rate
        else:
            pay_rate = 0
            overtime_rate = 0

        # Calculate gross pay, deductions
        gross_pay = (regular_hours * pay_rate) + (overtime_hours * overtime_rate)
        # TODO: implement deductions
        deductions = 0

        # Net pay
        net_pay = gross_pay - deductions
        is_locked = True

        return {
            "regular_hours": regular_hours,
            "overtime_hours": overtime_hours,
            "gross_pay": gross_pay,
            "deductions": deductions,
            "net_pay": net_pay,
            "is_locked": is_locked,
        }

    def calculate_deductions(self, gross_pay):
        pass

    def create(self, validated_data):
        payroll_data = self.calculate_payroll(validated_data)
        validated_data.update(payroll_data)

        return super().create(validated_data)

    def update(self, instance, validated_data):
        payroll_data = self.calculate_payroll(validated_data)
        validated_data.update(payroll_data)

        return super().update(instance, validated_data)
