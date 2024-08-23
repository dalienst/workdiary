from django.contrib.auth import get_user_model
from rest_framework import serializers

from company.models import Company
from roles.models import Role

User = get_user_model()


class RoleSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    pay_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    overtime_rate = serializers.DecimalField(max_digits=10, decimal_places=2)
    user = serializers.CharField(read_only=True, source="user.email")
    company = serializers.SlugRelatedField(
        slug_field="name", queryset=Company.objects.all()
    )
    employees = serializers.SlugRelatedField(
        many=True,
        slug_field="email",
        queryset=User.objects.filter(is_employee=True),
        required=False,
    )

    class Meta:
        model = Role
        fields = (
            "name",
            "pay_rate",
            "overtime_rate",
            "user",
            "company",
            "employees",
            "slug",
            "reference",
            "created_at",
            "updated_at",
        )

    def validate(self, data):
        company = data.get("company")
        employees = data.get("employees", [])

        # Validate that each employee belongs to the selected company
        for employee in employees:
            if not company.employees.filter(id=employee.id).exists():
                raise serializers.ValidationError(
                    f"Employee {employee.email} is not part of the company {company.name}."
                )

        return data
