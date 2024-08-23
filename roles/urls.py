from django.urls import path

from roles.views import RoleDetailView, RoleListCreateView

urlpatterns = [
    path("", RoleListCreateView.as_view(), name="role-list"),
    path("<str:slug>/", RoleDetailView.as_view(), name="role-detail"),
]
