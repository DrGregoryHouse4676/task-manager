from django.contrib import admin

from .models import (
    Position,
    Worker,
    TaskType,
    Task,
    Tag,
    Team,
    Project
)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Worker)
class WorkerAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "first_name", "last_name", "position")
    list_filter = ("position", "is_staff", "is_active")
    search_fields = ("username", "first_name", "last_name", "email")


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    search_fields = ("name",)
    filter_horizontal = ("members",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "team", "start_date", "due_date")
    list_filter = ("team",)
    search_fields = ("name", "description")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "task_type",
        "priority",
        "deadline",
        "is_completed",
        "project"
    )
    list_filter = ("task_type", "priority", "is_completed", "project", "tags")
    search_fields = ("name", "description")
    filter_horizontal = ("tags", "assignees")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return (qs.select_related("task_type", "project")
                .prefetch_related("tags", "assignees"))
