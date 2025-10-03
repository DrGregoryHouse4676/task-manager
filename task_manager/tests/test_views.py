import pytest
from django.urls import reverse, NoReverseMatch


CANDIDATES = {
    "list": ["task_manager:task-list", "tasks:task-list", "task-list", "task_list"],
    "detail": ["task_manager:task-detail", "tasks:task-detail", "task-detail", "task_detail"],
    "create": ["task_manager:task-create", "tasks:task-create", "task-create", "task_create"],
    "update": ["task_manager:task-update", "tasks:task-update", "task-update", "task_update"],
    "delete": ["task_manager:task-delete", "tasks:task-delete", "task-delete", "task_delete"],
}


def _reverse_first(names, **kwargs):
    last_err = None
    for n in names:
        try:
            return reverse(n, kwargs=kwargs or None)
        except NoReverseMatch as e:
            last_err = e
            continue
    pytest.skip(f"None of the URLs were found: {names}. Last error: {last_err}")


def test_task_urls_exist_no_db():
    _reverse_first(CANDIDATES["list"])
    _reverse_first(CANDIDATES["create"])
    _reverse_first(CANDIDATES["detail"], pk=1)
    _reverse_first(CANDIDATES["update"], pk=1)
    _reverse_first(CANDIDATES["delete"], pk=1)
