from datetime import date
from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    deadline = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))

    class Meta:
        model = Task
        fields = (
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
            "tags",
            "project",
            "is_completed",
        )

    def clean_deadline(self):
        ded = self.cleaned_data["deadline"]
        if ded < date.today():
            raise forms.ValidationError("The deadline cannot be in the past.")
        return ded
