from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', views.login_view, name='login'),      
    path('logout/', views.logout_view, name='logout'),  
    path('register/', views.register_view, name='register'),
    path('setup/', views.profile_setup, name='profile_setup'),
    path('profile/', views.profile_view, name='profile'),  
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
]
