from django.contrib.auth.decorators import login_required

from accounts.forms import CustomUserCreationForm, ProfileEditForm
from django.contrib.auth import login
from django.shortcuts import redirect, render, get_object_or_404

import cloudinary.uploader

from accounts.models import CustomUser, Notification
from articles.models import Article, Bookmark, Category


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_edit(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            profile = form.save(commit=False)

            avatar_file = request.FILES.get('avatar')
            if avatar_file:
                upload_result = cloudinary.uploader.upload(
                    avatar_file,
                    folder='avatars',
                    transformation=[
                        {'width': 400, 'height': 400, 'crop': 'fill', 'gravity': 'face'}
                    ]

                )
                profile.avatar = upload_result['public_id']

            profile.save()
            return redirect('accounts:profile_edit')

    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'accounts/profile_edit.html', {'form': form})

def profile_view(request, username):
    profile_user = get_object_or_404(CustomUser, username=username)

    articles = Article.objects.filter(author=profile_user, status=Article.Status.PUBLISHED).order_by('-created_at')

    bookmarks = []
    if request.user == profile_user:
        bookmarks = Bookmark.objects.filter(user=profile_user).select_related('article').order_by('-created_at')

    return render(request, 'accounts/profile.html', {'profile_user': profile_user, 'articles': articles, 'bookmarks': bookmarks})

# ======================= Admin =======================
@login_required
def admin_panel(request):
    if not request.user.is_admin:
        return redirect('articles')

    users = CustomUser.objects.exclude(pk=request.user.pk).order_by('username')
    articles = Article.objects.all().order_by('-created_at')
    category = Category.objects.all().order_by('name')
    pending = Article.objects.filter(status=Article.Status.PENDING).order_by('-created_at')

    return render(request, 'accounts/admin_panel.html', {'users': users, 'articles': articles, 'category': category, 'pending': pending})

@login_required
def ban_user(request, pk):
    if not request.user.is_admin:
        return redirect('articles')

    target = get_object_or_404(CustomUser, pk=pk)

    # Admin не может банить Superadmin-а
    if target.is_superuser and not request.user.is_superuser:
        return redirect('accounts:admin_panel')

    # Admin не может банить Admin-а
    if target.is_staff and not request.user.is_superuser:
        return redirect('accounts:admin_panel')

    if request.method == 'POST':
        target.is_banned = not target.is_banned
        target.save()

    return redirect('accounts:admin_panel')

@login_required
def change_role(request, pk):
    if not request.user.is_superuser:
        return redirect('articles')

    target = get_object_or_404(CustomUser, pk=pk)

    if request.method == 'POST':
        new_role = request.POST.get('role')
        if new_role == 'admin':
            target.is_staff = True
        elif new_role == 'user':
            target.is_staff = False
        target.save()

    return redirect('accounts:admin_panel')

@login_required
def notifications(request):
    notifs = Notification.objects.filter(user=request.user)

    notifs.filter(is_read=False).update(is_read=True)

    return render(request, 'accounts/notifications.html', {'notifications': notifs})

@login_required
def clear_notifications(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user).delete()
    return redirect('accounts:notifications')
