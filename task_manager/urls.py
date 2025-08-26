from django.urls import path
from . import views
from .views import WorkerCreationForm, WorkerListView

app_name = "task_manager"

urlpatterns = [
    path(
        "",
        views.TaskListView.as_view(),
        name="task-list"
    ),
    path(
        "tasks/<int:pk>/",
        views.TaskDetailView.as_view(),
        name="task-detail"
    ),
    path(
        "tasks/create/",
        views.TaskCreateView.as_view(),
        name="task-create"
    ),
    path(
        "tasks/<int:pk>/edit/",
        views.TaskUpdateView.as_view(),
        name="task-edit"
    ),
    path(
        "tasks/<int:pk>/toggle/",
        views.TaskToggleCompleteView.as_view(),
        name="task-toggle"
    ),
    path(
        "workers/",
        views.WorkerListView.as_view(),
        name="worker-list"
    ),
    path(
        "workers/<int:pk>/",
        views.WorkerDetailView.as_view(),
        name="worker-detail"
    ),
    path(
        "tasks/<int:pk>/update/",
        views.TaskUpdateView.as_view(),
        name="task-update"
    ),
    path(
        "tasks/<int:pk>/delete/",
        views.TaskDeleteView.as_view(),
        name="task-delete"
    ),
]
