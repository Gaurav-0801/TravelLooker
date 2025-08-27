from django.urls import path
from . import views

app_name = 'travel_options'

urlpatterns = [
    # API endpoints
    path('', views.TravelOptionListAPIView.as_view(), name='api_list'),
    path('<int:pk>/', views.TravelOptionDetailAPIView.as_view(), name='api_detail'),
    path('search/', views.search_travel_options, name='api_search'),
    
    # Template views
    path('list/', views.travel_options_list, name='list'),
    path('detail/<int:pk>/', views.travel_option_detail, name='detail'),
    path('home/', views.home_view, name='home'),
]