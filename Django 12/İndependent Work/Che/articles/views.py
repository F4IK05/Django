from django.shortcuts import render, redirect, get_object_or_404

from articles.forms import ArticleForm, CategoryForm
from articles.models import Article

def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('/')

    else:
        form = ArticleForm()

    return render(request, 'articles/create_article.html', {'form': form})

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