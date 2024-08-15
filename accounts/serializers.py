from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)
from clients.serializers import ClientSerializer
from company.serializers import CompanySerializer
from invitation.models import Invitation
from invoices.serializers import InvoiceSerializer
from projects.serializers import ProjectSerializer
from tasks.serializers import TaskSerializer

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """
    Serializing the User model
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    first_name = serializers.CharField(max_length=255)
    last_name = serializers.CharField(max_length=255)
    avatar = serializers.ImageField(use_url=True, required=False)
    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )
    clients = serializers.SerializerMethodField(read_only=True)
    invoices = serializers.SerializerMethodField(read_only=True)
    projects = serializers.SerializerMethodField(read_only=True)
    tasks = serializers.SerializerMethodField(read_only=True)
    company = serializers.SerializerMethodField(read_only=True)
    companies = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
            "avatar",
            "contact",
            "about",
            "is_verified",
            "is_staff",
            "is_superuser",
            "is_active",
            "is_client",
            "is_employee",
            "is_ceo",
            "is_manager",
            "is_personal",
            "created_at",
            "updated_at",
            "clients",
            "invoices",
            "projects",
            "tasks",
            "company",
            "companies",
        )

    def create(self, validated_data, role_field):
        user = User.objects.create_user(**validated_data)
        setattr(user, role_field, True)
        user.is_active = True
        user.save()
        return user

    def get_clients(self, obj):
        clients = obj.clients.all()
        serializer = ClientSerializer(clients, many=True)
        return serializer.data

    def get_invoices(self, obj):
        invoices = obj.invoices.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return serializer.data

    def get_projects(self, obj):
        projects = obj.projects.all()
        serializer = ProjectSerializer(projects, many=True)
        return serializer.data

    def get_tasks(self, obj):
        tasks = obj.tasks.all()
        serializer = TaskSerializer(tasks, many=True)
        return serializer.data

    def get_company(self, obj):
        company = obj.company.all()
        serializer = CompanySerializer(company, many=True)
        return serializer.data

    def get_companies(self, obj):
        companies = obj.companies.all()
        serializer = CompanySerializer(companies, many=True)
        return serializer.data


class UserSerializer(BaseUserSerializer):
    def create(self, validated_data):
        return super().create(validated_data, role_field="is_personal")


class CeoSerializer(BaseUserSerializer):
    def create(self, validated_data):
        return super().create(validated_data, role_field="is_ceo")


class EmployeeSerializer(BaseUserSerializer):
    token = serializers.CharField(write_only=True, required=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ("token",)

    def create(self, validated_data):
        token = validated_data.pop("token", None)

        # Validate the token
        try:
            invitation = Invitation.objects.get(token=token)
        except Invitation.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired token.")

        if invitation.expiry < timezone.now():
            raise serializers.ValidationError("Token has expired.")

        # Create the user and set the employee flag
        user = super().create(validated_data, role_field="is_employee")

        # Associate the user with the company
        user.company.add(invitation.company)

        # Optionally, you may want to delete the invitation after use
        invitation.delete()

        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True)
