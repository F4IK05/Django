from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms.models import ModelForm

from accounts.models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email')
        labels = {
            'username': 'Имя пользователя (Логин)',
            'email': 'Электронная почта',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email обязателен")
        return email

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password1'].label = 'Придумайте пароль'
        self.fields['password2'].label = 'Подтвердите пароль'

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-black w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent mt-1 transition-all',
            })

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['username'].label = 'Логин (Имя пользователя)'
        self.fields['password'].label = 'Пароль'

        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'text-black w-full border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-black focus:border-transparent mt-1 transition-all',
            })

class ProfileEditForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'bio', 'avatar']
        labels = {
            'username': 'Имя пользователя',
            'bio': 'О себе',
            'avatar': 'Аватар',
        }

        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full text-gray-800 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-black transition-all',
            }),
            'bio': forms.Textarea(attrs={
                'class': 'w-full text-gray-800 border border-gray-300 rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-black transition-all resize-none',
                'rows': 4,
                'placeholder': 'Расскажите о себе...',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'hidden',
                'accept': 'image/*',
                'id': 'avatar-input',
            }),
        }