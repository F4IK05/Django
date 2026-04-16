from django.core.exceptions import ValidationError
from django import forms


class NoteForm(forms.Form):
    CATEGORY_CHOICES = [
        ("study", "Study"),
        ("work", "Work"),
        ("personal", "Personal"),
    ]

    title = forms.CharField(label="Title", max_length=100, widget=forms.TextInput(attrs={"class": "form-control"}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"class": "form-control", "rows": 4}))
    category = forms.ChoiceField(label="Category", choices=CATEGORY_CHOICES, widget=forms.Select(attrs={"class": "form-select"}))
    tags = forms.CharField(label="Tags", required=False, help_text="Comma-separated tags", widget=forms.TextInput(attrs={"class": "form-control"}))

    def clean_title(self):
        title = self.cleaned_data.get("title")

        if title.lower().startswith("test"):
            raise ValidationError("Title cannot start with 'test'")

        return title