from django.urls import path

from payroll.views import PayrollDetailView, PayrollListCreateView

urlpatterns = [
    path("", PayrollListCreateView.as_view(), name="payroll-list"),
    path("<str:slug>/", PayrollDetailView.as_view(), name="payroll-detail"),
]
