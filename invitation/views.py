from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from company.permissions import IsCeo
from invitation.models import Invitation
from invitation.serializers import InvitationSerializer


class InvitationListCreateView(generics.ListCreateAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeo,
    ]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class InvitationDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Invitation.objects.all()
    serializer_class = InvitationSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeo,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
