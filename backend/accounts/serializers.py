from rest_framework import serializers
from .models import Booking
from travel_options.models import TravelOption

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
