from types import SimpleNamespace

from django.contrib import admin as dj_admin

import task_manager.admin as adm
from task_manager.models import (
    Position, Worker, TaskType, Task, Tag, Team, Project
)


def _get_admin(model):
    _ = adm  # noqa: F841
    assert model in dj_admin.site._registry, f"{model.__name__}not registered in the admin"
    return dj_admin.site._registry[model]


def test_admin_registration_classes():
    assert _get_admin(Position).__class__ is adm.PositionAdmin
    assert _get_admin(Worker).__class__ is adm.WorkerAdmin
    assert _get_admin(TaskType).__class__ is adm.TaskTypeAdmin
    assert _get_admin(Tag).__class__ is adm.TagAdmin
    assert _get_admin(Team).__class__ is adm.TeamAdmin
    assert _get_admin(Project).__class__ is adm.ProjectAdmin
    assert _get_admin(Task).__class__ is adm.TaskAdmin


def test_position_admin_opts():
    a = _get_admin(Position)
    assert a.search_fields == ("name",)


def test_worker_admin_opts():
    a = _get_admin(Worker)
    assert a.list_display == ("username", "email", "first_name", "last_name", "position")
    assert a.list_filter == ("position", "is_staff", "is_active")
    assert a.search_fields == ("username", "first_name", "last_name", "email")


def test_tasktype_admin_opts():
    a = _get_admin(TaskType)
    assert a.search_fields == ("name",)


def test_tag_admin_opts():
    a = _get_admin(Tag)
    assert a.search_fields == ("name",)


def test_team_admin_opts():
    a = _get_admin(Team)
    assert a.search_fields == ("name",)
    assert a.filter_horizontal == ("members",)


def test_project_admin_opts():
    a = _get_admin(Project)
    assert a.list_display == ("name", "team", "start_date", "due_date")
    assert a.list_filter == ("team",)
    assert a.search_fields == ("name", "description")


def test_task_admin_opts_and_queryset_optimized():
    a = _get_admin(Task)
    assert a.list_display == (
        "name", "task_type", "priority", "deadline", "is_completed", "project"
    )
    assert a.list_filter == ("task_type", "priority", "is_completed", "project", "tags")
    assert a.search_fields == ("name", "description")
    assert a.filter_horizontal == ("tags", "assignees")

    qs = a.get_queryset(SimpleNamespace(user=None))

    lookups = getattr(qs, "_prefetch_related_lookups", ())
    assert {"tags", "assignees"}.issubset(set(lookups))

    sr = getattr(qs.query, "select_related", None)
    if isinstance(sr, dict):
        ok = {"task_type", "project"}.issubset(set(sr.keys()))
    else:
        sql = str(qs.query)
        ok = (TaskType._meta.db_table in sql) and (Project._meta.db_table in sql)
    assert ok, "Очікуємо select_related на task_type і project"
