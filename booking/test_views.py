from django.test import TestCase
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Booking, Customer


class TestReadOnlyViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='johns', password='3450123DGee%%')
        u = cls.user
        cls.customer = Customer.objects.create(
            user=u,
            first_name='John',
            last_name='Smith',
            email='john@email.ie',
            phone_num='555 123 4567',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',
        )

    def test_get_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_customer_page(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.get('/customer/', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer.html')

    def test_get_customer_page_redirects_when_no_customer_details(self):
        user = self.user
        customer = Customer.objects.filter(user=user)
        customer.delete()
        self.client.force_login(user)
        response = self.client.get('/customer/', user=user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/firstlogin/')

    def test_signup_login_links_page(self):
        response = self.client.get('/signuporlogin/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_login_links.html')

    def test_view_bookings_page(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.get('/mybookings/', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'view_bookings.html')

    def test_get_view_bookings_page_redirects_when_no_customer_details(self):
        user = self.user
        customer = Customer.objects.filter(user=user)
        customer.delete()
        self.client.force_login(user)
        response = self.client.get('/mybookings/', user=user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/firstlogin/')


class TestAddCustomerViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='johns', password='3450123DGee%%')

    def test_customer_first_login_page(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.get('/customer/firstlogin/', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_first_login.html')

    def test_complete_customer_first_login_form(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.post(
            '/customer/firstlogin/',
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john@email.ie',
                'phone_num': '555 123 4567',
                'date_of_birth': '1980-04-10',
                'height': '1.8',
                'weight': '65',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        new_customer = Customer.objects.filter(user=user)
        self.assertEqual(len(new_customer), 1)


class TestEditDeleteCustomerViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='johns', password='3450123DGee%%')
        u = cls.user
        cls.customer = Customer.objects.create(
            user=u,
            first_name='John',
            last_name='Smith',
            email='john@email.ie',
            phone_num='555 123 4567',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',
        )

    def test_edit_customer_page(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.get('/editprofile/', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_profile.html')

    def test_complete_edit_customer_form(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.post(
            '/editprofile/',
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'email': 'john@myemail.ie',
                'phone_num': '555 123 4567',
                'date_of_birth': '1980-04-10',
                'height': '1.7',
                'weight': '65',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        edited_customer = get_object_or_404(Customer, user=user)
        self.assertEqual(edited_customer.email, 'john@myemail.ie')
        self.assertEqual(str(edited_customer.height), '1.70')

    def test_delete_user(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.get('/deleteprofile/', user=user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        check_user = User.objects.filter(id=user.id)
        self.assertEqual(len(check_user), 0)


class TestMakeBookingViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='johns', password='3450123DGee%%')
        u = cls.user
        cls.customer = Customer.objects.create(
            user=u,
            first_name='John',
            last_name='Smith',
            email='john@email.ie',
            phone_num='555 123 4567',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',

        )
        cls.booking = Booking.objects.create(
            customer=u,
            ability_level='Beginner',
            lesson_date='2023-10-10',
            lesson_time='09:00',
        )

    def test_make_booking_page(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.get('/book/', user=user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'make_booking.html')

    def test_get_make_booking_page_redirects_when_no_customer_details(self):
        user = self.user
        customer = Customer.objects.filter(user=user)
        customer.delete()
        self.client.force_login(user)
        response = self.client.get('/book/', user=user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/firstlogin/')

    def test_complete_make_booking_form(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.post(
            '/book/',
            {
                'ability_level': 'Intermediate',
                'lesson_date': '2023-10-11',
                'lesson_time': '09:00',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        bookings = Booking.objects.filter(customer=user)
        self.assertEqual(len(bookings), 2)

    def test_complete_make_booking_approved_defaults_to_false(self):
        booking = self.booking
        self.assertEqual(booking.approved, False)

    def test_complete_make_booking_form_prevents_double_bookings(self):
        user = self.user
        self.client.force_login(user)
        response = self.client.post(
            '/book/',
            {
                'ability_level': 'Intermediate',
                'lesson_date': '2023-10-10',
                'lesson_time': '09:00',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        bookings = Booking.objects.filter(customer=user)
        self.assertEqual(len(bookings), 1)


class TestEditDeleteBookingViews(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(
            username='johns', password='3450123DGee%%')
        u = cls.user
        cls.customer = Customer.objects.create(
            user=u,
            first_name='John',
            last_name='Smith',
            email='john@email.ie',
            phone_num='555 123 4567',
            date_of_birth='1980-04-10',
            height='1.8',
            weight='65',

        )
        cls.booking = Booking.objects.create(
            customer=u,
            ability_level='Beginner',
            lesson_date='2023-10-10',
            lesson_time='09:00',
        )

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
                'ability_level': 'Intermediate',
                'lesson_date': '2023-10-10',
                'lesson_time': '09:00',
                'customer_requests': 'My request',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mybookings/')
        edited_booking = get_object_or_404(Booking, id=booking.id)
        self.assertEqual(edited_booking.customer_requests, 'My request')
        self.assertEqual(edited_booking.ability_level, 'Intermediate')

    def test_complete_edit_booking_form_does_not_allow_double_bookings(self):
        user = self.user
        booking = self.booking
        other_existing_booking = Booking.objects.create(
            customer=user,
            ability_level='Beginner',
            lesson_date='2023-10-11',
            lesson_time='11:00',
        )
        self.client.force_login(user)
        response = self.client.post(
            f'/edit/{booking.id}',
            {
                'ability_level': 'Intermediate',
                'lesson_date': '2023-10-11',
                'lesson_time': '11:00',
            },
            user=user,
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/customer/')
        attempted_edited_booking = get_object_or_404(Booking, id=booking.id)
        self.assertEqual(attempted_edited_booking.ability_level, 'Beginner')

    def test_delete_booking(self):
        user = self.user
        booking = self.booking
        self.client.force_login(user)
        response = self.client.get(f'/delete/{booking.id}', user=user)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/mybookings/')
        existing_bookings = Booking.objects.filter(id=booking.id)
        self.assertEqual(len(existing_bookings), 0)
