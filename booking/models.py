from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,)
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    phone_num = models.CharField(max_length=20, null=False, blank=False)
    date_of_birth = models.DateField(null=False, blank=False)
    height = models.DecimalField(
        max_digits=3, decimal_places=2, null=False, blank=False)
    weight = models.DecimalField(
        max_digits=4, decimal_places=1, null=False, blank=False)

    def __str__(self):
        """
        Defines the name for an instance object of the
        Customer model overwriting the django default method.
        """
        return self.user.username


class Booking(models.Model):
    customer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings')
    ability_level = models.CharField(max_length=50, null=False, blank=False)
    lesson_date = models.DateField(null=False, blank=False)
    lesson_time = models.TimeField(null=False, blank=False)
    customer_requests = models.TextField(null=True, blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        """
        Defines the name for an instance object of the
        Booking model overwriting the django default method.
        """
        return str(self.lesson_date)
