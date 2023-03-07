from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, primary_key=True,)
    email = models.EmailField(null=False, blank=False)
    phone_num = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.user.username

