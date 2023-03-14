from django.test import TestCase
from .forms import CustomerForm, BookingForm


class TestCustomerForm(TestCase):

    def test_email_is_required(self):
        form = CustomerForm({'email': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0], 'This field is required.')

    def test_phone_num_is_required(self):
        form = CustomerForm({'email': 'email@email.ie', 'phone_num': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('phone_num', form.errors.keys())
        self.assertEqual(
            form.errors['phone_num'][0], 'This field is required.')

    def test_fields_are_explicit_in_form_metaclass(self):
        form = CustomerForm()
        self.assertEqual(form.Meta.fields, ['email', 'phone_num'])


class TestBookingForm(TestCase):

    def test_first_name_is_required(self):
        form = BookingForm({'first_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(
            form.errors['first_name'][0], 'This field is required.')

    def test_last_name_is_required(self):
        form = BookingForm({'first_name': 'John', 'last_name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(
            form.errors['last_name'][0], 'This field is required.')

    def test_date_of_birth_is_required(self):
        form = BookingForm({
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('date_of_birth', form.errors.keys())
        self.assertEqual(
            form.errors['date_of_birth'][0], 'This field is required.')

    def test_height_is_required(self):
        form = BookingForm({
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': '1977-05-10',
            'height': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('height', form.errors.keys())
        self.assertEqual(
            form.errors['height'][0], 'This field is required.')

    def test_weight_is_required(self):
        form = BookingForm({
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': '1977-05-10',
            'height': '1.7',
            'weight': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('weight', form.errors.keys())
        self.assertEqual(
            form.errors['weight'][0], 'This field is required.')

    def test_ability_level_is_required(self):
        form = BookingForm({
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': '1977-05-10',
            'height': '1.7',
            'weight': '65',
            'ability_level': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('ability_level', form.errors.keys())
        self.assertEqual(
            form.errors['ability_level'][0], 'This field is required.')

    def test_lesson_date_is_required(self):
        form = BookingForm({
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': '1977-05-10',
            'height': '1.7',
            'weight': '65',
            'ability_level': 'Beginner',
            'lesson_date': '',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('lesson_date', form.errors.keys())
        self.assertEqual(
            form.errors['lesson_date'][0], 'This field is required.')

    def test_lesson_time_is_required(self):
        form = BookingForm({
            'first_name': 'John',
            'last_name': 'Smith',
            'date_of_birth': '1977-05-10',
            'height': '1.7',
            'weight': '65',
            'ability_level': 'Beginner',
            'lesson_date': '2023-10-10',
            'lesson_time': ''
        })
        self.assertFalse(form.is_valid())
        self.assertIn('lesson_time', form.errors.keys())
        self.assertEqual(
            form.errors['lesson_time'][0], 'This field is required.')

    def test_fields_are_explicit_in_form_metaclass(self):
        form = BookingForm()
        self.assertEqual(form.Meta.fields, [
            'first_name',
            'last_name',
            'date_of_birth',
            'height',
            'weight',
            'ability_level',
            'lesson_date',
            'lesson_time',
        ])
