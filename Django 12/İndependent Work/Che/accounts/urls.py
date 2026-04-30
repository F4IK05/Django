from django.urls import path

from accounts.forms import CustomAuthenticationForm
from accounts.views import register
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', form_class=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]