from django.urls import path

from articles.views import create_category, create_article, article_list, article_detail, upload_image_editor

urlpatterns = [
    path('', article_list, name='articles'),
    path('article/add/', create_article, name='create_article'),
    path('category/add/', create_category, name='create_category'),
    path('article/<int:id>/', article_detail, name='article_detail'),
    path('article/upload-image/', upload_image_editor, name='upload_image_editor'),

]