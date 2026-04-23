from django.forms import ModelForm

from products.models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating']