from django.contrib.auth import get_user_model
from rest_framework import serializers

from clients.models import Client
from invoices.models import Invoice, InvoiceItem

User = get_user_model()


class InvoiceItemSerializer(serializers.ModelSerializer):
    invoice = serializers.SlugRelatedField(
        slug_field="slug", queryset=Invoice.objects.all()
    )
    description = serializers.CharField(max_length=10000)
    quantity = serializers.IntegerField(default=1)
    unit_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    user = serializers.CharField(read_only=True, source="user.email")

    class Meta:
        model = InvoiceItem
        fields = (
            "id",
            "invoice",
            "description",
            "quantity",
            "unit_price",
            "total_price",
            "item_slug",
            "user",
            "created_at",
            "updated_at",
        )


class InvoiceSerializer(serializers.ModelSerializer):
    client = serializers.SlugRelatedField(
        slug_field="email", queryset=Client.objects.all()
    )
    user = serializers.CharField(read_only=True, source="user.email")
    title = serializers.CharField(max_length=255)
    issue_date = serializers.DateField()
    due_date = serializers.DateField()
    items = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "client",
            "user",
            "title",
            "issue_date",
            "due_date",
            "is_paid",
            "total_amount",
            "items",
            "slug",
            "reference",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        # Remove items from validated_data if present, otherwise default to an empty list
        items_data = validated_data.pop("items", [])
        invoice = Invoice.objects.create(**validated_data)

        for item_data in items_data:
            InvoiceItem.objects.create(invoice=invoice, user=invoice.user, **item_data)

        invoice.update_total_amount()
        return invoice

    def get_items(self, obj):
        items = obj.items.all()
        serializer = InvoiceItemSerializer(items, many=True)
        return serializer.data

    def update(self, instance, validated_data):
        # Remove items from validated_data if present, otherwise default to an empty list
        items_data = validated_data.pop("items", None)

        instance.title = validated_data.get("title", instance.title)
        instance.issue_date = validated_data.get("issue_date", instance.issue_date)
        instance.due_date = validated_data.get("due_date", instance.due_date)
        instance.is_paid = validated_data.get("is_paid", instance.is_paid)
        instance.save()

        if items_data is not None:
            # Delete existing items and recreate them only if 'items' is in the request
            instance.items.all().delete()
            for item_data in items_data:
                InvoiceItem.objects.create(
                    invoice=instance, user=instance.user, **item_data
                )

        instance.update_total_amount()
        return instance


class MinimalClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = (
            "name",
            "email",
            "phone",
            "slug",
        )


class MinimalUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
        )


class MimimalInvoiceSerializer(serializers.ModelSerializer):
    client = MinimalClientSerializer(read_only=True)
    items = serializers.SerializerMethodField(read_only=True)
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "client",
            "title",
            "issue_date",
            "due_date",
            "is_paid",
            "items",
            "user",
            "reference",
            "total_amount",
            "created_at",
            "updated_at",
        )

    def get_items(self, obj):
        items = obj.items.all()
        serializer = InvoiceItemSerializer(items, many=True)
        return serializer.data
