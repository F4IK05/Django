from datetime import date

from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from notes import data
from notes.forms import NoteForm


class AboutPageView(TemplateView):
    template_name = 'notes/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["project_name"] = "Knowledge Hub"
        context["author"] = "Nadir Zamanov"
        return context


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "notes/home.html")


# def about(request: HttpRequest) -> HttpResponse:
#     context = {
#         "project_name": "Knowledge Hub",
#         "author": "Nadir Zamanov",
#     }
#     return render(request, "notes/about.html", context)


def notes_list(request: HttpRequest) -> HttpResponse:
    return render(request, "notes/notes_list.html",
                  {"page_title": "Notes List", "notes": data.TEMP_NOTES})


def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = next((item for item in data.TEMP_NOTES if item["id"] == note_id), None)
    return render(request, "notes/note_detail.html", {"note": note})

def create_note(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            category = form.cleaned_data["category"]
            tags_raw = form.cleaned_data["tags"]

            tags = [tag.strip() for tag in tags_raw.split(",")] if tags_raw else []

            new_id = max(note["id"] for note in data.TEMP_NOTES) + 1

            new_note = {
                "id": new_id,
                "title": title,
                "content": content,
                "category": category,
                "creates_at": str(date.today()),
                "tags": tags,
            }

            data.TEMP_NOTES.append(new_note)

            return redirect("notes:notes_list")
    else:
        form = NoteForm()

    return render(request, "notes/create_note.html", {"form": form})