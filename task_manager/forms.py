from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from .models import Task, Tag, Project

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = (
            "name", "description", "deadline", "priority",
            "task_type", "assignees", "tags", "project", "is_completed",
        )
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
            "deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "priority": forms.Select(attrs={"class": "form-select"}),
            "task_type": forms.Select(attrs={"class": "form-select"}),
            "project": forms.Select(attrs={"class": "form-select"}),
            "assignees": forms.SelectMultiple(attrs={"class": "form-select"}),
            "tags": forms.SelectMultiple(attrs={"class": "form-select"}),
        }
        help_texts = {
            "assignees": "",
            "tags": "",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assignees"].queryset = User.objects.order_by("username")
        self.fields["tags"].queryset = Tag.objects.order_by("name")
        self.fields["project"].queryset = Project.objects.order_by("name")

        self.fields["assignees"].required = False
        self.fields["tags"].required = False
        self.fields["project"].required = False

    def clean_deadline(self):
        ded = self.cleaned_data["deadline"]
        if ded < date.today():
            raise forms.ValidationError("The deadline cannot be in the past.")
        return ded
