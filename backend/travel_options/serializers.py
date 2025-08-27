from rest_framework import serializers
from .models import TravelOption

class TravelOptionSerializer(serializers.ModelSerializer):
    duration_hours = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()

    class Meta:
        model = TravelOption
        fields = [
            'id', 'travel_id', 'type', 'source', 'destination',
            'departure_datetime', 'arrival_datetime', 'price',
            'total_seats', 'available_seats', 'operator_name',
            'description', 'amenities', 'duration_hours', 'is_available'
        ]

class TravelOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = TravelOption
        fields = [
            'travel_id', 'type', 'source', 'destination',
            'departure_datetime', 'arrival_datetime', 'price',
            'total_seats', 'available_seats', 'operator_name',
            'description', 'amenities'
        ]

    def validate(self, attrs):
        if attrs['departure_datetime'] >= attrs['arrival_datetime']:
            raise serializers.ValidationError("Departure time must be before arrival time.")
        
        if attrs['available_seats'] > attrs['total_seats']:
            raise serializers.ValidationError("Available seats cannot exceed total seats.")
        
        return attrs

class TravelOptionSearchSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=100, required=False)
    destination = serializers.CharField(max_length=100, required=False)
    type = serializers.ChoiceField(choices=TravelOption.TRAVEL_TYPES, required=False)
    departure_date = serializers.DateField(required=False)
    min_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    max_price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    available_seats_min = serializers.IntegerField(min_value=1, required=False)
    
    def validate(self, attrs):
        min_price = attrs.get('min_price')
        max_price = attrs.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise serializers.ValidationError("Minimum price cannot be greater than maximum price.")
        
        return attrs