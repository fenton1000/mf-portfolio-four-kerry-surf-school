from django import forms
from .models import Customer, Booking


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = [
            'first_name',
            'last_name',
            'email',
            'phone_num',
            'date_of_birth',
            'height',
            'weight'
        ]


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = [
            'ability_level',
            'lesson_date',
            'lesson_time',
            'customer_requests'
            ]
