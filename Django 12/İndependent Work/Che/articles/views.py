import cloudinary.uploader
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from accounts.models import Notification
from articles.forms import CategoryForm, ArticleStepOneForm, ArticleStepTwoForm
from articles.models import Article, Category, Bookmark


@csrf_exempt
@login_required
def upload_image_editor(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']

        try:
            # Загрузка картинки на cloudinary
            upload_result = cloudinary.uploader.upload(image_file)

            # Ссылка на загруженную картинку
            image_url = upload_result.get('secure_url')

            return JsonResponse({
                'success': 1,
                'file': {
                    'url': image_url,
                }
            })

        except Exception as e:
            return JsonResponse({
                'success': 0,
                'message': str(e)
            })

    return JsonResponse({'success': 0, 'message': 'Некорректный запрос'})


@login_required
def create_article_step1(request):
    if request.method == 'POST':
        form = ArticleStepOneForm(request.POST)

        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.status = Article.Status.DRAFT

            # Временно чтобы была возможность перейти на второй этап
            article.category = Category.objects.first()
            article.save()

            return redirect('create_article_step2', pk = article.pk)

    else:
        form = ArticleStepOneForm()

    return render(request, 'articles/create_article_step1.html', {'form': form})


@login_required
def create_article_step2(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)

    if article.status not in (Article.Status.DRAFT, Article.Status.PENDING):
        return redirect('article_detail', id=article.pk)

    if request.method == 'POST':
        form = ArticleStepTwoForm(request.POST, request.FILES, instance=article)

        if form.is_valid():
            article = form.save(commit=False)

            # Admin публикует сразу, user отправляет на модерацию
            if request.user.is_admin:
                article.status = Article.Status.PUBLISHED
            else:
                article.status = Article.Status.PENDING

                Notification.objects.create(
                    user=request.user,
                    type=Notification.Type.ARTICLE_PENDING,
                    article_title=article.title,
                    article_id=article.pk,
                )
            article.save()

            return redirect('article_detail', id=article.pk)

    else:
        form = ArticleStepTwoForm(instance=article)

    return render(request, 'articles/create_article_step2.html', {'form': form, 'article': article})


@login_required
def create_article_step1_edit(request, pk):
    article = get_object_or_404(Article, pk=pk, author=request.user)

    if article.status != Article.Status.DRAFT:
        return redirect('article_detail', id=pk)

    if request.method == 'POST':
        form = ArticleStepOneForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('create_article_step2', pk=article.pk)
    else:
        form = ArticleStepOneForm(instance=article)

    return render(request, 'articles/create_article_step1.html', {'form': form, 'article': article,})

@login_required
def create_category(request):
    if not request.user.is_admin:
        return redirect('articles')

    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = CategoryForm()

    return render(request, 'articles/create_category.html', {'form': form})

@login_required
def edit_category(request, pk):
    if not request.user.is_admin:
        return redirect('articles')

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()

        if name:
            category.name = name
            category.save()
            return redirect('accounts:admin_panel')

    return render(request, 'articles/edit_category.html', {'category': category})

@login_required
def delete_category(request, pk):
    if not request.user.is_admin:
        return redirect('articles')

    category = get_object_or_404(Category, pk=pk)

    if request.method == 'POST':
        if category.articles.filter(is_published=True).count() == 0:
            category.delete()
        return redirect('accounts:admin_panel')

    return render(request, 'articles/delete_category.html', {})


def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    articles = Article.objects.filter(category=category, status=Article.Status.PUBLISHED).order_by('-created_at')
    return render(request, 'articles/category_detail.html', {
        'category': category,
        'articles': articles,
    })

@login_required
def category_list_admin(request):
    if not request.user.is_admin:
        return redirect('articles')

    categories = Category.objects.all().order_by('name')

    for category in categories:
        category.published_count = category.articles.filter(status=Article.Status.PUBLISHED).count()
        
    return render(request, 'articles/category_list_admin.html', {'categories': categories})

def article_list(request):
    articles = Article.objects.all().filter(status=Article.Status.PUBLISHED).order_by('-created_at')

    bookmarked_ids = set()
    if request.user.is_authenticated:
        bookmarked_ids = set(
            Bookmark.objects.filter(user=request.user).values_list('article_id', flat=True)
        )

    return render(request, 'articles/list.html', {'articles': articles, 'bookmarked_ids': bookmarked_ids})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)

    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, article=article).exists()

    return render(request, 'articles/detail.html', {'article': article, 'is_bookmarked': is_bookmarked})

@login_required
def toggle_bookmark(request, article_id):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    article = get_object_or_404(Article, pk=article_id)
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, article=article)

    if not created:
        bookmark.delete()
        return JsonResponse({'bookmarked': False})

    return JsonResponse({'bookmarked': True})

@login_required
def edit_article_step1(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if not (request.user == article.author or request.user.is_admin):
        return redirect('article_detail', id=pk)

    if request.method == 'POST':
        form = ArticleStepOneForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('edit_article_step2', pk=pk)
    else:
        form = ArticleStepOneForm(instance=article)

    return render(request, 'articles/edit_article_step1.html', {
        'form': form,
        'article': article,
    })

@login_required
def edit_article_step2(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if not (request.user == article.author or request.user.is_admin):
        return redirect('article_detail', id=pk)

    if request.method == 'POST':
        form = ArticleStepTwoForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            article = form.save(commit=False)

            # После редактирования user-ом снова на модерацию
            if not request.user.is_admin:
                article.status = Article.Status.PENDING
            article.save()

            return redirect('article_detail', id=pk)
    else:
        form = ArticleStepTwoForm(instance=article)

    return render(request, 'articles/edit_article_step2.html', {'form': form, 'article': article})

@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if not (request.user == article.author or request.user.is_admin):
        return redirect('article_detail', id=pk)

    if request.method == 'POST':
        article.delete()

        return redirect('articles')

    return render(request, 'articles/delete_article.html', {'article': article})

@login_required
def approve_article(request, pk):
    if not request.user.is_admin:
        return redirect('articles')

    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'approve':
            article.status = Article.Status.PUBLISHED
            Notification.objects.create(
                user=article.author,
                type=Notification.Type.ARTICLE_APPROVED,
                article_title=article.title,
                article_id=article.pk,
            )
        elif action == 'reject':
            article.status = Article.Status.DRAFT
            Notification.objects.create(
                user=article.author,
                type=Notification.Type.ARTICLE_REJECTED,
                article_title=article.title,
                article_id=article.pk,
            )
        article.save()

    return redirect('accounts:admin_panel')