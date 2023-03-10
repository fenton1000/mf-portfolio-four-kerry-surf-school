from django import forms
from .models import Customer, Booking


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['email', 'phone_num']


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'height',
            'weight',
            'ability_level',
            'lesson_date',
            'lesson_time'
            ]
