from django.contrib.auth import get_user_model
from django.utils import timezone as django_timezone
from rest_framework import serializers

from company.models import Company
from invitation.models import Invitation
from invitation.utils import generate_token, send_invitation_email

User = get_user_model()


class InvitationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    company = serializers.SlugRelatedField(
        slug_field="name", queryset=Company.objects.all()
    )
    user = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = Invitation
        fields = (
            "id",
            "email",
            "token",
            "expiry",
            "company",
            "user",
            "slug",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        email = validated_data["email"]
        company = validated_data["company"]
        user = self.context["request"].user

        # Check if invitation already exists
        existing_invitation = Invitation.objects.filter(
            email=email, company=company
        ).first()

        # TODO: add checks to check if email is already an employee in the company

        if existing_invitation:
            now = django_timezone.now()
            if existing_invitation.expiry > now:
                # send_invitation_email(email, existing_invitation.token, user, company)
                return existing_invitation
            else:
                # invitation exists but expired, update and resend
                existing_invitation.token = generate_token()
                existing_invitation.expiry = now + django_timezone.timedelta(days=7)
                existing_invitation.save(update_fields=["token", "expiry"])
                send_invitation_email(email, existing_invitation.token, user, company)
                return existing_invitation
        else:
            # invitation doesn't exist, create and send
            token = generate_token()
            expiry = django_timezone.now() + django_timezone.timedelta(days=7)
            invitation = Invitation.objects.create(
                token=token, expiry=expiry, email=email, company=company, user=user
            )
            send_invitation_email(email, token, user, company)
            return invitation
