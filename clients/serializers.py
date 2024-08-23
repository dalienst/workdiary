from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from clients.models import Client
from invoices.serializers import InvoiceSerializer


class ClientSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Client.objects.all())],
    )
    phone = serializers.CharField(max_length=15, required=False)
    user = serializers.CharField(read_only=True, source="user.email")
    invoice = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "name",
            "email",
            "phone",
            "user",
            "slug",
            "created_at",
            "updated_at",
            "client_reference",
            "invoice",
        )

    def get_invoice(self, obj):
        invoice = obj.invoice.all()
        serializer = InvoiceSerializer(invoice, many=True)
        return serializer.data
