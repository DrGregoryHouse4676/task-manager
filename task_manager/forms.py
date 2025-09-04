from datetime import date
from django import forms
from django.contrib.auth import get_user_model
from .models import Task, Tag, Project, Worker
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

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
            "description": forms.Textarea(attrs={"class": "form-control"}),
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


class WorkerCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "autocomplete": "username"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "autocomplete": "email"}),
            "position": forms.Select(attrs={"class": "form-select"}),
        }
        help_texts = {
            "username": "",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if email and Worker.objects.filter(email__iexact=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
                "placeholder": "New password",
            }
        )
        self.fields["password2"].widget = forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "new-password",
                "placeholder": "Confirm password",
            }
        )
        self.fields["password1"].help_text = "Please enter your new password"
        self.fields["password2"].help_text = "Please confirm your new password"


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("username", "first_name", "last_name", "email", "position", "is_active")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "position": forms.Select(attrs={"class": "form-select"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        help_texts = {"username": ""}

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            return email
        qs = Worker.objects.filter(email__iexact=email)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise ValidationError("A user with this email already exists.")
        return email
