from django.urls import path

from invoices.views import (
    InvoiceClientDetailView,
    InvoiceDetailView,
    InvoiceItemDetailView,
    InvoiceItemListCreateView,
    InvoiceListCreateView,
)

urlpatterns = [
    path("", InvoiceListCreateView.as_view(), name="invoice-list"),
    path("<str:slug>/", InvoiceDetailView.as_view(), name="invoice-detail"),
    path(
        "<str:reference>/client/",
        InvoiceClientDetailView.as_view(),
        name="invoice-client-detail",
    ),
    path(
        "<str:slug>/items/",
        InvoiceItemListCreateView.as_view(),
        name="invoice-item-list",
    ),
    path(
        "<str:slug>/items/<str:item_slug>/",
        InvoiceItemDetailView.as_view(),
        name="invoice-item-detail",
    ),
]
