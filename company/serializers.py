from django.contrib.auth import get_user_model
from rest_framework import serializers

from company.models import Company

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
        )
