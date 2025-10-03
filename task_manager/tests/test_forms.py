from datetime import date, timedelta
import pytest
from django import forms

from task_manager.forms import TaskForm, WorkerCreateForm



def test_task_form_clean_deadline_unit_no_db():
    form = TaskForm()
    form.cleaned_data = {"deadline": date.today() - timedelta(days=1)}
    with pytest.raises(forms.ValidationError):
        form.clean_deadline()


def test_worker_create_form_widgets_no_db():
    form = WorkerCreateForm()

    assert form.fields["username"].help_text == ""
    assert form.fields["password1"].widget.attrs.get("placeholder") == "New password"
    assert form.fields["password2"].widget.attrs.get("placeholder") == "Confirm password"
    assert "form-control" in form.fields["password1"].widget.attrs.get("class", "")
    assert "form-control" in form.fields["password2"].widget.attrs.get("class", "")
    if "position" in form.fields:
        assert form.fields["position"].widget.__class__.__name__.endswith("Select")
        assert "form-select" in form.fields["position"].widget.attrs.get("class", "")
