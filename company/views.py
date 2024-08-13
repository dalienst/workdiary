from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from company.models import Company
from company.permissions import IsCeo
from company.serializers import CompanySerializer


class CompanyListCreateView(generics.ListCreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticated,
        IsCeo,
    ]

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticated,
        IsCeo,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)


class CompanyPublicProfile(generics.RetrieveAPIView):
    serializer_class = CompanySerializer
    permission_classes = [
        AllowAny,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return Company.objects.filter(slug=self.kwargs["slug"])


class CompanyListView(generics.ListAPIView):
    serializer_class = CompanySerializer
    permission_classes = [
        AllowAny,
    ]
    queryset = Company.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = [
        "field",
        "location",
    ]
