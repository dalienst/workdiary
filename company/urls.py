from django.urls import path

from company.views import (
    CompanyDetailView,
    CompanyListCreateView,
    CompanyListView,
    CompanyPublicProfile,
)

urlpatterns = [
    path("", CompanyListCreateView.as_view(), name="company-list"),
    path("<str:slug>/", CompanyDetailView.as_view(), name="company-detail"),
    path("public/<str:slug>/", CompanyPublicProfile.as_view(), name="company-public"),
    path("public/", CompanyListView.as_view(), name="company-public-list"),
]
