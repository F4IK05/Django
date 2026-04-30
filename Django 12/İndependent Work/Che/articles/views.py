import cloudinary.uploader
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from articles.forms import ArticleForm, CategoryForm
from articles.models import Article


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
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            article = form.save(commit=False)

            article.author = request.user

            article.save()

            return redirect('/')

    else:
        form = ArticleForm()

    return render(request, 'articles/create_article.html', {'form': form})

@login_required
def create_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = CategoryForm()

    return render(request, 'articles/create_category.html', {'form': form})

def article_list(request):
    articles = Article.objects.all().order_by('-created_at')

    return render(request, 'articles/list.html', {'articles': articles})

def article_detail(request, id):
    article = get_object_or_404(Article, id=id)
    return render(request, 'articles/detail.html', {'article': article})