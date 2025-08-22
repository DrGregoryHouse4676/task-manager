from django.shortcuts import render
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class Position(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.PROTECT,
        related_name="workers",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.get_full_name().strip() or self.username


class TaskType(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        db_index=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=128, unique=True)
    members = models.ManyToManyField(
        "Worker",
        related_name="teams",
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Project(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="projects")
    start_date = models.DateField(default=timezone.now)
    due_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ("team", "name")
        ordering = ["name"]

    def __str__(self):
        return f"{self.team}: {self.name}"


class TaskQuerySet(models.query.QuerySet):
    def open(self):
        return self.filter(is_comleted=False)
    def close(self):
        return self.filter(is_comleted=True)
    def due_today(self):
        return self.filter(is_comleted=False, deadline=date.today())
    def overdue(self):
        return self.filter(is_comleted=False, deadline__lt=date.today())


class Task(models.Model):
    class Priority(models.TextChoices):
        URGENT = "urgent", "Urgent"
        HIGH = "high", "High"
        MEDIUM = "medium", "Medium"
        LOW = "low", "Low"

    name = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateField()
    is_comleted = models.BooleanField(default=False, db_index=True)
    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
        db_index=True
    )
    task_type = models.ForeignKey(TaskType, on_delete=models.PROTECT, related_name="tasks")
    assignees = models.ManyToManyField(Worker, related_name="tasks", blank=True)

    tags = models.ManyToManyField(Tag, related_name="tasks", blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TaskQuerySet.as_manager()

    class Meta:
        ordering = ["name", "deadline", "is_comleted"]
        indexes = [
            models.Index(fields=["deadline", "is_comleted"]),
            models.Index(fields=["priority"]),
        ]

    def __str__(self):
        return self.name

    @property
    def is_overdue(self) -> bool:
        return not self.is_comleted and self.deadline < date.today()
