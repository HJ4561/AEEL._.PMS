from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None  # Remove username, use email instead
    email = models.EmailField(unique=True, max_length=255)
    
    ROLE_CHOICES = (
        ('manager', 'Manager'),
        ('engineer', 'Engineer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='engineer')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # No other required fields besides email and password

    def __str__(self):
        return self.email