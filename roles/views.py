from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from company.permissions import IsCeoOrIsManager
from roles.models import Role
from roles.serializers import RoleSerializer


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeoOrIsManager,
    ]

    def get_queryset(self):
        return Role.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeoOrIsManager,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return Role.objects.filter(user=self.request.user)
