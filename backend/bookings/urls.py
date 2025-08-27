from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    # API endpoints
    path('', views.BookingListAPIView.as_view(), name='api_list'),
    path('<int:pk>/', views.BookingDetailAPIView.as_view(), name='api_detail'),
    path('create/', views.BookingCreateAPIView.as_view(), name='api_create'),
    path('<int:pk>/cancel/', views.cancel_booking_api, name='api_cancel'),
    path('<int:pk>/confirm/', views.confirm_booking_api, name='api_confirm'),
    
    # Template views
    path('list/', views.booking_list, name='list'),
    path('detail/<int:pk>/', views.booking_detail, name='detail'),
    path('create/<int:travel_option_id>/', views.create_booking, name='create'),
    path('cancel/<int:pk>/', views.cancel_booking, name='cancel'),
]