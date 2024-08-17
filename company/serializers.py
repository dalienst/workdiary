from django.contrib.auth import get_user_model
from rest_framework import serializers

from company.models import Company
from roles.serializers import RoleSerializer
from schedules.serializers import ScheduleSerializer

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    user = serializers.CharField(read_only=True, source="user.email")
    location = serializers.CharField(max_length=255)
    contact = serializers.CharField(max_length=255)
    no_of_employees = serializers.CharField(max_length=255)
    field = serializers.CharField(max_length=255)
    logo = serializers.ImageField(use_url=True, required=False)
    employees = serializers.SlugRelatedField(
        many=True,
        slug_field="email",
        queryset=User.objects.filter(is_employee=True),
        required=False,
    )
    company_schedules = serializers.SerializerMethodField(read_only=True)
    company_roles = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Company
        fields = (
            "name",
            "user",
            "location",
            "contact",
            "no_of_employees",
            "field",
            "logo",
            "employees",
            "description",
            "slug",
            "reference",
            "created_at",
            "updated_at",
            "company_schedules",
            "company_roles",
        )

    def get_company_schedules(self, obj):
        company_schedules = obj.company_schedules.all()
        serializer = ScheduleSerializer(company_schedules, many=True)
        return serializer.data

    def get_company_roles(self, obj):
        company_roles = obj.company_roles.all()
        serializer = RoleSerializer(company_roles, many=True)
        return serializer.data
