import json

from cloudinary.models import CloudinaryField
from django.conf import settings
from django.db import models
from django.utils.html import strip_tags
from django_editorjs import EditorJsField

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Черновик'
        PENDING = 'pending', 'На модерации'
        PUBLISHED = 'published', 'Опубликована'

    title = models.CharField(max_length=100)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    image = CloudinaryField('image', blank=True, null=True)

    content = EditorJsField(
        editorjs_config={
            'tools': {
                'Image': {
                    'config': {
                        'endpoints': {
                            'byFile': '/article/upload-image/',
                        }
                    }
                },
            }
        }
    )

    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )

    def mini_content(self):
        if not self.content:
            return ''

        try:
            data = json.loads(self.content)
            blocks = data.get('blocks', [])

            preview_html = ""
            block_count = 0

            for block in blocks:
                block_type = block.get('type', '').lower()

                if block_type == 'delimiter':
                    break

                # Если забыл поставить разделитель
                if block_count >= 3:
                    break

                if block_type == 'paragraph':
                    text = block['data'].get('text', '')
                    preview_html += f'<p class="text-gray-700 mb-3 leading-relaxed">{text}</p>'

                elif block_type == 'header':
                    text = block['data'].get('text', '')
                    preview_html += f'<h3 class="text-lg font-bold text-black mt-4 mb-2">{text}</h3>'

                block_count += 1

            return preview_html

        except (json.JSONDecodeError, TypeError):
            clean_fallback = strip_tags(str(self.content))
            return f'<p class="text-gray-700 mb-3">{clean_fallback[:150]}...</p>'

    def __str__(self):
        return self.title

class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Чтобы к одной и той же статье нельзя было создавать более одной закладки
    class Meta:
        unique_together = ('user', 'article')

    def __str__(self):
        return f'{self.user} {self.article}'