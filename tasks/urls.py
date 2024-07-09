from django.urls import path

from tasks.views import TaskDetailView, TaskListCreateView

urlpatterns = [
    path("", TaskListCreateView.as_view(), name="task-list"),
    path("<str:slug>/", TaskDetailView.as_view(), name="task-detail"),
]
