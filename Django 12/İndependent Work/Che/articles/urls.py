from django.urls import path

from articles.views import create_category, create_article, article_list, article_detail

urlpatterns = [
    path('', article_list, name='articles'),
    path('article/add/', create_article, name='create_article'),
    path('category/add/', create_category, name='create_category'),
    path('<int:id>/', article_detail, name='article_detail'),

]