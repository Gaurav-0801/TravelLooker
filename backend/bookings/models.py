from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
        ('REFUNDED', 'Refunded'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    travel_option = models.ForeignKey('travel_options.TravelOption', on_delete=models.CASCADE, related_name='bookings')
    number_of_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    passenger_details = models.JSONField(default=list)  # List of passenger information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    special_requests = models.TextField(blank=True)
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)

    class Meta:
        db_table = 'booking'
        ordering = ['-booking_date']
        indexes = [
            models.Index(fields=['user', 'status']),
            models.Index(fields=['booking_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"Booking {self.booking_id} - {self.user.username}"

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = self.generate_booking_id()
        
        # Calculate total price if not set
        if not self.total_price:
            self.total_price = self.travel_option.price * self.number_of_seats
        
        super().save(*args, **kwargs)

    def generate_booking_id(self):
        """Generate unique booking ID"""
        prefix = 'BK'
        timestamp = timezone.now().strftime('%Y%m%d')
        random_suffix = str(uuid.uuid4())[:6].upper()
        return f"{prefix}{timestamp}{random_suffix}"

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.travel_option and self.number_of_seats > self.travel_option.available_seats:
            raise ValidationError(f'Only {self.travel_option.available_seats} seats available')
        
        if self.travel_option and self.travel_option.departure_datetime <= timezone.now():
            raise ValidationError('Cannot book past travel options')

    def confirm_booking(self):
        """Confirm the booking and update seat availability"""
        if self.status != 'PENDING':
            raise ValueError('Only pending bookings can be confirmed')
        
        # Check seat availability
        if self.number_of_seats > self.travel_option.available_seats:
            raise ValueError('Not enough seats available')
        
        # Update travel option seats
        self.travel_option.book_seats(self.number_of_seats)
        
        # Update booking status
        self.status = 'CONFIRMED'
        self.save(update_fields=['status'])
        
        return True

    def cancel_booking(self, reason=''):
        """Cancel the booking and restore seat availability"""
        if self.status not in ['PENDING', 'CONFIRMED']:
            raise ValueError('Only pending or confirmed bookings can be cancelled')
        
        # Restore seats if booking was confirmed
        if self.status == 'CONFIRMED':
            self.travel_option.cancel_seats(self.number_of_seats)
        
        # Update booking status
        self.status = 'CANCELLED'
        self.cancelled_at = timezone.now()
        self.cancellation_reason = reason
        self.save(update_fields=['status', 'cancelled_at', 'cancellation_reason'])
        
        return True

    @property
    def can_be_cancelled(self):
        """Check if booking can be cancelled"""
        if self.status not in ['PENDING', 'CONFIRMED']:
            return False
        
        # Can't cancel if travel date is too close (e.g., less than 24 hours)
        time_until_departure = self.travel_option.departure_datetime - timezone.now()
        return time_until_departure.total_seconds() > 24 * 3600  # 24 hours

    @property
    def is_upcoming(self):
        """Check if the travel date is in the future"""
        return self.travel_option.departure_datetime > timezone.now()

    @property
    def days_until_travel(self):
        """Get number of days until travel"""
        if not self.is_upcoming:
            return 0
        
        time_diff = self.travel_option.departure_datetime - timezone.now()
        return time_diff.days


class PassengerDetail(models.Model):
    """Separate model for passenger details if needed for complex scenarios"""
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='passengers')
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')])
    id_number = models.CharField(max_length=50, blank=True)  # Passport/ID number
    seat_preference = models.CharField(max_length=20, blank=True)

    class Meta:
        db_table = 'passenger_detail'

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.booking.booking_id}"