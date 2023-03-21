from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.shortcuts import get_object_or_404
from .models import Booking, Customer


class TestViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='johns', password='3450123DGee%%')
        customer = cls.user
        cls.booking = Booking.objects.create(
            customer=customer,
            first_name='John',
            last_name='Smith',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',
            ability_level='Beginner',
            lesson_date='2023-10-10',
            lesson_time='09:00',
        )

    def test_get_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_customer_page(self):
        response = self.client.get('/customer/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer.html')

    def test_signup_login_links_page(self):
        response = self.client.get('/signuporlogin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_login_links.html')

    def test_customer_first_login_page(self):
        response = self.client.get('/customer/firstlogin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_first_login.html')

    def test_complete_customer_first_login_form(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.post(
            '/customer/firstlogin/',
            {
                'email': 'john@email.ie',
                'phone_num': '555 123 4567'
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        new_customer = Customer.objects.filter(user=user)
        self.assertEqual(len(new_customer), 1)

    def test_make_booking_page(self):
        response = self.client.get('/book/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'make_booking.html')

    def test_complete_make_booking_form(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.post(
            '/book/',
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': '1980-04-11',
                'height': '1.6',
                'weight': '65',
                'ability_level': 'Intermediate',
                'lesson_date': '2023-10-10',
                'lesson_time': '09:00',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        new_booking = Booking.objects.filter(customer=user, first_name='Jane')
        self.assertEqual(len(new_booking), 1)

    def test_complete_make_booking_form_prevents_double_bookings(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.post(
            '/book/',
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'date_of_birth': '1980-04-11',
                'height': '1.6',
                'weight': '75',
                'ability_level': 'Intermediate',
                'lesson_date': '2023-10-10',
                'lesson_time': '09:00',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        johns_bookings = Booking.objects.filter(
            customer=user, first_name='John')
        self.assertEqual(len(johns_bookings), 1)

    def test_view_bookings_page(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.get('/mybookings/', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_bookings.html')

    def test_edit_booking_page(self):
        user = self.user
        booking = self.booking
        self.client.force_login(user)
        response = self.client.get(f'/edit/{booking.id}', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_booking.html')

    def test_complete_edit_booking_form(self):
        user = self.user
        booking = self.booking
        self.client.force_login(user)
        response = self.client.post(
            f'/edit/{booking.id}',
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'date_of_birth': '1980-06-12',
                'height': '1.8',
                'weight': '75',
                'ability_level': 'Intermediate',
                'lesson_date': '2023-10-10',
                'lesson_time': '09:00',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mybookings/')
        edited_booking = get_object_or_404(Booking, id=booking.id)
        self.assertEqual(edited_booking.weight, 75.0)
        self.assertEqual(edited_booking.ability_level, 'Intermediate')

    def test_complete_edit_booking_form_does_not_allow_double_bookings(self):
        user = self.user
        booking = self.booking
        other_existing_booking = Booking.objects.create(
            customer=user,
            first_name='Jane',
            last_name='Smith',
            date_of_birth='1977-05-11',
            height='1.7',
            weight='65',
            ability_level='Beginner',
            lesson_date='2023-10-10',
            lesson_time='09:00',
        )
        self.client.force_login(user)
        response = self.client.post(
            f'/edit/{booking.id}',
            {
                'first_name': 'Jane',
                'last_name': 'Smith',
                'date_of_birth': '1980-04-10',
                'height': '1.8',
                'weight': '65',
                'ability_level': 'Beginner',
                'lesson_date': '2023-10-10',
                'lesson_time': '09:00',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        attempted_edited_booking = get_object_or_404(Booking, id=booking.id)
        self.assertEqual(attempted_edited_booking.first_name, 'John')

    def test_delete_booking(self):
        user = self.user
        booking = self.booking
        self.client.force_login(user)
        response = self.client.get(f'/delete/{booking.id}', user=user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mybookings/')
        existing_bookings = Booking.objects.filter(id=booking.id)
        self.assertEqual(len(existing_bookings), 0)
