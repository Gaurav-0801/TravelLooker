from django.contrib import admin
from .models import Booking, PassengerDetail

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'user', 'travel_option', 'number_of_seats', 
                   'total_price', 'status', 'booking_date')
    list_filter = ('status', 'booking_date', 'travel_option__type')
    search_fields = ('booking_id', 'user__username', 'user__email', 
                    'travel_option__travel_id', 'contact_email')
    readonly_fields = ('booking_id', 'created_at', 'updated_at', 'cancelled_at')
    list_editable = ('status',)
    
    fieldsets = (
        ('Booking Information', {
            'fields': ('booking_id', 'user', 'travel_option', 'status')
        }),
        ('Booking Details', {
            'fields': ('number_of_seats', 'total_price', 'contact_email', 
                      'contact_phone', 'special_requests')
        }),
        ('Passenger Information', {
            'fields': ('passenger_details',),
            'classes': ('collapse',)
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_reference'),
            'classes': ('collapse',)
        }),
        ('Cancellation', {
            'fields': ('cancelled_at', 'cancellation_reason'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('user', 'travel_option', 'number_of_seats')
        return self.readonly_fields

@admin.register(PassengerDetail)
class PassengerDetailAdmin(admin.ModelAdmin):
    list_display = ('booking', 'first_name', 'last_name', 'age', 'gender')
    list_filter = ('gender', 'booking__status')
    search_fields = ('first_name', 'last_name', 'booking__booking_id', 'id_number')