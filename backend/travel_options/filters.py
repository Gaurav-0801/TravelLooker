import django_filters
from django.utils import timezone
from .models import TravelOption

class TravelOptionFilter(django_filters.FilterSet):
    source = django_filters.CharFilter(lookup_expr='icontains')
    destination = django_filters.CharFilter(lookup_expr='icontains')
    departure_date = django_filters.DateFilter(field_name='departure_datetime', lookup_expr='date')
    departure_date_from = django_filters.DateFilter(field_name='departure_datetime', lookup_expr='date__gte')
    departure_date_to = django_filters.DateFilter(field_name='departure_datetime', lookup_expr='date__lte')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    available_seats_min = django_filters.NumberFilter(field_name='available_seats', lookup_expr='gte')
    
    class Meta:
        model = TravelOption
        fields = {
            'type': ['exact'],
            'operator_name': ['icontains'],
        }