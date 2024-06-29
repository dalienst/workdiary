from django.urls import path

from clients.views import ClientDetailView, ClientListCreateView

urlpatterns = [
    path("", ClientListCreateView.as_view(), name="client-list"),
    path("<str:client_reference>/", ClientDetailView.as_view(), name="client-detail"),
]
