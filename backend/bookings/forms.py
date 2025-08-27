from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['number_of_seats', 'contact_email', 'contact_phone', 'special_requests']
        widgets = {
            'special_requests': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['number_of_seats'].widget.attrs.update({
            'min': '1',
            'max': '10'  # You can adjust this limit
        })

    def clean_number_of_seats(self):
        seats = self.cleaned_data.get('number_of_seats')
        if seats and seats < 1:
            raise forms.ValidationError('Number of seats must be at least 1.')
        if seats and seats > 10:
            raise forms.ValidationError('Maximum 10 seats can be booked at once.')
        return seats

class BookingSearchForm(forms.Form):
    STATUS_CHOICES = [('', 'All Statuses')] + Booking.STATUS_CHOICES
    
    status = forms.ChoiceField(choices=STATUS_CHOICES, required=False)
    booking_id = forms.CharField(max_length=20, required=False)
    date_from = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'