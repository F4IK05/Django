from django.http import HttpResponse, HttpRequest, HttpResponseRedirect
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.utils.html import escape
from django.urls import reverse

from notes import data


# Create your views here.

def _html_shell(title: str, body: str) -> str:
    safe_title = escape(title)
    return f"""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{safe_title}</title>

    <link
        href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
        rel="stylesheet"
    >

    <style>
        body {{
            background: #f0f4f8;
            min-height: 100vh;
            font-family: system-ui, -apple-system, sans-serif;
        }}

        .navbar {{
    background: #1a1f36 !important;
            padding: 0.6rem 0;
            border-bottom: 1px solid rgba(255,255,255,0.06);
        }}

        .navbar-brand {{
            font-weight: 500;
            font-size: 1rem;
            letter-spacing: 0.3px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .nav-link {{
            color: rgba(255,255,255,0.6) !important;
            font-size: 0.875rem;
            padding: 6px 12px !important;
            border-radius: 7px;
            transition: background 0.15s, color 0.15s;
        }}

        .nav-link:hover,
        .nav-link.active {{
            color: #fff !important;
            background: rgba(255,255,255,0.08);
        }}

        .btn-newnote {{
            background: #6b8cff;
            color: #fff !important;
            font-size: 0.8125rem;
            font-weight: 500;
            padding: 7px 14px;
            border-radius: 8px;
            transition: background 0.15s;
            border: none;
        }}

        .btn-newnote:hover {{
            background: #5a7aee;
            color: #fff !important;
        }}

        .main-card {{
            border: 1px solid rgba(0,0,0,0.07);
            border-radius: 16px;
            box-shadow: none;
            background: #fff;
        }}

        .main-card .card-body {{
            padding: 2rem 2.25rem;
        }}

        code {{
            background: #f5f6f8;
            padding: 0.15rem 0.4rem;
            border-radius: 6px;
            color: #c2185b;
            font-size: 0.875em;
            border: 1px solid rgba(0,0,0,0.06);
        }}

        .notes li {{
            margin - bottom: 0.5rem;
        }}

        textarea {{
            min-height: 140px;
            resize: vertical;
            border-radius: 10px !important;
            border-color: rgba(0,0,0,0.12) !important;
            font-size: 0.9375rem;
        }}

        textarea:focus {{
            border-color: #6b8cff !important;
            box-shadow: 0 0 0 3px rgba(107,140,255,0.15) !important;
        }}

        .form-control {{
            border-radius: 10px;
            border-color: rgba(0,0,0,0.12);
            font-size: 0.9375rem;
        }}

        .form-control:focus {{
            border-color: #6b8cff;
            box-shadow: 0 0 0 3px rgba(107,140,255,0.15);
        }}

        .btn-primary {{
            background: #1a1f36;
            border: none;
            border-radius: 8px;
            padding: 9px 20px;
            font-size: 0.875rem;
            font-weight: 500;
        }}

        .btn-primary:hover {{
            background: #252b47;
        }}

        .btn-outline-secondary {{
            border-color: rgba(0,0,0,0.15);
            color: #555;
            border-radius: 8px;
            padding: 9px 20px;
            font-size: 0.875rem;
        }}

        .btn-outline-secondary:hover {{
            background: #f5f6f8;
            border-color: rgba(0,0,0,0.2);
            color: #333;
        }}

        footer {{
            color: #aaa;
            font-size: 0.8125rem;
            border-top: 1px solid rgba(0,0,0,0.07);
            background: transparent;
        }}

        footer .accent {{
            color: #6b8cff;
        }}
    </style>
</head>
<body>

    <nav class="navbar navbar-expand-lg navbar-dark shadow-none">
        <div class="container">
            <a class="navbar-brand text-white" href="{escape(reverse('home'))}">MySite</a>

            <button
                class="navbar-toggler border-0"
                type="button"
                data-bs-toggle="collapse"
                data-bs-target="#mainNavbar"
                aria-controls="mainNavbar"
                aria-expanded="false"
                aria-label="Toggle navigation"
            >
                <span class="navbar-toggler-icon"></span>
            </button>

            <div class="collapse navbar-collapse" id="mainNavbar">
                <ul class="navbar-nav ms-auto mb-2 mb-lg-0 align-items-lg-center gap-1">
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('home'))}">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('about'))}">About</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="{escape(reverse('notes_list'))}">Notes</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <main class="container py-5">
        <div class="card-body">
            {body}
        </div>
    </main>

    <script
        src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js">
    </script>
</body>
</html>
    """


def _csrf_field(request: HttpRequest) -> str:
    token = get_token(request)
    return f'<input type="hidden" name="csrfmiddlewaretoken" value="{escape(token)}">'


def home(request: HttpRequest) -> HttpResponse:
    body = f"""
        <div class="d-flex justify-content-center align-items-center py-3">
            <div class="bg-white border-0 rounded-4 p-5 text-center" style="max-width: 480px; width: 100%; border: 1px solid rgba(0,0,0,0.07) !important;">

                <h1 class="mb-2" style="font-size: 2rem; font-weight: 700; color: #1a1f36;">
                    Knowledge Hub
                </h1>
                <p class="mb-4" style="font-size: 0.9375rem; color: #888; line-height: 1.6;">
                    Your personal space for notes and ideas.<br>Start by browsing what you've saved.
                </p>

                <a href="{escape(reverse('notes_list'))}"
                   class="btn d-inline-flex align-items-center justify-content-center gap-2 mx-auto"
                   style="
                       background: #1a1f36; color: #fff; border: none;
                       padding: 10px 24px; border-radius: 9px;
                       font-size: 0.875rem; font-weight: 500;
                       text-decoration: none; width: fit-content;
                       transition: background 0.15s;
                   "
                   onmouseover="this.style.background='#252b47'"
                   onmouseout="this.style.background='#1a1f36'">
                    <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/>
                    </svg>
                    Go to Notes
                </a>

            </div>
        </div>
    """
    return HttpResponse(_html_shell("Knowledge Hub - home page", body))


def about(request: HttpRequest) -> HttpResponse:
    body = f"""
            <div class="d-flex justify-content-center">
    <div class="card shadow-lg border-0 rounded-4 p-4 text-center" style="max-width: 500px;">

        <h1 class="fw-bold mb-3">ℹ️ About this Project</h1>

        <p class="text-muted mb-2">
            Knowledge Hub — project for Django course
        </p>

        <p class="badge bg-primary-subtle text-primary px-3 py-2">
            Lesson 7 — Views & Routes
        </p>

    </div>
</div>
        """
    return HttpResponse(_html_shell("Knowledge Hub - about page", body))


def notes_list(request: HttpRequest) -> HttpResponse:
    raw_tag = request.GET.get('tag')
    raw_category = request.GET.get('category')

    notes = data.list_notes()

    if raw_tag:
        tag_filter = raw_tag.strip().lower()
        notes = [n for n in notes if n['tag'.lower()] == tag_filter]

    if raw_tag:
        category_filter = raw_category.strip().lower()
        notes = [n for n in notes if n['category'.lower()] == category_filter]

    items: list[str] = []
    for note in notes:
        url = reverse('note_detail', kwargs={'note_id': note['id']})
        items.append(f"""
        
        <li class="list-group-item d-flex align-items-center justify-content-between"
            style="border-color: rgba(0,0,0,0.06); transition: background 0.15s; cursor: pointer;"
            onmouseover="this.style.background='#f8f9fb'"
            onmouseout="this.style.background=''">

            <a href="{escape(url)}" class="px-2 py-3 d-flex align-items-center justify-content-between w-100" style="text-decoration: none;">
                <div class="d-flex align-items-center gap-3">
                    <div style="
                        width: 34px; height: 34px; border-radius: 9px;
                        background: #eef1ff; flex-shrink: 0;
                        display: flex; align-items: center; justify-content: center;
                    ">
                        <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                            stroke="#6b8cff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                            <polyline points="14 2 14 8 20 8"/>
                        </svg>
                    </div>
                    <div>
                        <div style="font-size: 0.9375rem; font-weight: 500; color: #1a1f36;">
                            {escape(note["title"])}
                        </div>
                        <div class="small text-muted mt-1">
                            Tag: <span class="text-black" style="font-weight:600">{escape(note["tag"])}</span>
                            Category: <span class="text-black" style="font-weight:600">{escape(note["category"])}</span>
                        </div>
                    </div>
                </div>

                <svg width="15" height="15" viewBox="0 0 24 24" fill="none"
                    stroke="#ccc" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polyline points="9 18 15 12 9 6"/>
                </svg>
            </a>

        </li>
""")

    items_html = "\n    ".join(items) if items else "<li class=muted>Notes not found</li>"

    filter_hint = f"""
        <p class="muted"> Filter example from query string:
        <a href="?tag=python><code>?tag=python</code></a>
        <a href="?category=django><code>?category=django</code></a>
        <a href="{escape(reverse("notes_list"))}>Reset filters</a?
        </p>
    """
    body = f"""
    <div class="container d-flex justify-content-center">
        <div class="w-100" style="max-width: 700px;">

            <div class="d-flex align-items-center justify-content-between mb-4">
                <div>
                    <h1 class="mb-1" style="font-size: 1.375rem; font-weight: 500; color: #1a1f36;">Notes</h1>
                    <p class="mb-0" style="font-size: 0.875rem; color: #aaa;">Browse your saved notes</p>
                </div>
                <a href="{escape(reverse('note_create'))}"
                    class="btn d-inline-flex align-items-center gap-2"
                    style="
                        background: #1a1f36; color: #fff; border: none;
                        padding: 8px 18px; border-radius: 9px;
                        font-size: 0.8125rem; font-weight: 500;
                        text-decoration: none;
                    "
                    onmouseover="this.style.background='#252b47'"
                    onmouseout="this.style.background='#1a1f36'">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none"
                        stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
                    </svg>
                        New note
                    </a>
            </div>

            <div class="card overflow-hidden"
                style="border: 1px solid rgba(0,0,0,0.07) !important;">
                <ul class="list-group list-group-flush notes">
                    {items_html}
                </ul>
            </div>

        </div>
    </div>
    """

    return HttpResponse(_html_shell("Notes list", body))


def note_detail(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(f"""
        <div class="d-flex justify-content-center align-items-center" style="min-height: 60vh;">

    <div class="card shadow-lg border-0 rounded-4 p-4 text-center" style="max-width: 500px;">

        <h1 class="fw-bold text-danger mb-3">⚠️ Note not found</h1>

        <p class="text-muted mb-2">
            ID: <code>{escape(str(note_id))}</code>
        </p>

        <p class="text-secondary">
            The requested note does not exist or was removed.
        </p>

        <a href="{escape(reverse('notes_list'))}" 
           class="btn btn-primary mt-3">
            ⬅ Return to Notes
        </a>

    </div>

</div>
""", status=404)
    edit_url = reverse('note_edit', kwargs={'note_id': note["id"]})
    delete_url = reverse('note_delete', kwargs={'note_id': note["id"]})
    list_url = escape(reverse("notes_list"))

    body = f"""
        <div class="container d-flex justify-content-center">
    <div class="w-100" style="max-width: 700px;">

        <div class="mb-4">
            <h1 class="mb-2" style="font-size: 1.75rem; font-weight: 600; color: #1a1f36;">
                {escape(note["title"])}
            </h1>
            <div class="d-flex align-items-center gap-2">
                <span style="font-size: 0.8125rem; color: #aaa;">ID: {note["id"]}</span>
                
                <span style="
                    font-weight: 600; padding: 2px 10px;
                ">
                    {escape(note["tag"])}
                </span>
                
                <span>-</span>
                
                <span style="
                    font-weight: 600; padding: 2px 10px;
                ">
                    {escape(note["category"])}
                </span>
            </div>
        </div>

        <div class="card mb-4" style="border: 1px solid rgba(0,0,0,0.07); border-radius: 12px; overflow: hidden;">
            <div class="card-body p-4">
                <div style="font-size: 1rem; color: #4f566b; line-height: 1.6; white-space: pre-wrap;">
                    {escape(note["body"])}
                </div>
            </div>
        </div>

        <div class="d-flex align-items-center justify-content-between flex-wrap gap-3">
            <div class="d-flex gap-2">
                <a href="{edit_url}" class="btn d-inline-flex align-items-center gap-2"
                   style="background: #fff; border: 1px solid #dcdfe4; color: #1a1f36; padding: 8px 16px; border-radius: 9px; font-size: 0.875rem; font-weight: 500;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                    Edit
                </a>

                <a href="{delete_url}" class="btn d-inline-flex align-items-center gap-2"
                   style="background: #fff; border: 1px solid #fee2e2; color: #ef4444; padding: 8px 16px; border-radius: 9px; font-size: 0.875rem; font-weight: 500;">
                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/></svg>
                    Delete
                </a>
            </div>

            <a href="{list_url}" class="btn d-inline-flex align-items-center gap-2"
               style="background: #1a1f36; color: #fff; border: none; padding: 8px 18px; border-radius: 9px; font-size: 0.875rem; font-weight: 500;">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12 19 5 12 12 5"/></svg>
                Back to Notes
            </a>
        </div>

    </div>
</div>
    """
    return HttpResponse(_html_shell(note["body"], body))


def note_create(request: HttpRequest) -> HttpResponse:
    title_val = ""
    body_val = ""
    tag_val = ""
    category_val = ""

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        title_val, body_val, tag_val, category_val = title, note_body, tag, category

        if not title.strip():
            err = "<p class='muted' style = 'color: #b00020;'>Title cannot be empty</p>"
        else:
            data.create_note(title=title, body=note_body, tag=tag or "misc", category=category or "general")
            return redirect("notes_list")
    else:
        err = ""

    form = f"""
    <div class="container d-flex justify-content-center py-5">
            <div class="w-100" style="max-width: 600px;">
            
                <div class="mb-4">
                    <h1 class="mb-1" style="font-size: 1.5rem; font-weight: 600; color: #1a1f36;">Create New Note</h1>
                    <p class="mb-0" style="font-size: 0.875rem; color: #aaa;">Fill in the details below to save a new note</p>
                </div>
            
                {err}
            
                <div class="card border-0" style="background: #fff; border: 1px solid rgba(0,0,0,0.07) !important; border-radius: 12px;">
                    <div class="card-body p-4">
                        <form method="post" action="{escape(reverse('note_create'))}">
                            {_csrf_field(request)}
            
                            <div class="mb-3">
                                <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Title</label>
                                <input 
                                    type="text" 
                                    name="title" 
                                    class="form-control shadow-none"
                                    style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem;"
                                    value="{escape(title_val)}" 
                                    placeholder="Enter note title..."
                                    required
                                >
                            </div>
            
                            <div class="mb-3">
                                <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Content</label>
                                <textarea 
                                    name="body" 
                                    class="form-control shadow-none" 
                                    rows="6"
                                    style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem;"
                                    placeholder="Write your thoughts here..."
                                >{escape(body_val)}</textarea>
                            </div>
            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Tag</label>
                                    <input 
                                        type="text" 
                                        name="tag" 
                                        class="form-control shadow-none"
                                        style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem;"
                                        value="{escape(tag_val)}" 
                                        placeholder="e.g. Python"
                                    >
                                </div>
            
                                <div class="col-md-6 mb-3">
                                    <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Category</label>
                                    <input 
                                        type="text" 
                                        name="category" 
                                        class="form-control shadow-none"
                                        style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem;"
                                        value="{escape(category_val)}" 
                                        placeholder="e.g. Backend"
                                    >
                                </div>
                            </div>
            
                            <div class="d-flex justify-content-between align-items-center mt-4">
                                <a href="{escape(reverse('notes_list'))}" 
                                   class="text-decoration-none" 
                                   style="font-size: 0.875rem; color: #6b7280; font-weight: 500;">
                                    Cancel
                                </a>
            
                                <button type="submit" class="btn d-inline-flex align-items-center gap-2"
                                    style="
                                        background: #1a1f36; color: #fff; border: none;
                                        padding: 10px 24px; border-radius: 9px;
                                        font-size: 0.875rem; font-weight: 500;
                                    "
                                    onmouseover="this.style.background='#252b47'"
                                    onmouseout="this.style.background='#1a1f36'">
                                    Save Note
                                </button>
                            </div>
            
                        </form>
                    </div>
                </div>

            </div>
        </div>
        """
    return HttpResponse(_html_shell("Create note", form))


def note_edit(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)
    if note is None:
        return HttpResponse(_html_shell("404 not found", f"""
    <h1>Can't edit</h1>
    <p class="muted">Note id: {escape(str(note_id))} nor found</p>
    <p><a href="{escape(reverse("notes_list"))}">Return to Nodes List</a></p>
"""), status=404)

    if request.method == "POST":
        title = request.POST.get("title", "")
        note_body = request.POST.get("body", "")
        tag = request.POST.get("tag", "")
        category = request.POST.get("category", "")

        if not title.strip():
            err = "<p class='muted' style = 'color: #b00020;'>Title cannot be empty</p>"

            note = {
                **note,
                "title": title,
                "body": note_body,
                "tag": tag,
                "category": category,
            }
        else:
            data.update_note(
                note_id,
                title=title,
                body=note_body,
                tag=tag or "misc",
                category=category or "general",
            )
            return redirect("note_detail", note_id=note_id)
    else:
        err = ""
        title_e = escape(note["title"])
        note_e = escape(note["body"])
        tag_e = escape(note["tag"])
        category_e = escape(note["category"])

        form = f"""
        <div class="container d-flex justify-content-center py-5">
            <div class="w-100" style="max-width: 600px;">
            
                <div class="mb-4 d-flex align-items-center gap-3">
                    <div style="background: #fff; padding: 10px; border-radius: 12px;">
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path>
                            <path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path>
                        </svg>
                    </div>
                    <div>
                        <h1 class="mb-0" style="font-size: 1.5rem; font-weight: 600; color: #1a1f36;">Edit Note</h1>
                        <p class="mb-0" style="font-size: 0.875rem; color: #aaa;">Update your note information</p>
                    </div>
                </div>
            
                <div class="card border-0" style="background: #fff; border: 1px solid rgba(0,0,0,0.07) !important; border-radius: 12px;">
                    <div class="card-body p-4">
                        <form method="post" action="{escape(reverse('note_edit', kwargs={'note_id': note_id}))}">
                            {_csrf_field(request)}
            
                            <div class="mb-3">
                                <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Title</label>
                                <input 
                                    type="text" 
                                    name="title" 
                                    class="form-control shadow-none"
                                    style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem;"
                                    value="{title_e}" 
                                    required
                                >
                            </div>
            
                            <div class="mb-3">
                                <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Content</label>
                                <textarea 
                                    name="body" 
                                    class="form-control shadow-none" 
                                    rows="8"
                                    style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem; line-height: 1.5;"
                                >{note_e}</textarea>
                            </div>
            
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Tag</label>
                                    <input 
                                        type="text" 
                                        name="tag" 
                                        class="form-control shadow-none"
                                        style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem;"
                                        value="{tag_e}" 
                                    >
                                </div>
            
                                <div class="col-md-6 mb-3">
                                    <label class="form-label" style="font-size: 0.8125rem; font-weight: 600; color: #4f566b; text-transform: uppercase; letter-spacing: 0.025em;">Category</label>
                                    <input 
                                        type="text" 
                                        name="category" 
                                        class="form-control shadow-none"
                                        style="border-radius: 8px; border: 1px solid #dcdfe4; padding: 10px 12px; font-size: 0.9375rem;"
                                        value="{category_e}" 
                                    >
                                </div>
                            </div>
            
                            <div class="d-flex justify-content-between align-items-center mt-4">
                                <a href="{escape(reverse('note_detail', kwargs={'note_id': note_id}))}" 
                                   class="text-decoration-none" 
                                   style="font-size: 0.875rem; color: #6b7280; font-weight: 500;">
                                    Cancel
                                </a>
            
                                <button type="submit" class="btn d-inline-flex align-items-center gap-2"
                                    style="
                                        background: #1a1f36; color: #fff; border: none;
                                        padding: 10px 24px; border-radius: 9px;
                                        font-size: 0.875rem; font-weight: 500;
                                        transition: background 0.2s;
                                    "
                                    onmouseover="this.style.background='#252b47'"
                                    onmouseout="this.style.background='#1a1f36'">
                                    <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
                                        <path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
                                        <polyline points="17 21 17 13 7 13 7 21"></polyline>
                                        <polyline points="7 3 7 8 15 8"></polyline>
                                    </svg>
                                    Save Changes
                                </button>
                            </div>
            
                        </form>
                    </div>
                </div>
            
            </div>
        </div>
        """
        return HttpResponse(_html_shell("Edit note", form))


def note_delete(request: HttpRequest, note_id: int) -> HttpResponse:
    note = data.get_note(note_id)

    if note is None:
        return HttpResponse(_html_shell("404 not found", f"""
        <h1>Can't delete</h1>
        <p>Note id: {escape(str(note_id))} not found</p>
        """), status=404)

    if request.method == "POST":
        data.delete_note(note_id)

        return redirect("notes_list")

    else:
        title = escape(note["title"])

        form = f"""
        <div class="container d-flex justify-content-center align-items-center" style="min-height: 70vh;">
            <div class="w-100 text-center" style="max-width: 450px;">
        
                <div class="mb-4 d-inline-flex align-items-center justify-content-center" 
                     style="width: 64px; height: 64px; background: #fff1f0; border-radius: 50%;">
                    <svg width="30" height="30" viewBox="0 0 24 24" fill="none" 
                         stroke="#ff4d4f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M3 6h18"></path>
                        <path d="M19 6v14c0 1-1 2-2 2H7c-1 0-2-1-2-2V6"></path>
                        <path d="M8 6V4c0-1 1-2 2-2h4c1 0 2 1 2 2v2"></path>
                        <line x1="10" y1="11" x2="10" y2="17"></line>
                        <line x1="14" y1="11" x2="14" y2="17"></line>
                    </svg>
                </div>
                
                <h1 class="mb-3" style="font-size: 1.5rem; font-weight: 600; color: #1a1f36;">Delete Note?</h1>
                
                <p class="mb-4" style="font-size: 0.9375rem; color: #6b7280; line-height: 1.5;">
                    Are you sure you want to delete <br>
                    <strong style="color: #1a1f36;">"{title}"</strong>? <br>
                    <span class="text-muted small">This action cannot be undone.</span>
                </p>

                <form method="post" action="{escape(reverse('note_delete', kwargs={'note_id': note_id}))}">
                    {_csrf_field(request)}
                    
                    <div class="d-flex flex-column gap-2">
                        <button type="submit" class="btn w-100" 
                            style="
                                background: #ff4d4f; color: #fff; border: none; 
                                padding: 12px; border-radius: 9px; font-weight: 500;
                                transition: background 0.2s;
                            "
                            onmouseover="this.style.background='#ff7875'"
                            onmouseout="this.style.background='#ff4d4f'">
                            Yes, delete note
                        </button>
                        
                        <a href="{escape(reverse('note_detail', kwargs={'note_id': note_id}))}" 
                            class="btn w-100" 
                            style="
                                background: transparent; color: #6b7280; border: none; 
                                padding: 10px; font-size: 0.875rem; font-weight: 500;
                            ">
                            Cancel
                        </a>
                    </div>
                </form>

            </div>
        </div>
        """

        return HttpResponse(_html_shell("Delete note", form))
