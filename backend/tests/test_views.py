from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import json

from travel_options.models import TravelOption
from bookings.models import Booking

User = get_user_model()

class TravelOptionAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.future_date = timezone.now() + timedelta(days=7)
        self.arrival_date = self.future_date + timedelta(hours=2)
        
        self.travel_option = TravelOption.objects.create(
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

    def test_travel_option_list_api(self):
        response = self.client.get('/api/travel-options/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)

    def test_travel_option_detail_api(self):
        response = self.client.get(f'/api/travel-options/{self.travel_option.id}/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['travel_id'], 'FL001')

    def test_travel_option_search_api(self):
        search_data = {
            'source': 'New York',
            'destination': 'Los Angeles',
            'type': 'FLIGHT'
        }
        
        response = self.client.post(
            '/api/travel-options/search/',
            data=json.dumps(search_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['count'], 1)

class BookingAPITest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        self.future_date = timezone.now() + timedelta(days=7)
        self.arrival_date = self.future_date + timedelta(hours=2)
        
        self.travel_option = TravelOption.objects.create(
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

    def test_create_booking_api_authenticated(self):
        self.client.login(username='testuser', password='testpass123')
        
        booking_data = {
            'travel_option_id': self.travel_option.id,
            'number_of_seats': 2,
            'contact_email': 'test@example.com',
            'contact_phone': '1234567890'
        }
        
        response = self.client.post(
            '/api/bookings/create/',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        self.assertTrue(Booking.objects.filter(user=self.user).exists())

    def test_create_booking_api_unauthenticated(self):
        booking_data = {
            'travel_option_id': self.travel_option.id,
            'number_of_seats': 2,
            'contact_email': 'test@example.com',
            'contact_phone': '1234567890'
        }
        
        response = self.client.post(
            '/api/bookings/create/',
            data=json.dumps(booking_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 401)

    def test_user_bookings_api(self):
        self.client.login(username='testuser', password='testpass123')
        
        # Create a booking
        booking = Booking.objects.create(
            user=self.user,
            travel_option=self.travel_option,
            number_of_seats=2,
            contact_email='test@example.com',
            contact_phone='1234567890'
        )
        
        response = self.client.get('/api/bookings/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_user_registration_api(self):
        user_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'complexpass123',
            'password_confirm': 'complexpass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        
        response = self.client.post(
            '/api/accounts/register/',
            data=json.dumps(user_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertIn('user', data)
        self.assertIn('token', data)

    def test_user_login_api(self):
        # Create user first
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
        login_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        response = self.client.post(
            '/api/accounts/login/',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('user', data)
        self.assertIn('token', data)

    def test_user_login_invalid_credentials(self):
        login_data = {
            'username': 'nonexistent',
            'password': 'wrongpass'
        }
        
        response = self.client.post(
            '/api/accounts/login/',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)