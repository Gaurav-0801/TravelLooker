# accounts/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from bookings.models import Booking
from travel_options.models import TravelOption

User = get_user_model()

# --------------------------
# User Serializers
# --------------------------
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'password_confirm')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        from django.contrib.auth import authenticate
        user = authenticate(username=attrs['username'], password=attrs['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials.")
        attrs['user'] = user
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

# --------------------------
# Booking Serializers
# --------------------------
class BookingSerializer(serializers.ModelSerializer):
    travel = serializers.CharField(source='travel_option.id', read_only=True)

    class Meta:
        model = Booking
        fields = (
            'id', 'travel', 'type', 'source', 'destination', 'date', 'time',
            'passengers', 'total_price', 'status', 'booking_date', 'passenger_details'
        )

class BookingCreateSerializer(serializers.ModelSerializer):
    travelId = serializers.CharField(write_only=True)
    passengers = serializers.IntegerField()
    totalPrice = serializers.FloatField()
    passengerDetails = serializers.JSONField()

    class Meta:
        model = Booking
        fields = ('travelId', 'passengers', 'totalPrice', 'passengerDetails')

    def create(self, validated_data):
        user = self.context['request'].user
        travel_id = validated_data.pop('travelId')
        travel_option = TravelOption.objects.get(id=travel_id)

        booking = Booking.objects.create(
            user=user,
            travel_option=travel_option,
            type=travel_option.type,
            source=travel_option.source,
            destination=travel_option.destination,
            date=travel_option.date,
            time=travel_option.time,
            passengers=validated_data['passengers'],
            total_price=validated_data['totalPrice'],
            passenger_details=validated_data['passengerDetails'],
            status='CONFIRMED'
        )
        return booking

class BookingCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(required=False, allow_blank=True)
