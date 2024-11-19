from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', views.register_view, name='register'),  
    path('profile/', views.profile_view, name='profile'),  
    path('profile/edit/', views.edit_profile_view, name='edit_profile'), 
    path('password/change/', views.change_password_view, name='change_password'), 
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
]
