from django.urls import path

from articles.views import create_category, article_list, article_detail, upload_image_editor, \
    create_article_step1, create_article_step2, create_article_step1_edit, toggle_bookmark, \
    delete_article, edit_article_step1, edit_article_step2, edit_category, delete_category, category_detail, \
    category_list_admin, approve_article

urlpatterns = [
    path('', article_list, name='articles'),
    path('article/add/', create_article_step1, name='create_article_step1'),
    path('article/add/<int:pk>/settings/', create_article_step2, name='create_article_step2'),
    path('article/add/<int:pk>/edit/', create_article_step1_edit, name='create_article_step1_edit'),
    path('admin/category/add/', create_category, name='create_category'),
    path('category/<int:pk>/edit/', edit_category, name='edit_category'),
    path('category/<int:pk>/delete/', delete_category, name='delete_category'),
    path('category/<int:pk>/', category_detail, name='category_detail'),
    path('category/list/', category_list_admin, name='category_list_admin'),
    path('article/<int:id>/', article_detail, name='article_detail'),
    path('article/upload-image/', upload_image_editor, name='upload_image_editor'),
    path('article/<int:article_id>/bookmark/', toggle_bookmark, name='toggle_bookmark'),
    path('article/<int:pk>/edit/', edit_article_step1, name='edit_article_step1'),
    path('article/<int:pk>/edit/settings/', edit_article_step2, name='edit_article_step2'),
    path('article/<int:pk>/delete/', delete_article, name='delete_article'),
    path('article/<int:pk>/approve/', approve_article, name='approve_article'),
]