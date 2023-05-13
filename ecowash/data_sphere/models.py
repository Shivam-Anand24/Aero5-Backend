# models.py
from django.db import models
from django.utils.crypto import get_random_string

class Role(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    token = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        # Generate a random token if creating a new user
        if not self.pk:
            self.token = get_random_string(length=10)

        super().save(*args, **kwargs)
