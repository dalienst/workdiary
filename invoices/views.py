from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from invoices.models import Invoice, InvoiceItem
from invoices.serializers import (
    InvoiceItemSerializer,
    InvoiceSerializer,
    MimimalInvoiceSerializer,
)


class InvoiceListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceSerializer
    queryset = Invoice.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        return Invoice.objects.filter(user=self.request.user)


class InvoiceClientDetailView(generics.RetrieveAPIView):
    serializer_class = MimimalInvoiceSerializer
    queryset = Invoice.objects.all()
    lookup_field = "reference"


class InvoiceItemListCreateView(generics.ListCreateAPIView):
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InvoiceItem.objects.filter(invoice__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvoiceItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = InvoiceItemSerializer
    queryset = InvoiceItem.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = "item_slug"

    def get_queryset(self):
        return InvoiceItem.objects.filter(invoice__user=self.request.user)
