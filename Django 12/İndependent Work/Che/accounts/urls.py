import profile

from django.urls import path

from accounts.forms import CustomAuthenticationForm
from accounts.views import register, profile_edit, profile_view, admin_panel, ban_user, change_role, notifications, \
    clear_notifications
from django.contrib.auth import views as auth_views

app_name = 'accounts'

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', form_class=CustomAuthenticationForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/<str:username>/', profile_view, name='profile_view'),
    path('admin/', admin_panel, name='admin_panel'),
    path('admin/ban/<int:pk>/', ban_user, name='ban_user'),
    path('admin/role/<int:pk>/', change_role, name='change_role'),
    path('notifications/', notifications, name='notifications'),
    path('notifications/clear/', clear_notifications, name='clear_notifications'),
]