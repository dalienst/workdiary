from django.urls import path

from accounts.views import LogoutView, TokenView, UserDetailView, UserRegistrationView

urlpatterns = [
    path("token/", TokenView.as_view(), name="token_obtain_pair"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("<str:id>/", UserDetailView.as_view(), name="user_detail"),
]
