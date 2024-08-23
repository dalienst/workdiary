from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from company.permissions import IsCeoOrIsManager
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer


class ScheduleListCreateView(generics.ListCreateAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeoOrIsManager,
    ]

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ScheduleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
    permission_classes = [
        IsAuthenticated,
        IsCeoOrIsManager,
    ]
    lookup_field = "slug"

    def get_queryset(self):
        return Schedule.objects.filter(user=self.request.user)
