from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # API endpoints
    path('register/', views..as_view(), name='api_register'),
    path('login/', views.LoginAPIView.as_view(), name='api_login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api_logout'),
    path('profile/', views.ProfileAPIView.as_view(), name='api_profile'),
    
    # Template views
    path('register-form/', views.RegisterView.as_view(), name='register'),
    path('profile-view/', views.profile_view, name='profile'),
    path('profile-update/', views.ProfileUpdateView.as_view(), name='profile_update'),
]