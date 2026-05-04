from django import forms
from django.forms.models import ModelForm

from articles.models import Article, Category


class ArticleStepOneForm(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Заголовок',
                'class': 'text-[40px] font-bold w-full border rounded-lg px-3 py-2 border-none h-15 focus:outline-none',
            }),
        }

class ArticleStepTwoForm(ModelForm):
    class Meta:
        model = Article
        fields = ['category', 'image']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'text-gray-800 w-full border rounded-lg px-3 py-2'
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'text-gray-800 w-full'
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