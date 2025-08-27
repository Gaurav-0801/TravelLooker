from rest_framework import serializers
from django.utils import timezone
from .models import Booking, PassengerDetail
from travel_options.serializers import TravelOptionSerializer

class PassengerDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PassengerDetail
        fields = ['first_name', 'last_name', 'age', 'gender', 'id_number', 'seat_preference']

class BookingSerializer(serializers.ModelSerializer):
    travel_option = TravelOptionSerializer(read_only=True)
    passengers = PassengerDetailSerializer(many=True, read_only=True)
    can_be_cancelled = serializers.ReadOnlyField()
    is_upcoming = serializers.ReadOnlyField()
    days_until_travel = serializers.ReadOnlyField()

    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'travel_option', 'number_of_seats', 'total_price',
            'booking_date', 'status', 'passenger_details', 'contact_email',
            'contact_phone', 'special_requests', 'passengers', 'can_be_cancelled',
            'is_upcoming', 'days_until_travel', 'cancelled_at', 'cancellation_reason'
        ]

class BookingCreateSerializer(serializers.ModelSerializer):
    travel_option_id = serializers.IntegerField()
    passenger_details = serializers.JSONField(required=False, default=list)

    class Meta:
        model = Booking
        fields = [
            'travel_option_id', 'number_of_seats', 'contact_email',
            'contact_phone', 'special_requests', 'passenger_details'
        ]

    def validate_travel_option_id(self, value):
        from travel_options.models import TravelOption
        try:
            travel_option = TravelOption.objects.get(id=value, is_active=True)
            if travel_option.departure_datetime <= timezone.now():
                raise serializers.ValidationError("Cannot book past travel options")
            return value
        except TravelOption.DoesNotExist:
            raise serializers.ValidationError("Travel option not found or inactive")

    def validate(self, attrs):
        from travel_options.models import TravelOption
        
        travel_option = TravelOption.objects.get(id=attrs['travel_option_id'])
        
        if attrs['number_of_seats'] > travel_option.available_seats:
            raise serializers.ValidationError(
                f"Only {travel_option.available_seats} seats available"
            )
        
        # Validate passenger details if provided
        passenger_details = attrs.get('passenger_details', [])
        if passenger_details and len(passenger_details) != attrs['number_of_seats']:
            raise serializers.ValidationError(
                "Number of passenger details must match number of seats"
            )
        
        return attrs

    def create(self, validated_data):
        from travel_options.models import TravelOption
        
        travel_option_id = validated_data.pop('travel_option_id')
        travel_option = TravelOption.objects.get(id=travel_option_id)
        
        booking = Booking.objects.create(
            user=self.context['request'].user,
            travel_option=travel_option,
            total_price=travel_option.price * validated_data['number_of_seats'],
            **validated_data
        )
        
        return booking

class BookingCancelSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=500, required=False, default='')

    def validate(self, attrs):
        booking = self.context['booking']
        if not booking.can_be_cancelled:
            raise serializers.ValidationError("This booking cannot be cancelled")
        return attrs