from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View, generic

from .forms import TaskForm, WorkerCreateForm, WorkerUpdateForm
from .models import Task, Worker


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    template_name = "task_manager/task_list.html"
    context_object_name = "task_list"
    paginate_by = 20

    def get_queryset(self):
        querys = (
            Task.objects.all()
            .select_related("task_type", "project")
            .prefetch_related("assignees", "tags")
        )
        status = self.request.GET.get("status")
        if status == "open":
            querys = querys.open()
        elif status == "closed":
            querys = querys.closed()

        if prior := self.request.GET.get("priority"):
            querys = querys.filter(priority=prior)

        if self.request.GET.get("mine"):
            querys = querys.filter(assignees=self.request.user)

        if tipy := self.request.GET.get("type"):
            querys = querys.filter(task_type_id=tipy)

        if tag := self.request.GET.get("tag"):
            querys = querys.filter(tags__name__iexact=tag)

        if q := self.request.GET.get("q"):
            querys = querys.filter(Q(name__icontains=q)
                                   | Q(description__icontains=q))

        return querys.order_by(*Task._meta.ordering)


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("task_type", "project")
            .prefetch_related("assignees", "tags")
        )


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("task_manager:task-list")


class TaskToggleCompleteView(LoginRequiredMixin, View):
    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.is_completed = not task.is_completed
        task.save(update_fields=["is_completed"])
        return redirect("task_manager:task-detail", pk=pk)


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 20
    queryset = Worker.objects.select_related("position")


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        tasks_querys = (
            Task.objects.filter(assignees=self.object)
            .select_related("task_type", "project")
            .prefetch_related("tags")
        )
        ctx["tasks_open"] = tasks_querys.open()
        ctx["tasks_done"] = tasks_querys.closed()
        return ctx


class TaskDeleteView(generic.DeleteView):
    model = Task
    success_url = reverse_lazy("task_manager:task-list")
    template_name = ("task_manager/confirm_delete.html")


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreateForm
    template_name = "task_manager/worker_form.html"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    template_name = "task_manager/worker_form.html"
    success_url = reverse_lazy("task_manager:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    template_name = "task_manager/worker_confirm_delete.html"
    success_url = reverse_lazy("task_manager:worker-list")
