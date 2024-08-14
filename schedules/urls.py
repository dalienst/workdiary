from django.urls import path

from schedules.views import ScheduleDetailView, ScheduleListCreateView

urlpatterns = [
    path("", ScheduleListCreateView.as_view(), name="schedule-list"),
    path("<str:slug>/", ScheduleDetailView.as_view(), name="schedule-detail"),
]
