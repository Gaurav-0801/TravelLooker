from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta
from decimal import Decimal

from travel_options.models import TravelOption
from bookings.models import Booking

User = get_user_model()

class TravelOptionModelTest(TestCase):
    def setUp(self):
        self.future_date = timezone.now() + timedelta(days=7)
        self.arrival_date = self.future_date + timedelta(hours=2)
        
    def test_create_travel_option(self):
        travel_option = TravelOption.objects.create(
            travel_id='FL001',
            type='FLIGHT',
            source='New York',
            destination='Los Angeles',
            departure_datetime=self.future_date,
            arrival_datetime=self.arrival_date,
            price=Decimal('299.99'),
            total_seats=100,
            available_seats=100,
            operator_name='Test Airlines'
        )
        
        self.assertEqual(travel_option.travel_id, 'FL001')
        self.assertTrue(travel_option.is_available)
        self.assertAlmostEqual(travel_option.duration_hours, 2.0, places=1)

    def test_invalid_departure_time(self):
        with self.assertRaises(ValidationError):
            travel_option = TravelOption(
                travel_id='FL002',
                type='FLIGHT',
                source='New York',
                destination='Los Angeles',
                departure_datetime=self.arrival_date,  # After arrival
                arrival_datetime=self.future_date,
                price=Decimal('299.99'),
                total_seats=100,
                available_seats=100,
                operator_name='Test Airlines'
            )
            travel_option.full_clean()

    def test_book_seats(self):
        travel_option = TravelOption.objects.create(
            travel_id='FL003',
            type='FLIGHT',
            source='New York',
            destination='Los Angeles',
            departure_datetime=self.future_date,
            arrival_datetime=self.arrival_date,
            price=Decimal('299.99'),
            total_seats=100,
            available_seats=100,
            operator_name='Test Airlines'
        )
        
        initial_seats = travel_option.available_seats
        travel_option.book_seats(5)
        travel_option.refresh_from_db()
        
        self.assertEqual(travel_option.available_seats, initial_seats - 5)

    def test_book_more_seats_than_available(self):
        travel_option = TravelOption.objects.create(
            travel_id='FL004',
            type='FLIGHT',
            source='New York',
            destination='Los Angeles',
            departure_datetime=self.future_date,
            arrival_datetime=self.arrival_date,
            price=Decimal('299.99'),
            total_seats=5,
            available_seats=5,
            operator_name='Test Airlines'
        )
        
        with self.assertRaises(ValueError):
            travel_option.book_seats(10)

class BookingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.future_date = timezone.now() + timedelta(days=7)
        self.arrival_date = self.future_date + timedelta(hours=2)
        
        self.travel_option = TravelOption.objects.create(
            travel_id='FL005',
            type='FLIGHT',
            source='New York',
            destination='Los Angeles',
            departure_datetime=self.future_date,
            arrival_datetime=self.arrival_date,
            price=Decimal('299.99'),
            total_seats=100,
            available_seats=100,
            operator_name='Test Airlines'
        )

    def test_create_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            contact_email='test@example.com',
            contact_phone='1234567890'
        )
        
        self.assertTrue(booking.booking_id.startswith('BK'))
        self.assertEqual(booking.total_price, Decimal('599.98'))  # 2 * 299.99
        self.assertEqual(booking.status, 'PENDING')

    def test_confirm_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            contact_email='test@example.com',
            contact_phone='1234567890'
        )
        
        initial_seats = self.travel_option.available_seats
        booking.confirm_booking()
        
        self.travel_option.refresh_from_db()
        self.assertEqual(booking.status, 'CONFIRMED')
        self.assertEqual(self.travel_option.available_seats, initial_seats - 2)

    def test_cancel_booking(self):
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            contact_email='test@example.com',
            contact_phone='1234567890'
        )
        
        booking.confirm_booking()
        initial_seats = self.travel_option.available_seats
        
        booking.cancel_booking('Changed plans')
        
        self.travel_option.refresh_from_db()
        self.assertEqual(booking.status, 'CANCELLED')
        self.assertEqual(self.travel_option.available_seats, initial_seats + 2)
        self.assertEqual(booking.cancellation_reason, 'Changed plans')

    def test_booking_validation(self):
        with self.assertRaises(ValidationError):
            booking = Booking(
                user=self.user,
                travel_option=self.travel_option,
                number_of_seats=150,  # More than available
                contact_email='test@example.com',
                contact_phone='1234567890'
            )
            booking.full_clean()