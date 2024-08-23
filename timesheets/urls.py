from django.urls import path

from timesheets.views import (
    CheckinView,
    CheckoutView,
    FinanceTimeSheetListView,
    TimesheetList,
)

urlpatterns = [
    path("", TimesheetList.as_view(), name="timesheets"),
    path("timesheets/", FinanceTimeSheetListView.as_view(), name="finance_timesheet"),
    path("checkin/", CheckinView.as_view(), name="checkin"),
    path("checkout/<str:slug>/", CheckoutView.as_view(), name="checkout"),
]
