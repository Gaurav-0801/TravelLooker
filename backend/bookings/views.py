from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Booking
from .serializers import BookingSerializer, BookingCreateSerializer, BookingCancelSerializer
from .forms import BookingForm
from travel_options.models import TravelOption

# ---------------- API VIEWS ----------------

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
        serializer.save(user=self.request.user)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def cancel_booking_api(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    serializer = BookingCancelSerializer(data=request.data)

    if serializer.is_valid():
        reason = serializer.validated_data.get('reason', '')
        booking.cancel_booking(reason)
        return Response({'message': 'Booking cancelled', 'booking': BookingSerializer(booking).data})
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def confirm_booking_api(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if booking.status != 'PENDING':
        return Response({'error': 'Only pending bookings can be confirmed'}, status=status.HTTP_400_BAD_REQUEST)
    
    booking.confirm_booking()
    return Response({'message': 'Booking confirmed', 'booking': BookingSerializer(booking).data})


# ---------------- TEMPLATE VIEWS ----------------

@login_required
def booking_list(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-booking_date')
    status_filter = request.GET.get('status')
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    return render(request, 'bookings/list.html', {'bookings': bookings, 'status_choices': Booking.STATUS_CHOICES, 'current_status': status_filter})

@login_required
def booking_detail(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    return render(request, 'bookings/detail.html', {'booking': booking})

@login_required
def create_booking(request, travel_option_id):
    travel_option = get_object_or_404(TravelOption, pk=travel_option_id, is_active=True)
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
            booking.save()
            booking.confirm_booking()
            messages.success(request, f'Booking {booking.booking_id} created successfully!')
            return redirect('bookings:detail', pk=booking.pk)
    else:
        form = BookingForm(initial={'contact_email': request.user.email, 'contact_phone': getattr(request.user, 'phone_number', '')})

    return render(request, 'bookings/create.html', {'form': form, 'travel_option': travel_option})

@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, user=request.user)
    if not booking.can_be_cancelled:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', pk=pk)

    if request.method == 'POST':
        reason = request.POST.get('reason', '')
        booking.cancel_booking(reason)
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('bookings:detail', pk=booking.pk)

    return render(request, 'bookings/cancel.html', {'booking': booking})
