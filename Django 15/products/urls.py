from django.urls import path
from products import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('product/<int:product_id>/add-review/', views.add_review, name='add_review'),
    path('product/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('product/<int:pk>/delete/', views.delete_review, name='delete_review'),
]