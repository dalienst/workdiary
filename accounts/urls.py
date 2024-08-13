from django.urls import path

from accounts.views import (
    CeoRegistrationView,
    EmployeeCreateView,
    LogoutView,
    TokenView,
    UserDetailView,
    UserRegistrationView,
)

urlpatterns = [
    path("token/", TokenView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("corporate/", CeoRegistrationView.as_view(), name="register_ceo"),
    path("employee/", EmployeeCreateView.as_view(), name="register_employee"),
    path("<str:id>/", UserDetailView.as_view(), name="user_detail"),
]
