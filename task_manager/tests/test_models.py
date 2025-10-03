from datetime import date, timedelta

from task_manager.models import (
    Position, Worker, TaskType, Tag, Team, Project, Task
)


def test_position_str_no_db():
    p = Position(name="Backend")
    assert str(p) == "Backend"


def test_worker_str_no_db():
    w_full = Worker(username="lev", first_name="Lev", last_name="Ivanov")
    w_user = Worker(username="anon")
    assert str(w_full) == "Lev Ivanov"
    assert str(w_user) == "anon"


def test_tasktype_and_tag_str_no_db():
    assert str(TaskType(name="Bug")) == "Bug"
    assert str(Tag(name="api")) == "api"


def test_team_str_no_db():
    t = Team(name="Core Team")
    assert str(t) == "Core Team"


def test_project_str_no_db():
    pr = Project(name="Alpha", team=Team(name="A"))
    assert str(pr) == "Alpha: Alpha"


def test_task_str_and_is_overdue_no_db():
    task_today = Task(
        name="T",
        description="d",
        deadline=date.today(),
        task_type=TaskType(name="Feature"),
        project=Project(name="P", team=Team(name="T")),
    )
    assert str(task_today) == "T"

    task_over = Task(
        name="Over",
        description="d",
        deadline=date.today() - timedelta(days=1),
        is_completed=False,
        task_type=TaskType(name="X"),
        project=Project(name="P2", team=Team(name="T2")),
    )
    task_done = Task(
        name="Done",
        description="d",
        deadline=date.today() - timedelta(days=1),
        is_completed=True,
        task_type=TaskType(name="Y"),
        project=Project(name="P3", team=Team(name="T3")),
    )
    assert task_over.is_overdue is True
    assert task_done.is_overdue is False
