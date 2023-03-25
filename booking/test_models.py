from django.test import TestCase
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from .models import Booking, Customer


class TestModels(TestCase):

    def test_delete_user_deletes_customer_and_booking_on_cascade(self):
        user = User.objects.create(
            username='johns', password='3450123DGee%%')
        customer = Customer.objects.create(
            user=user,
            first_name='John',
            last_name='Smith',
            email='john@email.ie',
            phone_num='555 123 4567',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',
        )
        booking = Booking.objects.create(
            customer=user,
            ability_level='Beginner',
            lesson_date='2023-10-10',
            lesson_time='09:00',
        )
        customers = Customer.objects.filter(user=user)
        self.assertEqual(len(customers), 1)
        bookings = Booking.objects.filter(customer=user)
        self.assertEqual(len(bookings), 1)
        test_user = get_object_or_404(User, username='johns')
        test_user.delete()
        customers = Customer.objects.filter(user=user)
        self.assertEqual(len(customers), 0)
        bookings = Booking.objects.filter(customer=user)
        self.assertEqual(len(bookings), 0)

    def test_customer_string_method_returns_username(self):
        user = User.objects.create(
            username='johns', password='3450123DGee%%')
        customer = Customer.objects.create(
            user=user,
            first_name='John',
            last_name='Smith',
            email='john@email.ie',
            phone_num='555 123 4567',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',
        )
        self.assertEqual(str(customer), 'johns')

    def test_booking_string_method_returns_lesson_date(self):
        user = User.objects.create(
            username='johns', password='3450123DGee%%')
        customer = Customer.objects.create(
            user=user,
            first_name='John',
            last_name='Smith',
            email='john@email.ie',
            phone_num='555 123 4567',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',
        )
        booking = Booking.objects.create(
            customer=user,
            ability_level='Beginner',
            lesson_date='2023-10-10',
            lesson_time='09:00',
        )
        self.assertEqual(str(booking), '2023-10-10')
