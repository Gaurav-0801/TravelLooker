from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class TravelOption(models.Model):
    TRAVEL_TYPES = [
        ('FLIGHT', 'Flight'),
        ('TRAIN', 'Train'),
        ('BUS', 'Bus'),
    ]

    travel_id = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=10, choices=TRAVEL_TYPES)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_datetime = models.DateTimeField()
    arrival_datetime = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    total_seats = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    available_seats = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    operator_name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    amenities = models.JSONField(default=list, blank=True)  # List of amenities
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'travel_option'
        ordering = ['departure_datetime']
        indexes = [
            models.Index(fields=['type', 'source', 'destination']),
            models.Index(fields=['departure_datetime']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.travel_id} - {self.type} from {self.source} to {self.destination}"

    def clean(self):
        from django.core.exceptions import ValidationError
        
        if self.departure_datetime >= self.arrival_datetime:
            raise ValidationError('Departure time must be before arrival time.')
        
        if self.departure_datetime <= timezone.now():
            raise ValidationError('Departure time must be in the future.')
        
        if self.available_seats > self.total_seats:
            raise ValidationError('Available seats cannot exceed total seats.')

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def duration(self):
        """Returns travel duration as a timedelta object"""
        return self.arrival_datetime - self.departure_datetime

    @property
    def duration_hours(self):
        """Returns travel duration in hours"""
        return self.duration.total_seconds() / 3600

    @property
    def is_available(self):
        """Check if travel option is available for booking"""
        return (
            self.is_active and 
            self.available_seats > 0 and 
            self.departure_datetime > timezone.now()
        )

    def book_seats(self, num_seats):
        """Book specified number of seats"""
        if num_seats > self.available_seats:
            raise ValueError(f"Only {self.available_seats} seats available")
        
        self.available_seats -= num_seats
        self.save(update_fields=['available_seats'])
        return True

    def cancel_seats(self, num_seats):
        """Cancel specified number of seats"""
        if self.available_seats + num_seats > self.total_seats:
            raise ValueError("Cannot cancel more seats than total capacity")
        
        self.available_seats += num_seats
        self.save(update_fields=['available_seats'])
        return True