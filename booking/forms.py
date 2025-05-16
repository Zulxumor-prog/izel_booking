from django import forms
from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['client_name', 'phone', 'route', 'passports', 'photos', 'receipts', 'tour']
        exclude = ['agent', 'commission']
