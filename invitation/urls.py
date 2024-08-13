from django.urls import path

from invitation.views import InvitationDetailView, InvitationListCreateView

urlpatterns = [
    path("", InvitationListCreateView.as_view()),
    path("<str:slug>/", InvitationDetailView.as_view()),
]
