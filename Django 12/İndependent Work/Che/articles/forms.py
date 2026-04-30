from django import forms
from django.forms.models import ModelForm

from articles.models import Article, Category


class ArticleForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'category', 'image', 'content']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Заголовок',
                'class': 'text-[40px] w-full border rounded-lg px-3 py-2 border-none h-15 focus:outline-none',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border rounded-lg px-3 py-2 '
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'w-full'
            }),
        }

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-black',
                'placeholder': 'Например: Технологии'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'w-full border border-gray-300 rounded-lg p-2 focus:outline-none focus:ring-2 focus:ring-black',
                'placeholder': 'tech-news'
                }),
            }