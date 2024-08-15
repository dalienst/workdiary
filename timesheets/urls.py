from django.urls import path

from timesheets.views import CheckinView, CheckoutView

urlpatterns = [
    path("checkin/", CheckinView.as_view(), name="checkin"),
    path("checkout/<str:slug>/", CheckoutView.as_view(), name="checkout"),
]
