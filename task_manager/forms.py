from datetime import date

from django import forms

from .models import Project, Tag, Task, Worker

class TaskForm(forms.ModelForm):
    deadline = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"})
    )
    assignees = forms.ModelMultipleChoiceField(
        queryset=Worker.objects.all(),
        widget=forms.Select(attrs={"class": "form-control", "size": 6}),
    )
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.Select(attrs={"class": "form-check" , "size": 6}),
    )
    project = forms.ModelChoiceField(
        queryset=Project.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        required=False
    )

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
        widgets = {
            "assignees": forms.SelectMultiple(
                attrs={"class": "form-control"}
            ),
            "tags": forms.CheckboxSelectMultiple(
                attrs={"class": "form-check"}
            ),
            "project": forms.Select(
                attrs={"class": "form-control"}
            ),
            "deadline": forms.DateInput(
                attrs={"type": "date"}
            ),
        }

    def clean_deadline(self):
        ded = self.cleaned_data["deadline"]
        if ded < date.today():
            raise forms.ValidationError("The deadline cannot be in the past.")
        return ded
