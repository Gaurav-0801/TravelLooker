from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Booking
from .serializers import (
    BookingSerializer, 
    BookingCreateSerializer, 
    BookingCancelSerializer
)
from .forms import BookingForm

# API Views
class BookingListAPIView(generics.ListAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingDetailAPIView(generics.RetrieveAPIView):
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

class BookingCreateAPIView(generics.CreateAPIView):
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        booking = serializer.save()
        # Auto-confirm booking (in real app, you might want payment integration)
        booking.confirm_booking()

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking_api(request, pk):
    """Cancel a booking via API"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    serializer = BookingCancelSerializer(
        data=request.data, 
        context={'booking': booking}
    )
    
    if serializer.is_valid():
        reason = serializer.validated_data.get('reason', '')
        booking.cancel_booking(reason)
        
        return Response({
            'message': 'Booking cancelled successfully',
            'booking': BookingSerializer(booking).data
        })
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_booking_api(request, pk):
    """Confirm a pending booking"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if booking.status != 'PENDING':
        return Response(
            {'error': 'Only pending bookings can be confirmed'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        booking.confirm_booking()
        return Response({
            'message': 'Booking confirmed successfully',
            'booking': BookingSerializer(booking).data
        })
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Template Views
@login_required
def booking_list(request):
    """Template view for user's bookings"""
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    
    # Filter by status if requested
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    context = {
        'bookings': bookings,
        'status_choices': Booking.STATUS_CHOICES,
        'current_status': status_filter
    }
    return render(request, 'bookings/list.html', context)

@login_required
def booking_detail(request, pk):
    """Template view for booking details"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    context = {'booking': booking}
    return render(request, 'bookings/detail.html', context)

@login_required
def create_booking(request, travel_option_id):
    """Template view for creating a booking"""
    from travel_options.models import TravelOption
    
    travel_option = get_object_or_404(
        TravelOption, 
        pk=travel_option_id, 
        is_active=True
    )
    
    if not travel_option.is_available:
        messages.error(request, 'This travel option is no longer available.')
        return redirect('travel_options:detail', pk=travel_option_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.travel_option = travel_option
            booking.total_price = travel_option.price * booking.number_of_seats
            
            try:
                booking.save()
                booking.confirm_booking()
                messages.success(request, f'Booking {booking.booking_id} created successfully!')
                return redirect('bookings:detail', pk=booking.pk)
            except Exception as e:
                messages.error(request, f'Error creating booking: {str(e)}')
    else:
        form = BookingForm(initial={
            'contact_email': request.user.email,
            'contact_phone': getattr(request.user, 'phone_number', '')
        })
    
    context = {
        'form': form,
        'travel_option': travel_option
    }
    return render(request, 'bookings/create.html', context)

@login_required
def cancel_booking(request, pk):
    """Template view for cancelling a booking"""
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    
    if not booking.can_be_cancelled:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        try:
            booking.cancel_booking(reason)
            messages.success(request, 'Booking cancelled successfully.')
        except Exception as e:
            messages.error(request, f'Error cancelling booking: {str(e)}')
        
        return redirect('bookings:detail', pk=pk)
    
    context = {'booking': booking}
    return render(request, 'bookings/cancel.html', context)