from django.contrib import admin
from .models import TravelOption

@admin.register(TravelOption)
class TravelOptionAdmin(admin.ModelAdmin):
    list_display = ('travel_id', 'type', 'source', 'destination', 'departure_datetime', 
                   'price', 'available_seats', 'total_seats', 'is_active')
    list_filter = ('type', 'is_active', 'departure_datetime', 'source', 'destination')
    search_fields = ('travel_id', 'source', 'destination', 'operator_name')
    list_editable = ('is_active', 'available_seats')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('travel_id', 'type', 'operator_name')
        }),
        ('Route & Schedule', {
            'fields': ('source', 'destination', 'departure_datetime', 'arrival_datetime')
        }),
        ('Pricing & Capacity', {
            'fields': ('price', 'total_seats', 'available_seats')
        }),
        ('Additional Information', {
            'fields': ('description', 'amenities', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('travel_id',)
        return self.readonly_fields