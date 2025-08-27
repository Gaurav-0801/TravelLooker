from rest_framework import generics, filters, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.db.models import Q
from .models import TravelOption
from .serializers import (
    TravelOptionSerializer, 
    TravelOptionSearchSerializer,
    TravelOptionCreateSerializer
)
from .filters import TravelOptionFilter

# API Views
class TravelOptionListAPIView(generics.ListAPIView):
    serializer_class = TravelOptionSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = TravelOptionFilter
    search_fields = ['source', 'destination', 'operator_name', 'type']
    ordering_fields = ['departure_datetime', 'price', 'duration_hours']
    ordering = ['departure_datetime']

    def get_queryset(self):
        return TravelOption.objects.filter(
            is_active=True,
            departure_datetime__gt=timezone.now()
        )


class TravelOptionDetailAPIView(generics.RetrieveAPIView):
    queryset = TravelOption.objects.filter(is_active=True)
    serializer_class = TravelOptionSerializer
    permission_classes = [permissions.AllowAny]


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def search_travel_options(request):
    """Advanced search endpoint for travel options"""
    serializer = TravelOptionSearchSerializer(data=request.data)
    if serializer.is_valid():
        filters = Q(is_active=True, departure_datetime__gt=timezone.now())

        if serializer.validated_data.get('source'):
            filters &= Q(source__icontains=serializer.validated_data['source'])
        if serializer.validated_data.get('destination'):
            filters &= Q(destination__icontains=serializer.validated_data['destination'])
        if serializer.validated_data.get('type'):
            filters &= Q(type=serializer.validated_data['type'])
        if serializer.validated_data.get('departure_date'):
            date = serializer.validated_data['departure_date']
            filters &= Q(departure_datetime__date=date)
        if serializer.validated_data.get('min_price'):
            filters &= Q(price__gte=serializer.validated_data['min_price'])
        if serializer.validated_data.get('max_price'):
            filters &= Q(price__lte=serializer.validated_data['max_price'])
        if serializer.validated_data.get('available_seats_min'):
            filters &= Q(available_seats__gte=serializer.validated_data['available_seats_min'])

        travel_options = TravelOption.objects.filter(filters).order_by('departure_datetime')
        result_serializer = TravelOptionSerializer(travel_options, many=True)
        return Response({'count': travel_options.count(), 'results': result_serializer.data})

    return Response(serializer.errors, status=400)


# Template Views
def travel_options_list(request):
    """Template view for listing travel options"""
    travel_options = TravelOption.objects.filter(
        is_active=True,
        departure_datetime__gt=timezone.now()
    ).order_by('departure_datetime')

    source = request.GET.get('source')
    destination = request.GET.get('destination')
    travel_type = request.GET.get('type')
    departure_date = request.GET.get('departure_date')

    if source:
        travel_options = travel_options.filter(source__icontains=source)
    if destination:
        travel_options = travel_options.filter(destination__icontains=destination)
    if travel_type:
        travel_options = travel_options.filter(type=travel_type)
    if departure_date:
        travel_options = travel_options.filter(departure_datetime__date=departure_date)

    context = {
        'travel_options': travel_options,
        'travel_types': TravelOption.TRAVEL_TYPES,
        'search_params': {
            'source': source or '',
            'destination': destination or '',
            'type': travel_type or '',
            'departure_date': departure_date or '',
        }
    }
    return render(request, 'travel_options/list.html', context)


def travel_option_detail(request, pk):
    """Template view for travel option details"""
    travel_option = get_object_or_404(TravelOption, pk=pk, is_active=True)
    context = {'travel_option': travel_option}
    return render(request, 'travel_options/detail.html', context)


def home_view(request):
    """Home page with search form"""
    featured_options = TravelOption.objects.filter(
        is_active=True,
        departure_datetime__gt=timezone.now()
    ).order_by('departure_datetime')[:6]

    context = {
        'featured_options': featured_options,
        'travel_types': TravelOption.TRAVEL_TYPES,
    }
    return render(request, 'travel_options/home.html', context)
