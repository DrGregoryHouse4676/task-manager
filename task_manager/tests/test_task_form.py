from datetime import date, timedelta

from django import forms
from django.test import TestCase

from task_manager.forms import TaskForm


class TaskFormTests(TestCase):
    def setUp(self):
        self.form = TaskForm()

    def test_fields_present(self):
        expected = {
            "name",
            "description",
            "deadline",
            "priority",
            "task_type",
            "assignees",
            "tags",
            "project",
            "is_completed",
        }
        self.assertTrue(expected.issubset(set(self.form.fields.keys())))

    def test_assignees_is_multiple_choice(self):
        field = self.form.fields["assignees"]
        self.assertIsInstance(field, forms.ModelMultipleChoiceField)

    def test_tags_is_multiple_choice(self):
        field = self.form.fields["tags"]
        self.assertIsInstance(field, forms.ModelMultipleChoiceField)

    def test_project_is_optional(self):
        field = self.form.fields["project"]
        self.assertFalse(field.required)
        self.assertIsInstance(field, forms.ModelChoiceField)

    def test_deadline_validation_rejects_past(self):
        past = date.today() - timedelta(days=1)
        form = TaskForm(data={"deadline": past})
        form.full_clean()
        self.assertIn("deadline", form.errors)
        self.assertIn("The deadline cannot be in the past.", form.errors["deadline"])
